from src.codeFiles.add_subtract import add, subtract

def test_add():
    assert add(1, 5) == 6

def test_subtract():
    assert subtract(6, 2) == 4
