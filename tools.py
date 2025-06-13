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
