import pytest

from codeFiles.sample3_mathOperations import factorial, fibonacci, MathOperations

math = MathOperations()

def test_factorial():
    assert factorial(5) == 120
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(10) == 3628800

def test_fibonacci():
    assert fibonacci(5) == 5
    assert fibonacci(1) == 1
    assert fibonacci(20) == 6765
    assert fibonacci(0) == 0
    assert fibonacci(50) == 12586269025

def test_add():
    assert math.add(3, 5) == 8
    assert math.add(-1, 1) == 0
    assert math.add(0, 0) == 0

def test_divide():
    assert math.divide(10, 2) == 5
    assert math.divide(0, 5) == 0
    assert math.divide(-10, 2) == -5
    with pytest.raises(ZeroDivisionError):
        math.divide(5, 0)

def test_is_prime():
    assert math.is_prime(7) == True
    assert math.is_prime(1) == False
    assert math.is_prime(2) == True
    assert math.is_prime(0) == False