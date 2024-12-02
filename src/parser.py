import ast

class CodeParser:
    def __init__(self, code):
        self.tree = ast.parse(code)

    def get_functions(self):
        functions = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args if arg.arg != 'self']
                return_type = self._get_return_type(node)
                docstring = ast.get_docstring(node) or "No description available"
                functions.append({
                    'name': node.name,
                    'args': args,
                    'type_hints': f"{docstring} Returns: {return_type}"
                })
        return functions

    
    def get_classes(self):
        # Extract all class names and their methods.
        classes = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_type = 'instance'
                        if any(isinstance(deco, ast.Name) and deco.id == 'staticmethod' for deco in item.decorator_list):
                            method_type = 'staticmethod'
                        elif any(isinstance(deco, ast.Name) and deco.id == 'classmethod' for deco in item.decorator_list):
                            method_type = 'classmethod'

                        args = [arg.arg for arg in item.args.args if arg.arg != 'self']
                        return_type = self._get_return_type(item)
                        docstring = ast.get_docstring(item) or "No description available"
                        methods.append({
                            'name': item.name,
                            'args': args,
                            'type_hints': f"{docstring} Returns: {return_type}",
                            'method_type': method_type
                        })
                classes.append({
                    'name': node.name,
                    'methods': methods
                })
        return classes
    
    def _get_return_type(self, node):
        return getattr(node.returns, 'id', 'Any') if node.returns else 'Any'