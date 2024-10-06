import ast

class CodeParser:
    def __init__(self, code):
        self.code = code
        self.tree = ast.parse(code)

    def get_functions(self):
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'params': [arg.arg for arg in node.args.args]
                }
                functions.append(func_info)
        return functions

    def get_classes(self):
        # Implement class extraction similarly if needed
        classes = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                classes.append({'name': node.name})
        return classes
