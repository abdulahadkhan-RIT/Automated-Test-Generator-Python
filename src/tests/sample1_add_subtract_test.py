import pytest
from codeFiles.sample1_add_subtract import add, subtract

def test_add():
    """Tests the add function."""
    assert add('a_example', 'b_example') == 'expected_value'

def test_subtract():
    """Tests the subtract function."""
    assert subtract('a_example', 'b_example') == 'expected_value'