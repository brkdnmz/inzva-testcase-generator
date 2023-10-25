import random
from typing import List

from tqdm import tqdm

from generator_util import randint, randints

""" 
    Sample Problem

    Given an array a of n integers, print for each position the number of distinct elements up to
    that position.

    Constraints:
    - 1 <= n <= 2 * 10**5
    - |a_i| <= 10**9
"""


# This class wraps the input parameters.
# Note that parameters vary problem to problem.
# You must manually customize the class!
class Input:
    n: int  # The number of elements
    a: List[int]  # The array

    def __init__(self, n: int, a: List[int]) -> None:
        self.n = n
        self.a = a


# Most constraints are usually in the following form:
#   - 1 <= n <= 2 * 10^5
# Here, 1 is the lower bound and 2 * 10^5 is the upper bound.
# So, this `Bounds` class helps wrapping the bounds in a proper way.
class Bounds:
    lower: int
    upper: int

    def __init__(self, lower: int, upper: int) -> None:
        self.lower = lower
        self.upper = upper


# This class will help us using proper parameters when generating random numbers.
# Also, it can validate a custom input -- whether it satisfies the constraints.
class Constraints:
    # You must check for each constraint given in the problem statement.
    # So, declare the necessary constraints here.
    # Of course, name them as you prefer!
    n_bounds: Bounds
    elem_bounds: Bounds

    def __init__(self, n_bounds: Bounds, elem_bounds: Bounds) -> None:
        self.n_bounds = n_bounds
        self.elem_bounds = elem_bounds

    # This method will be used to validate inputs.
    def validate(self, input: Input) -> None:
        assert self.n_bounds.lower <= input.n <= self.n_bounds.upper
        assert input.n == len(input.a)
        assert (self.elem_bounds.lower <= x <= self.elem_bounds.upper for x in input.a)


# Implement your various input generator algorithms inside this class.
class InputGenerator:
    # Here, you can define your constraints.
    # You may also choose to define specific constraint per each generator.
    generalConstraints = Constraints(n_bounds=Bounds(1, 2 * 10**5), elem_bounds=Bounds(-(10**9), 10**9))
    # smallConstraints = Constraints(n_bounds=Bounds(1, 100), elem_bounds=Bounds(-100, 100))
    # midConstraints = Constraints(n_bounds=Bounds(10**2 + 1, 10**5), elem_bounds=Bounds(-100, 100))
    # ...

    ### IMPLEMENT GENERATORS BEGIN ###

    def all_random(self) -> Input:
        constraints = self.generalConstraints
        n = randint(constraints.n_bounds.lower, constraints.n_bounds.upper)
        a = randints(n, constraints.elem_bounds.lower, constraints.elem_bounds.upper)
        input = Input(n, a)
        return self.validateAndReturn(input, constraints)

    def small_random(self) -> Input:
        constraints = Constraints(n_bounds=Bounds(1, 100), elem_bounds=Bounds(0, 100))
        n = randint(constraints.n_bounds.lower, constraints.n_bounds.upper)
        a = randints(n, constraints.elem_bounds.lower, constraints.elem_bounds.upper)
        input = Input(n, a)
        return self.validateAndReturn(input, constraints)

    def n_max(self) -> Input:
        constraints = self.generalConstraints
        n = constraints.n_bounds.upper
        a = randints(n, constraints.elem_bounds.lower, constraints.elem_bounds.upper)
        input = Input(n, a)
        return self.validateAndReturn(input, constraints)

    def all_different(self) -> Input:
        constraints = self.generalConstraints
        n = constraints.n_bounds.upper
        a = random.sample(range(constraints.elem_bounds.lower, constraints.elem_bounds.upper + 1), n)
        input = Input(n, a)
        return self.validateAndReturn(input, constraints)

    def all_same(self) -> Input:
        constraints = self.generalConstraints
        n = constraints.n_bounds.upper
        a = [randint(constraints.elem_bounds.lower, constraints.elem_bounds.upper)] * n
        input = Input(n, a)
        return self.validateAndReturn(input, constraints)

    # And so on...

    ### IMPLEMENT GENERATORS END ###

    # You should only call this method of the InputGenerator object.
    def generate(self) -> List[Input]:
        generators = (self.all_random, self.small_random, self.n_max, self.all_different, self.all_same)
        inputs: List[Input] = []
        print("Generating inputs...")
        for generate in tqdm(generators):
            inputs.append(generate())
        return inputs

    # Each generator should return by calling this method.
    def validateAndReturn(self, input: Input, constraints: Constraints):
        constraints.validate(input)
        self.generalConstraints.validate(input)  # Any input must satisfy the general constraints.
        return input
