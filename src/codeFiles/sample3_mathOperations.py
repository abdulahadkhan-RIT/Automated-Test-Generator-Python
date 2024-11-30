class MathOperations:
    def add(self, a, b):
        """Returns the sum of a and b."""
        return a + b

    def divide(self, a, b):
        """Returns the division of a by b. Raises ValueError if b is zero."""
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b

    def is_prime(self, n):
        """Checks if a number n is prime."""
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

def factorial(n):
    """Returns the factorial of a number n. Raises ValueError for negative inputs."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def fibonacci(n):
    """Returns the nth Fibonacci number. Raises ValueError if n is negative."""
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative indices.")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
