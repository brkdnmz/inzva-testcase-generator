import random
from typing import List

from tqdm import tqdm

from util import randint, randints


class Input:
    def __init__(self, n: int, a: List[int]) -> None:
        self.n = n
        self.a = a


MultipleTestInput = List[Input]


class InputGenerator:

    ### IMPLEMENT GENERATORS BEGIN ###

    def all_random(self) -> Input:
        n = randint(1, 2 * 10**5)
        a = randints(n, -(10**9), 10**9)
        return Input(n, a)

    def small_random(self) -> Input:
        n = randint(1, 100)
        a = randints(n, 0, 100)
        return Input(n, a)

    def n_max(self) -> Input:
        n = 2 * 10**5
        a = randints(n, -(10**9), 10**9)
        return Input(n, a)

    def all_different(self) -> Input:
        n = 2 * 10**5
        a = random.sample(range(-(10**9), 10**9 + 1), n)
        return Input(n, a)

    def all_same(self) -> Input:
        n = 2 * 10**5
        a = [randint(-(10**9), 10**9)] * n
        return Input(n, a)

    ### IMPLEMENT GENERATORS END ###

    def generate(self) -> List[Input]:
        generators = []
        for _ in range(5):
            generators.append(self.all_random)
        for _ in range(5):
            generators.append(self.small_random)
        for _ in range(5):
            generators.append(self.n_max)
        for _ in range(5):
            generators.append(self.all_different)
        for _ in range(5):
            generators.append(self.all_same)

        print("Generating inputs...")
        inputs: List[Input] = []
        for generate in tqdm(generators):
            inputs.append(generate())
        return inputs
