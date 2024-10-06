# Automated-Test-Generator-Python

Steps to run the program:

1) Creat a virtual enviroment
    - python -m venv venv

2) Activate the virtual environment:
    For Windows:
    - venv\Scripts\activate
    For macOS/Linux:
    - source venv/bin/activate

3) Install the required packages:
    - pip install -r requirements.txt

4) Run the generator by executing the cli.py script:
    > Navigate to src folder:
        - cd src
    Then run,
    - python -m cli codeFiles/file_name.py

5) Run the test file:
    > From the root directory:
        - cd ..
    Then run,
    - pytest src/tests/testfile_name.py