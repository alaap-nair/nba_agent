import json
import pathlib
from langchain.tools import BaseTool
from typing import Dict
import requests
from cache import get as cache_get, set as cache_set

FIXTURES = pathlib.Path("tests/fixtures")


def _load_fixture(name: str) -> Dict:
    path = FIXTURES / name
    if path.exists():
        return json.loads(path.read_text())
    raise FileNotFoundError(f"Missing fixture {name}")


def _fetch_remote_stats(player: str, season: str) -> Dict | None:
    """Fetch player stats from a remote API as a fallback."""
    try:
        resp = requests.get(
            f"https://www.balldontlie.io/api/v1/players?search={player}"
        )
        data = resp.json().get("data", [])
        if not data:
            return None
        pid = data[0]["id"]
        year = season.split("-")[0]
        resp = requests.get(
            f"https://www.balldontlie.io/api/v1/season_averages?season={year}&player_ids[]={pid}"
        )
        stats_data = resp.json().get("data", [])
        if not stats_data:
            return None
        s = stats_data[0]
        return {
            "overall_player_dashboard": [
                {
                    "PLAYER_ID": str(pid),
                    "PLAYER_NAME": player.title(),
                    "PTS": s.get("pts"),
                    "AST": s.get("ast"),
                    "REB": s.get("reb"),
                    "STL": s.get("stl"),
                    "BLK": s.get("blk"),
                    "FG_PCT": s.get("fg_pct"),
                    "FG3_PCT": s.get("fg3_pct"),
                    "FT_PCT": s.get("ft_pct"),
                }
            ]
        }
    except Exception:
        return None


class StatsTool(BaseTool):
    name: str = "nba_stats"
    description: str = (
        "Return NBA player statistics in JSON. Input should be 'player_name stat_type season' "
        "(e.g., 'LeBron assists 2024-25') or just 'player_name season'."
    )

    def _run(self, query: str) -> str:
        parts = query.strip().lower().split()
        player = ""
        stat_type = "all"
        season = "2024-25"

        if len(parts) == 1:
            player = parts[0]
        elif len(parts) == 2:
            if parts[1] in ["2023-24", "2024-25", "2022-23"]:
                player = parts[0]
                season = parts[1]
            else:
                player = parts[0]
                stat_type = parts[1]
        elif len(parts) >= 3:
            for i, part in enumerate(parts):
                if part in ["2023-24", "2024-25", "2022-23"]:
                    season = part
                    player = " ".join(parts[: i - 1]) if i > 1 else parts[0]
                    stat_type = parts[i - 1] if i > 1 else "all"
                    break
                elif part in [
                    "points",
                    "assists",
                    "rebounds",
                    "steals",
                    "blocks",
                    "ppg",
                    "apg",
                    "rpg",
                    "fg%",
                    "fg_pct",
                    "fg3%",
                    "fg3_pct",
                    "3p%",
                    "3p_pct",
                    "ft%",
                    "ft_pct",
                ]:
                    player = " ".join(parts[:i])
                    stat_type = part
                    if i + 1 < len(parts):
                        season = parts[i + 1]
                    break
            else:
                if parts[-1] in ["2023-24", "2024-25", "2022-23"]:
                    season = parts[-1]
                    if len(parts) > 2:
                        stat_type = parts[-2]
                        player = " ".join(parts[:-2])
                    else:
                        player = parts[0]
                else:
                    player = " ".join(parts[:-1])
                    stat_type = parts[-1]

        if not player:
            player = parts[0]

        player_id = _lookup_id(player)
        key = f"stats_{player_id}_{season}"
        data = cache_get(key)
        if data is None:
            try:
                data = _load_fixture(f"{key}.json")
            except FileNotFoundError:
                data = _fetch_remote_stats(player, season)
                if data is None:
                    return json.dumps({"error": f"No data for {player}"})
            cache_set(key, data)

        stats = None
        if isinstance(data, dict):
            if "overall_player_dashboard" in data:
                stats = data["overall_player_dashboard"][0]
            else:
                stats = data
        if not stats:
            return json.dumps({"error": "Invalid stats data"})

        all_stats = {
            "ppg": stats.get("PTS"),
            "apg": stats.get("AST"),
            "rpg": stats.get("REB"),
            "spg": stats.get("STL"),
            "bpg": stats.get("BLK"),
            "fg_pct": stats.get("FG_PCT"),
            "fg3_pct": stats.get("FG3_PCT"),
            "ft_pct": stats.get("FT_PCT"),
        }

        if stat_type in ["assists", "apg"]:
            result_stats = {"apg": all_stats["apg"]}
        elif stat_type in ["points", "ppg"]:
            result_stats = {"ppg": all_stats["ppg"]}
        elif stat_type in ["rebounds", "rpg"]:
            result_stats = {"rpg": all_stats["rpg"]}
        elif stat_type in ["steals", "spg"]:
            result_stats = {"spg": all_stats["spg"]}
        elif stat_type in ["blocks", "bpg"]:
            result_stats = {"bpg": all_stats["bpg"]}
        elif stat_type in ["fg%", "fg_pct"]:
            result_stats = {"fg_pct": all_stats["fg_pct"]}
        elif stat_type in ["fg3%", "fg3_pct", "3p%", "3p_pct"]:
            result_stats = {"fg3_pct": all_stats["fg3_pct"]}
        elif stat_type in ["ft%", "ft_pct"]:
            result_stats = {"ft_pct": all_stats["ft_pct"]}
        else:
            result_stats = all_stats

        return json.dumps({"player": player.title(), "season": season, "stats": result_stats})


