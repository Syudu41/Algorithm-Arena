"""Offline request parsing and safe Codex launcher protocol; no AI calls."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / 'scripts/manim_agent.py'
spec = importlib.util.spec_from_file_location('manim_agent_cli', SCRIPT)
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


def request(*args):
    return cli.request_from_args(cli.parser().parse_args(args))


def test_natural_command_and_optional_link():
    data = request('insertion', 'sort', 'algo', 'https://algs4.cs.princeton.edu/21elementary/', '--values=-3,0,2,2')
    assert data['algorithm'] == 'insertion sort'
    assert data['values'] == [-3,0,2,2]
    assert data['reference'].startswith('https://algs4.')
    assert data['mode'] == 'both' and data['quality'] == 'release'


@pytest.mark.parametrize('args', [
    ['sort; touch /tmp/not-a-command'],
    ['insertion','--reference','file:///etc/passwd'],
    ['insertion','--reference','https://user:password@example.com'],
    ['insertion','--values','1.5,2'],
    ['insertion','--values','100,2'],
    ['insertion','--output-dir','../outside'],
    ['insertion','--output-dir','.'],
])
def test_rejects_invalid_request_data(args):
    with pytest.raises(ValueError):
        request(*args)


def test_dry_run_never_calls_codex(monkeypatch, capsys):
    def forbidden(*a, **k):
        pytest.fail('dry run invoked a subprocess')
    monkeypatch.setattr(cli.subprocess,'run',forbidden)
    assert cli.main(['insertion','sort','--dry-run']) == 0
    protocol = json.loads(capsys.readouterr().out)
    assert protocol['argv'][-1] == '-'
    assert protocol['request']['algorithm'] == 'insertion sort'


def test_real_launch_uses_argv_and_stdin(monkeypatch):
    calls=[]
    monkeypatch.setattr(cli.shutil,'which',lambda _: '/tools/codex')
    monkeypatch.setattr(cli.subprocess,'run',lambda args,**kwargs: calls.append((args,kwargs)) or SimpleNamespace(returncode=7))
    assert cli.main(['bubble','sort','--mode','custom','--pace','slow']) == 7
    args,kwargs=calls[0]
    assert args == ['/tools/codex','exec','--cd',str(cli.ROOT),'--sandbox','workspace-write','-']
    assert kwargs['shell'] is False
    assert '"algorithm": "bubble sort"' in kwargs['input']
    assert kwargs['cwd'] == cli.ROOT
