import pytest
from efsync.main import efsync

efsync_path = 'efsync/test/efsync.yaml'

def test_main():
    res = efsync(efsync_path)
    assert res == True
