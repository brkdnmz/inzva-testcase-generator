import random
from typing import List, Tuple, Union

from tqdm import tqdm

from generator_util import randint, randints


class Input:
    n: int
    a: List[int]

    def __init__(self, n: int, a: List[int]) -> None:
        self.n = n
        self.a = a


MultipleTestInput = List[Input]


class Bounds:
    lower: int
    upper: int

    def __init__(self, lower: int, upper: int) -> None:
        self.lower = lower
        self.upper = upper


class Constraints:
    n: Bounds
    elem: Bounds

    def __init__(self, n_bounds: Tuple[int, int], elem_bounds: Tuple[int, int]) -> None:
        self.n = Bounds(*n_bounds)
        self.elem = Bounds(*elem_bounds)

    def validate(self, input: Union[Input, MultipleTestInput]) -> None:
        def validate_single(input: Input) -> None:
            assert self.n.lower <= input.n <= self.n.upper
            assert input.n == len(input.a)
            assert (self.elem.lower <= x <= self.elem.upper for x in input.a)

        if type(input) == Input:
            validate_single(input)
        elif type(input) == MultipleTestInput:
            for input in input:
                validate_single(input)


class InputGenerator:
    generalConstraints = Constraints(n_bounds=(1, 2 * 10**5), elem_bounds=(-(10**9), 10**9))

    ### IMPLEMENT GENERATORS BEGIN ###

    def all_random(self) -> Input:
        constraints = self.generalConstraints
        n = randint(constraints.n.lower, constraints.n.upper)
        a = randints(n, constraints.elem.lower, constraints.elem.upper)
        input = Input(n, a)
        return self.validateAndReturn(input, constraints)

    def small_random(self) -> Input:
        constraints = Constraints(n_bounds=(1, 100), elem_bounds=(0, 100))
        n = randint(constraints.n.lower, constraints.n.upper)
        a = randints(n, constraints.elem.lower, constraints.elem.upper)
        input = Input(n, a)
        return self.validateAndReturn(input, constraints)

    def n_max(self) -> Input:
        constraints = self.generalConstraints
        n = constraints.n.upper
        a = randints(n, constraints.elem.lower, constraints.elem.upper)
        input = Input(n, a)
        return self.validateAndReturn(input, constraints)

    def all_different(self) -> Input:
        constraints = self.generalConstraints
        n = constraints.n.upper
        a = random.sample(range(constraints.elem.lower, constraints.elem.upper + 1), n)
        input = Input(n, a)
        return self.validateAndReturn(input, constraints)

    def all_same(self) -> Input:
        constraints = self.generalConstraints
        n = constraints.n.upper
        a = [randint(constraints.elem.lower, constraints.elem.upper)] * n
        input = Input(n, a)
        return self.validateAndReturn(input, constraints)

    ### IMPLEMENT GENERATORS END ###

    def generate(self) -> List[Input]:
        generators = [self.all_random, self.small_random, self.n_max, self.all_different, self.all_same]
        inputs: List[Input] = []
        print("Generating inputs...")
        for generate in tqdm(generators):
            inputs.append(generate())
        return inputs

    def validateAndReturn(self, input: Input, constraints: Constraints):
        constraints.validate(input)
        self.generalConstraints.validate(input)
        return input
