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

from tools import StatsTool, ScheduleTool, StandingsTool, _lookup_id
from cache import _path_for_key


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


def test_standings_tool():
    tool = StandingsTool()
    data = json.loads(tool._run('Warriors'))
    assert data['team'].startswith('Golden')
    assert 'wins' in data

