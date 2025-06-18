import json
import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Provide minimal langchain stubs if library not installed
if 'langchain' not in sys.modules:
    import types
    langchain = types.ModuleType('langchain')
    tools_mod = types.ModuleType('tools')
    class DummyTool:
        def __init__(self, *a, **kw):
            pass
    tools_mod.BaseTool = DummyTool
    langchain.tools = tools_mod
    sys.modules['langchain'] = langchain
    sys.modules['langchain.tools'] = tools_mod

if 'requests' not in sys.modules:
    import types
    requests = types.ModuleType('requests')
    def dummy_get(*a, **kw):
        class Dummy:
            def json(self_inner):
                return {}
        return Dummy()
    requests.get = dummy_get
    sys.modules['requests'] = requests

from tools import (
    StatsTool,
    ScheduleTool,
    StandingsTool,
    RosterTool,
    ArenaTool,
    _lookup_id,
    _lookup_team_id,
)
from cache import _path_for_key, _memory_cache


def test_stats_tool_uses_fixture_and_cache(tmp_path, monkeypatch):
    tool = StatsTool()
    key = f"stats_{_lookup_id('lebron')}_2024-25"
    cache_file = _path_for_key(key)
    if cache_file.exists():
        cache_file.unlink()

    result = json.loads(tool._run('LeBron 2024-25'))
    assert result['player'] == 'Lebron'
    assert 'ppg' in result['stats']
    assert cache_file.exists()
    mtime = cache_file.stat().st_mtime

    # second call should read from cache and not modify file
    result2 = json.loads(tool._run('LeBron 2024-25'))
    assert cache_file.stat().st_mtime == mtime
    assert result2 == result


def test_schedule_tool_returns_game():
    tool = ScheduleTool()
    out = tool._run('Warriors')
    assert 'Next Warriors game' in out


def test_roster_tool():
    tool = RosterTool()
    key = f"roster_{_lookup_team_id('Warriors')}"
    cache_file = _path_for_key(key)
    if cache_file.exists():
        cache_file.unlink()
    if key in _memory_cache:
        del _memory_cache[key]

    data = json.loads(tool._run('Warriors'))
    assert data['team'].startswith('Warriors') or data['team'].startswith('Golden')
    assert any('Curry' in p for p in data['roster'])
    assert cache_file.exists()


def test_arena_tool():
    tool = ArenaTool()
    key = f"arena_{_lookup_team_id('Warriors')}"
    cache_file = _path_for_key(key)
    if cache_file.exists():
        cache_file.unlink()
    if key in _memory_cache:
        del _memory_cache[key]

    data = json.loads(tool._run('Warriors'))
    assert data['team'].startswith('Golden')
    assert 'arena' in data
    assert cache_file.exists()

def test_standings_tool():
    tool = StandingsTool()
    data = json.loads(tool._run('Warriors'))
    assert data['team'].startswith('Golden')
    assert 'wins' in data


def test_new_player_stats():
    tool = StatsTool()
    result = json.loads(tool._run('Shai 2024-25'))
    assert result['player'].startswith('Shai')
    assert 'ppg' in result['stats']


def test_stats_tool_remote(monkeypatch):
    tool = StatsTool()
    key = "stats_1000_2024-25"
    cache_file = _path_for_key(key)
    if cache_file.exists():
        cache_file.unlink()
    if key in _memory_cache:
        del _memory_cache[key]

    def fake_load(name):
        raise FileNotFoundError

    def fake_fetch(player, season):
        return {
            "overall_player_dashboard": [
                {
                    "PLAYER_ID": "1000",
                    "PLAYER_NAME": player.title(),
                    "PTS": 22,
                    "AST": 5,
                    "REB": 6,
                    "STL": 1,
                    "BLK": 1,
                }
            ]
        }

    monkeypatch.setattr('tools._load_fixture', fake_load)
    monkeypatch.setattr('tools._fetch_remote_stats', fake_fetch)
    monkeypatch.setattr('tools._lookup_id', lambda p: '1000')

    result = json.loads(tool._run('Remote Guy 2024-25'))
    assert result['player'].startswith('Remote Guy'.split()[0])
    assert result['stats']['ppg'] == 22


def test_stats_tool_fg_pct(monkeypatch):
    tool = StatsTool()
    key = "stats_1000_2024-25"
    cache_file = _path_for_key(key)
    if cache_file.exists():
        cache_file.unlink()
    if key in _memory_cache:
        del _memory_cache[key]

    def fake_load(name):
        raise FileNotFoundError

    def fake_fetch(player, season):
        return {
            "overall_player_dashboard": [
                {
                    "PLAYER_ID": "1000",
                    "PLAYER_NAME": player.title(),
                    "PTS": 30,
                    "AST": 5,
                    "REB": 7,
                    "STL": 2,
                    "BLK": 1,
                    "FG_PCT": 0.55,
                    "FG3_PCT": 0.4,
                    "FT_PCT": 0.85,
                }
            ]
        }

    monkeypatch.setattr('tools._load_fixture', fake_load)
    monkeypatch.setattr('tools._fetch_remote_stats', fake_fetch)
    monkeypatch.setattr('tools._lookup_id', lambda p: '1000')

    result = json.loads(tool._run('Remote Guy fg% 2024-25'))
    assert result['stats']['fg_pct'] == 0.55

