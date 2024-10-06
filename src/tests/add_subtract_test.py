from codeFiles.add_subtract import add, subtract

def test_add():
    assert add(3, 4) == 7

def test_subtract():
    assert subtract(4, 3) == 1
