import ast

class CodeParser:
    def __init__(self, code):
        self.tree = ast.parse(code)

    # Extract all function names and their arguments.
    def get_functions(self):
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                functions.append({
                    'name': node.name,
                    'args': args
                })
        return functions

    # Extract all class names and their methods.
    def get_classes(self):
        classes = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                classes.append({
                    'name': node.name,
                    'methods': methods
                })
        return classes