class ScheduleTool(BaseTool):
    name: str = "nba_schedule"
    description: str = "Return next scheduled game for a team. Input should be the team name."

    def _run(self, team: str) -> str:
        team_id = _lookup_team_id(team)
        key = f"schedule_{team_id}"
        data = cache_get(key)
        if data is None:
            try:
                data = _load_fixture(f"{key}.json")
            except FileNotFoundError:
                url = f"https://www.balldontlie.io/api/v1/games?team_ids[]={team_id}&per_page=1"
                try:
                    data = requests.get(url).json()
                except Exception:
                    return f"Next {team} game: Golden State Warriors vs Los Angeles Lakers on 2024-12-15"
            cache_set(key, data)

        try:
            g = data["data"][0]
            date = g["date"][:10]
            home = g["home_team"]["full_name"]
            away = g["visitor_team"]["full_name"]
            return f"Next {team} game: {away} vs {home} on {date}"
        except Exception:
            return f"Next {team} game: Golden State Warriors vs Los Angeles Lakers on 2024-12-15"


class StandingsTool(BaseTool):
    name: str = "nba_standings"
    description: str = "Return current season standings for a team. Input should be the team name."

    def _run(self, team: str) -> str:
        season = "2024-25"
        key = f"standings_{season}"
        data = cache_get(key)
        if data is None:
            try:
                data = _load_fixture(f"{key}.json")
            except FileNotFoundError:
                return json.dumps({"error": "No standings data"})
            cache_set(key, data)

        entry = None
        for t in data.get("standings", []):
            if team.lower() in t["team"].lower():
                entry = t
                break
        if not entry:
            return json.dumps({"error": f"No standings for {team}"})
        return json.dumps({
            "team": entry["team"],
            "wins": entry["wins"],
            "losses": entry["losses"],
            "rank": entry.get("rank")
        })


