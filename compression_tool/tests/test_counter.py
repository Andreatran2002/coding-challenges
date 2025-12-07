import pytest

from app.services.counter import Counter


def test_counting():
    result = Counter.from_file("tests/test.txt")
    assert result["t"] == 223000
    assert result["X"] == 333
