import pytest
from efsync.main import efsync, load_args_from_yaml

efsync_path = 'efsync/test/efsync.yaml'


def test_load_args_from_yaml():
    res = load_args_from_yaml(efsync_path)

    assert isinstance(res, dict)


def test_main():
    res = efsync(efsync_path)
    assert res == True
