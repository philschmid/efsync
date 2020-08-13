import pytest
from main import efsync, load_args_from_yaml


def test_load_args_from_yaml():
    res = load_args_from_yaml()
    assert isinstance(res, dict)


def test_main():
    res = efsync()
    assert res == True
