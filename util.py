import random
from typing import List, Tuple

from numba import njit

MOD = 10**9 + 7  # 998244353


def randints(n: int, lower_bound: int, upper_bound: int) -> List[int]:
    """Generates `n` random integers within `[lower_bound, upper_bound]`.

    Args:
        n (int): The number of integers to generate.
        lower_bound (int): The lower bound.
        upper_bound (int): The upper bound.

    Returns:
        List[int]: List of generated integers.
    """

    assert 0 <= n, "The number of integers to generate must be non-negative"
    assert lower_bound <= upper_bound, "Lower bound must not be greater than upper bound"

    return random.choices(range(lower_bound, upper_bound + 1), k=n)


def randint(lower_bound: int, upper_bound: int) -> int:
    """Generates a random integer within `[lower_bound, upper_bound]`.

    Args:
        lower_bound (int): The lower bound.
        upper_bound (int): The upper bound.

    Returns:
        int: A random integer within [lower_bound, upper_bound].
    """

    return randints(1, lower_bound, upper_bound)[0]


def randints_with_target_sum(n: int, target_sum: int, lower_bound: int) -> List[int]:
    """Generates `n` random integers not less than `lower_bound`, which sum up to `target_sum`.

    Args:
        n (int): The number of integers to generate.
        target_sum (int): The target sum.
        lower_bound (int): The lower bound.

    Returns:
        List[int]: List of generated integers.
    """

    assert 1 <= n, "The number of integers to generate must be positive"
    assert n * lower_bound <= target_sum, f"Unable to generate, the minimum possible sum is greater than the target sum"

    # Generated numbers will be in the form of lower_bound + x_i, where 0 <= x_i.
    # Generate x_i's, then add lower_bound to all.
    # sum(x_i) == target_sum - n * lower_bound (normalized sum)
    normalized_sum = target_sum - n * lower_bound
    prefix_sums = [0] + sorted(randints(n - 1, 0, normalized_sum)) + [normalized_sum]
    ints = [prefix_sums[i + 1] - prefix_sums[i] + lower_bound for i in range(n)]

    assert sum(ints) == target_sum

    return ints


def numbers_with_max_number_of_divisors(limit: int) -> List[int]:
    """Given an upper bound `limit`, finds all positive integers not exceeding `limit` and having the maximum number of divisors. `limit` must not exceed `10**12`.

    Args:
        limit (int): The upper bound.

    Returns:
        List[int]: The positive integers having the maximum number of divisors.
    """

    assert 1 <= limit <= 10**12, "`limit` must be within [1, 10**12]"

    # List of smallest primes (numbers to be found won't be divisible by a greater prime).
    p = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    # Keeps the record of the maximum number of divisors found so far.
    max_number_of_divisors = 0

    # The numbers to be found will be stored in this.
    target_numbers: List[int] = []

    # The recursive function for finding the numbers. This does all the work.
    def helper(num: int, p_i: int, cnt: int) -> None:
        nonlocal target_numbers, max_number_of_divisors, limit
        if cnt > max_number_of_divisors:
            max_number_of_divisors = cnt
            target_numbers = [num]
        elif cnt == max_number_of_divisors:
            target_numbers.append(num)
        if p_i == len(p):
            return
        pw = 1
        while num * p[p_i] ** pw <= limit:
            helper(num * p[p_i] ** pw, p_i + 1, cnt * (pw + 1))
            pw += 1

    helper(1, 0, 1)

    return target_numbers


@njit
def is_prime(num: int) -> bool:
    """Checks whether given integer is a prime.

    Args:
        num (int): The integer to check whether it's a prime.

    Returns:
        bool: `true` if `num` is a prime, otherwise `false`.
    """

    assert num >= 0, "`num` should not be negative"

    if num <= 1:
        return False

    for i in range(2, num + 1):
        if i * i > num:
            break
        if num % i == 0:
            return False
    return True


