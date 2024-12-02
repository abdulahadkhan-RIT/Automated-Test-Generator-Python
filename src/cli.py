import click
import os
from dotenv import load_dotenv
from parser import CodeParser
from generator import TestCaseGenerator, ChatGPTTestCaseGenerator
import openai

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def format_check(test_cases, api_key):
    """
    Use AI to check and correct the formatting of the test cases.
    """
    prompt = f"""
    The following Python test cases are auto-generated. They are all supposed to be in one file and should not have any redundancies escpecially with 
    respect to imports.
    Check them for any formatting or syntax issues and correct them to ensure they are clean and properly formatted:
    {test_cases}

    Return the corrected test cases. Give only the correct as the output and nothing else at all.
    """

    openai.api_key = api_key
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=1500
    )
    
    return response.choices[0].message.content.strip()

@click.command()
@click.argument('file_path')
@click.option('--output-dir', default='tests', help="Directory to save test files.")
@click.option('--overwrite', is_flag=True, help="Overwrite existing test files if they already exist.")
@click.option('--framework', default='pytest', type=click.Choice(['pytest', 'unittest', 'nose2'], case_sensitive=False), help="Test framework to use.")
@click.option('--use-ai', is_flag=True, help="Use ChatGPT to generate test cases.")
@click.option('--custom-templates', is_flag=True, help="Use custom test templates for generating tests.")
@click.option('--coverage-report', is_flag=True, help="Generate a coverage report for the tests.")
@click.option('--ci-integration', is_flag=True, help="Generate configuration for CI tools like GitHub Actions.")

def generate_tests(file_path, output_dir, overwrite, framework, use_ai, custom_templates, coverage_report, ci_integration):
    """CLI tool to generate automated test cases from Python code."""
    if not os.path.exists(file_path):
        click.echo(f"Error: {file_path} does not exist.")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read the file content
    with open(file_path, 'r') as file:
        code = file.read()

    # Parse code and extract functions and classes
    parser = CodeParser(code)
    functions = parser.get_functions()
    classes = parser.get_classes()

    # Generate test cases
    if use_ai:
        if not api_key:
            click.echo("Error: API key is required for AI-based test generation.")
            return
        generator = ChatGPTTestCaseGenerator(functions, classes, framework, api_key)
    else:
        generator = TestCaseGenerator(functions, classes)
    
    test_cases = generator.generate_unit_tests(file_path, custom_templates=None)

    test_cases = format_check(test_cases, api_key)

    # Extract filename without extension for test file naming
    filename = os.path.splitext(os.path.basename(file_path))[0]
    test_file_name = f"{filename}_test.py"
    test_file_path = os.path.join(output_dir, test_file_name)

    if os.path.exists(test_file_path) and not overwrite:
        click.echo(f"Error: {test_file_path} already exists. Use --overwrite to overwrite.")
        return
    
    # Remove code fencing
    if test_cases.startswith("```python"):
        test_cases = test_cases[len("```python"):].strip()
    if test_cases.endswith("```"):
        test_cases = test_cases[:-len("```")].strip()
    
    # Save the test cases to a file
    with open(test_file_path, 'w') as test_file:
        test_file.write(test_cases)

    click.echo(f"Test cases generated successfully and saved to {test_file_path}.")

    # Generate additional artifacts if required
    if coverage_report:
        click.echo("Generating a coverage report... (not yet implemented)")

    if ci_integration:
        ci_config_path = os.path.join(output_dir, 'ci_config.yml')
        with open(ci_config_path, 'w') as ci_file:
            ci_file.write("# Sample CI configuration for running tests\n")
            ci_file.write("steps:\n  - run: pytest tests/")
        click.echo(f"CI configuration generated at {ci_config_path}.")

if __name__ == '__main__':
    generate_tests()