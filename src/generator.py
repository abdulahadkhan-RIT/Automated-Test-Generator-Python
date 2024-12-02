import os
import openai

class TestCaseGenerator:
    def __init__(self, functions, classes):
        self.functions = functions
        self.classes = classes

    def generate_imports(self, file_path):
        """Generate import statements for the functions being tested."""
        import_statements = []        
        module_name = os.path.splitext(os.path.basename(file_path))[0]  # 'add_subtract'
        import_statements.append(f"from codeFiles.{module_name} import " + ', '.join([func['name'] for func in self.functions]))
        
        return "\n".join(import_statements)
    
    def generate_test_header(self):
        return (
            "import pytest\n\n"
            "# Auto-generated test cases\n"
            "# Modify values and assertions to align with actual function behavior\n"
        )

    def generate_unit_tests(self, file_path, custom_templates=None):
        test_cases = [self.generate_test_header(), self.generate_imports(file_path), ""]
                
        for function in self.functions:
            func_name = function['name']
            params = function['args']
            type_hints = function.get('type_hints', 'No description available')

            test_cases.append(f"def test_{func_name}():")
            test_cases.append(f"    \"\"\"{type_hints}\"\"\"")
            example_args = ", ".join(f"'{param}_example'" for param in params) if params else ""
            test_cases.append(f"    # TODO: Replace placeholders with actual values")
            test_cases.append(f"    assert {func_name}({example_args}) == 'expected_value'")
            test_cases.append("")
        
        # Add class-based tests if necessary
        for cls in self.classes:
            class_name = cls['name']
            test_cases.append(f"def test_{class_name}():")
            test_cases.append(f"    instance = {class_name}()")
            test_cases.append(f"    assert instance is not None")
            test_cases.append("    assert instance is not None")
            
        return "\n".join(test_cases)

class ChatGPTTestCaseGenerator(TestCaseGenerator):
    def __init__(self, functions, classes, framework, api_key):
        super().__init__(functions, classes)
        self.framework = framework
        self.api_key = api_key

    def generate_test_case_using_chatgpt(self, function):
        prompt = f"""
        Write 3 testcases for the following Python function: 
        1) General test
        2) Boundary values
        3) Edge case
        Do this using {self.framework}:
        {function}

        Ensure proper formatting and syntax.
        """

        openai.api_key = self.api_key
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=150
        )

        return response.choices[0].message.content.strip()

    def generate_unit_tests(self, file_path, custom_templates=None):
        test_cases = [self.generate_test_header(), self.generate_imports(file_path), ""]

        # Group functions by file
        functions_by_file = {}

        for function in self.functions:
            # Default to "unknown_file" if 'file' key is missing
            file_name = function.get('file', 'unknown_file')  
            if file_name not in functions_by_file:
                functions_by_file[file_name] = []
            functions_by_file[file_name].append(function)

        # Generate tests for each file
        for file_name, file_functions in functions_by_file.items():
            test_cases.append(f"\n# Tests for {file_name} functions\n")
            for function in file_functions:
                func_name = function['name']
                function_code = f"def {func_name}({', '.join(function['args'])}): pass"

                # Generate test case using ChatGPT
                test_case = self.generate_test_case_using_chatgpt(function_code)
                test_cases.append(f"def test_{func_name}():\n    {test_case}\n")

        return "\n".join(test_cases)
