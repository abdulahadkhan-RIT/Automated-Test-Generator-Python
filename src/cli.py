import click
import os
from parser import CodeParser  # Changed to absolute import
from generator import TestCaseGenerator  # Changed to absolute import

@click.command()
@click.argument('file_path')
def generate_tests(file_path):
    """CLI tool to generate automated test cases from Python code."""
    if not os.path.exists(file_path):
        click.echo(f"Error: {file_path} does not exist.")
        return

    # Read the file content
    with open(file_path, 'r') as file:
        code = file.read()

    # Parse code and extract functions and classes
    parser = CodeParser(code)
    functions = parser.get_functions()
    classes = parser.get_classes()

    # Generate test cases
    generator = TestCaseGenerator(functions, classes)
    test_cases = generator.generate_unit_tests(file_path)

    # Extract filename without extension for test file naming
    filename = os.path.splitext(os.path.basename(file_path))[0]
    test_file_name = f"{filename}_test.py"
    
    # Save the test cases to a file
    test_file_path = os.path.join('tests', test_file_name)
    with open(test_file_path, 'w') as test_file:
        test_file.write(test_cases)

    click.echo(f"Test cases generated successfully and saved to {test_file_path}.")

if __name__ == '__main__':
    generate_tests()