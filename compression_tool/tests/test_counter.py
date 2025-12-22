import pytest

from app.services.counter import Counter


def test_counting():
    result = Counter.from_file("tests/test.txt")
    assert result[b't'] == 223000
    assert result[b'X'] == 333