@njit
def prev_prime(n: int) -> int:
    """Returns the largest prime less than the given integer.

    Args:
        n (int): The given integer. Must be at least 3.

    Returns:
        int: Largest `p` such that `p < n` and `p` is a prime.
    """

    assert n > 2, "Given integer must be strictly larger than 2"

    n -= 1
    while not is_prime(n):
        n -= 1
    return n


@njit
def next_prime(n: int) -> int:
    """Returns the smallest prime greater than the given integer.

    Args:
        n (int): The given integer.

    Returns:
        int: Smallest `p` such that `p > n` and `p` is a prime.
    """

    n += 1
    while not is_prime(n):
        n += 1
    return n


def gen_tree(n: int, parent_dist: int = 10**9, root: int = 1) -> List[Tuple[int, int]]:
    """Generates a tree with `n` nodes. Returns the bidirectional edges forming the tree.

    Args:
        n (int): The number of nodes. The nodes are numbered `1...n`.
        parent_dist (int, optional): Each node's parent will be added to the tree at most `parent_dist` nodes before itself. Defaults to `10**9`.
        root (int, optional): The root node's number. Defaults to `1`.
    Returns:
        List[Tuple[int, int]]: `n - 1` bidirectional edges, each represented with two node numbers `u` and `v` which are connected by that edge.
    """

    assert 1 <= n, "There must be at least 1 node"
    assert 0 <= parent_dist, "`parent_dist` must be positive"
    assert 1 <= root <= n, "The root's number must be within [1, n]"

    nodes = list(range(1, n + 1))
    nodes.remove(root)
    random.shuffle(nodes)
    nodes.insert(0, root)
    edges: List[Tuple[int, int]] = []
    for node_index, node in enumerate(nodes):
        # Ignore the root
        if not node_index:
            continue
        parent_index = random.choice(range(max(0, node_index - parent_dist), node_index))
        parent = nodes[parent_index]
        u, v = node, parent
        if randint(0, 1):
            u, v = v, u
        edges.append((u, v))
    random.shuffle(edges)
    return edges


def gen_chain_tree(n: int, root: int = 1) -> List[Tuple[int, int]]:
    """Generates a tree rooted at node `1`, where each non-leaf node has exactly 1 child.

    Args:
        n (int): The number of nodes. The nodes are numbered `1...n`.

    Returns:
        List[Tuple[int, int]]: `n - 1` bidirectional edges, each represented with two node numbers `u` and `v` which are connected by that edge.
    """

    return gen_tree(n, 1, root)


def gen_blossom_tree(n: int, root: int = 1) -> List[Tuple[int, int]]:
    """Generates a tree rooted at node `1`, where each node except the root is a leaf node.

    Args:
        n (int): The number of nodes. The nodes are numbered `1...n`.

    Returns:
        List[Tuple[int, int]]: `n - 1` bidirectional edges, each represented with two node numbers `u` and `v` which are connected by that edge.
    """

    assert 1 <= n, "There must be at least 1 node"
    assert 1 <= root <= n, "The root's number must be within [1, n]"

    nodes = list(range(1, n + 1))
    nodes.remove(root)
    random.shuffle(nodes)
    edges: List[Tuple[int, int]] = []
    for node in nodes:
        u, v = node, root
        if randint(0, 1):
            u, v = v, u
        edges.append((u, v))
    return edges


def gen_random_tree(n: int) -> List[Tuple[int, int]]:
    """An exemplary random tree generator. Change the parameters however you want.

    Args:
        n (int): The number of nodes.

    Returns:
        List[Tuple[int, int]]: The list of edges.
    """

    pick = random.random()
    if pick <= 0.2:
        return gen_chain_tree(n)
    elif pick <= 0.4:
        return gen_blossom_tree(n)
    elif pick <= 0.6:
        return gen_tree(n, 5)
    elif pick <= 0.7:
        return gen_tree(n, 10)
    elif pick <= 0.8:
        return gen_tree(n, 100)
    elif pick <= 0.9:
        return gen_tree(n, 1000)
    else:
        return gen_tree(n, n)