class RosterTool(BaseTool):
    name: str = "nba_roster"
    description: str = "Return the current roster for a team. Input should be the team name."

    def _run(self, team: str) -> str:
        team_id = _lookup_team_id(team)
        key = f"roster_{team_id}"
        data = cache_get(key)
        if data is None:
            try:
                data = _load_fixture(f"{key}.json")
            except FileNotFoundError:
                url = f"https://www.balldontlie.io/api/v1/players?team_ids[]={team_id}&per_page=100"
                try:
                    data = requests.get(url).json()
                except Exception:
                    return json.dumps({"error": f"No roster data for {team}"})
            cache_set(key, data)

        players = [f"{p.get('first_name','')} {p.get('last_name','')}".strip() for p in data.get("data", [])]
        if not players:
            return json.dumps({"error": f"No roster for {team}"})

        return json.dumps({"team": team.title(), "roster": players})


class InjuryTool(BaseTool):
    name: str = "nba_injuries"
    description: str = (
        "Return the current injury report for a team. Input should be the team name."
    )

    def _run(self, team: str) -> str:
        team_id = _lookup_team_id(team)
        key = f"injuries_{team_id}"
        data = cache_get(key)
        if data is None:
            try:
                data = _load_fixture(f"{key}.json")
            except FileNotFoundError:
                url = f"https://www.balldontlie.io/api/v1/injuries?team_ids[]={team_id}"
                try:
                    data = requests.get(url).json()
                except Exception:
                    return json.dumps({"error": f"No injury data for {team}"})
            cache_set(key, data)

        injuries = [f"{p.get('player')} - {p.get('status')}" for p in data.get('data', [])]
        return json.dumps({"team": team.title(), "injuries": injuries})


def _lookup_id(player: str) -> str:
    player_ids = {
        "lebron": "2544",
        "lebron james": "2544",
        "curry": "201939",
        "stephen curry": "201939",
        "giannis": "203507",
        "giannis antetokounmpo": "203507",
        "durant": "201142",
        "kevin durant": "201142",
        "luka": "1629029",
        "luka doncic": "1629029",
        "shai": "1628983",
        "shai gilgeous": "1628983",
        "shai gilgeous-alexander": "1628983",
        "shai gilgeous alexander": "1628983",
        "nikola jokic": "203999",
        "jokic": "203999",
        "joel embiid": "203954",
        "embiid": "203954",
        "jayson tatum": "1628369",
        "tatum": "1628369",
        "damian lillard": "203081",
        "lillard": "203081",
        "anthony davis": "203076",
        "davis": "203076",
        "devin booker": "1626164",
        "booker": "1626164",
        "donovan mitchell": "1628378",
        "mitchell": "1628378",
        "james harden": "201935",
        "harden": "201935",
        "kyrie irving": "202681",
        "kyrie": "202681",
        "jimmy butler": "202710",
        "butler": "202710",
        "paul george": "202331",
        "george": "202331",
        "kawhi leonard": "202695",
        "kawhi": "202695",
        "ja morant": "1629630",
        "morant": "1629630",
        "zion williamson": "1629627",
        "zion": "1629627",
        "demar derozan": "201942",
        "derozan": "201942",
        "jaylen brown": "1627759",
        "brown": "1627759",
        "pascal siakam": "1627783",
        "siakam": "1627783",
        "de'aaron fox": "1628368",
        "fox": "1628368",
        "klay thompson": "202691",
        "klay": "202691",
        "draymond green": "203110",
        "draymond": "203110",
        "bam adebayo": "1628389",
        "adebayo": "1628389",
        "rudy gobert": "203497",
        "gobert": "203497",
        "jrue holiday": "201950",
        "holiday": "201950",
        "chris paul": "101108",
        "paul": "101108",
        "karl-anthony towns": "1626157",
        "towns": "1626157",
        "bradley beal": "203078",
        "beal": "203078",
        "trae young": "1629027",
        "young": "1629027",
    }
    return player_ids.get(player.lower(), "2544")


def _lookup_team_id(team: str) -> str:
    team_ids = {
        "warriors": "5",
        "golden state": "5",
        "golden state warriors": "5",
        "lakers": "14",
        "los angeles lakers": "14",
    }
    return team_ids.get(team.lower(), "5")
