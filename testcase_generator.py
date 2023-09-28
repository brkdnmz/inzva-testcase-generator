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


# This class will help us using proper parameters when generating random numbers.
# Also, it can validate a custom input -- whether it satisfies the constraints.
class Constraints:
    # You must check for each constraint given in the problem statement.
    # So, declare the necessary constraints here.
    # Of course, name them as you prefer!
    N_LOWER: int
    N_UPPER: int
    ELEM_LOWER: int
    ELEM_UPPER: int

    def __init__(self, n_lower: int, n_upper: int, elem_lower: int, elem_upper: int) -> None:
        self.N_LOWER = n_lower
        self.N_UPPER = n_upper
        self.ELEM_LOWER = elem_lower
        self.ELEM_UPPER = elem_upper

    # This method will be used to validate inputs.
    def validate(self, input: Input) -> None:
        assert self.N_LOWER <= input.n <= self.N_UPPER
        assert input.n == len(input.a)
        assert (self.ELEM_LOWER <= x <= self.ELEM_UPPER for x in input.a)


# Implement your various input generator algorithms inside this class.
class InputGenerator:
    # Here, you can define your constraints.
    # You may also choose to define specific constraint per each generator.
    generalConstraints = Constraints(n_lower=1, n_upper=2 * 10**5, elem_lower=-(10**9), elem_upper=10**9)
    # smallConstraints = Constraints(n_lower=1, n_upper=100, elem_lower=-100, elem_upper=100)
    # midConstraints = Constraints(n_lower=10**2 + 1, n_upper=10**5, elem_lower=-100, elem_upper=100)
    # ...

    ### IMPLEMENT GENERATORS BEGIN ###

    def all_random(self) -> Input:
        constraints = self.generalConstraints
        n = randint(constraints.N_LOWER, constraints.N_UPPER)
        a = randints(n, constraints.ELEM_LOWER, constraints.ELEM_UPPER)
        input = Input(n, a)
        return self.validateAndReturn(input, constraints)

    def small_random(self) -> Input:
        constraints = Constraints(n_lower=1, n_upper=100, elem_lower=0, elem_upper=100)
        n = randint(constraints.N_LOWER, constraints.N_UPPER)
        a = randints(n, constraints.ELEM_LOWER, constraints.ELEM_UPPER)
        input = Input(n, a)
        return self.validateAndReturn(input, constraints)

    def n_max(self) -> Input:
        constraints = self.generalConstraints
        n = constraints.N_UPPER
        a = randints(n, constraints.ELEM_LOWER, constraints.ELEM_UPPER)
        input = Input(n, a)
        return self.validateAndReturn(input, constraints)

    def all_different(self) -> Input:
        constraints = self.generalConstraints
        n = constraints.N_UPPER
        a = random.sample(range(constraints.ELEM_LOWER, constraints.ELEM_UPPER), n)
        input = Input(n, a)
        return self.validateAndReturn(input, constraints)

    def all_same(self) -> Input:
        constraints = self.generalConstraints
        n = constraints.N_UPPER
        a = [randint(constraints.ELEM_LOWER, constraints.ELEM_UPPER)] * n
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
