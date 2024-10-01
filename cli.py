import argparse
import ast

def parse_functions(code: str):
    """
    Parse the Python code and return a list of function definitions.
    
    Args:
        code (str): The Python source code as a string.
    
    Returns:
        List[Dict]: A list of dictionaries where each dictionary contains
                    information about a function (name, arguments).
    """
    tree = ast.parse(code)
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_info = {
                'name': node.name,
                'args': [arg.arg for arg in node.args.args],
            }
            functions.append(func_info)
    
    return functions

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Python File Analyzer CLI Tool")

    # Add the filename argument
    parser.add_argument('filename', type=str, help='The Python file to analyze')

    # Parse the arguments
    args = parser.parse_args()

    # Read the content of the file
    try:
        with open(args.filename, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    # Parse functions in the code
    functions = parse_functions(code)

    # Print the function definitions found in the file
    if functions:
        print("Functions found in the file:")
        for func in functions:
            print(f"Name: {func['name']}, Arguments: {', '.join(func['args'])}")
    else:
        print("No functions found in the file.")

if __name__ == "__main__":
    main()
