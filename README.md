# inzva Test Case Generator

I have planned to use this generator system for all my future problems.

PRs are much appreciated!

## Files

### `main.py`

This is the main script that does all the job:

1. **Prepares the inut/output folders.** Creates folders `input` and `output` if they don't exist. Then, empties these folders (in case there weren't empty).
2. **Generates input files using the generator.** Generates the test cases by running an instance of `InputGenerator` class in `testcase_generator.py`, then writes the generated test cases into the `input` folder with the file name format `input_[test_case_no].txt`.
3. **Generates output files using `sol.cpp`.** Compiles and runs `sol.cpp` for each input file created. Here, actually the C++ program (`sol.cpp`) generates the output file.
4. **Zips the generated files.** Using `shutil`, zips `input` and `output` folders into `testcases.zip`.

### `sol.cpp`

You should write the whole solution code in `sol.cpp` as if you're trying to solve the problem.

### `sol.py`

This file is outside the flow. However, implementing the solution in Python is also considered nice practice :)

### `generator_util.py`

This file contains common utility functions such as **random number generators**, **tree generators** etc. You may use this file just to have some idea. Using the functions inside `generator_util.py` is not mandatory.

### `testcase_generator.py`

The actual stuff is done here. There are several classes inside this file:

1. `class Input`: Defines and wraps the parameters forming the input of a single test case file. Since it varies from problem to problem, you should rewrite it for each problem.
2. `class Bounds`: Since constraints generally have a lower and an upper bound, it felt more proper to wrap the bounds with a class.
3. `class Constraints`: Defines and wraps all the constraints. Its `validate` method takes in a single `Input` instance and validates it by the validation code, which you should write (I suggest `assert`). If the given `Input` instance violates the contraints, it raises `AssertionError`.
4. `class InputGenerator`: Implement all your generators with their particular generation logics inside this class. `main.py` calls its `generate` method to generate the inputs.

### `playgroung.ipynb`

I added it just for you to see how utility generator functions inside `generator_util.py` works.