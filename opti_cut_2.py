#!/usr/bin/python3

from math import factorial
import numpy as np


def subset_sum(n, k, target, memo=None):
    """
    Computes (and returns) the number of possibilities
    of taking k different integers between 1 and n who sum
    up to target.
    """
    if memo is None:
        return subset_sum(n, k, target,
                          [[[-1 for _ in range(target + 1)]
                            for _ in range(k + 1)] for _ in range(n + 1)])
    if k == 0:
        return int(target == 0)
    elif target <= 0 or n == 0:
        return 0
    if memo[n][k][target] == -1:
        memo[n][k][target] = (
            subset_sum(n - 1, k - 1, target - n, memo) +
            subset_sum(n - 1, k, target, memo))
    return memo[n][k][target]


def bobs_expected_utility(n, k, memo=None):
    """
    Computes (and returns) the expected utility for Bob, assuming
    that there are n objects, and Alice picks the first k ones.
    """
    total_utility = int(n * (n + 1) / 2)
    min_picked = int(k * (k + 1) / 2)
    max_picked = total_utility - int((n - k) * (n - k + 1) / 2)
    return sum((total_utility - picked) * subset_sum(n, k, picked, memo)
               for picked in range(min_picked, max_picked + 1)) * factorial(k) * factorial(n - k) / factorial(n)


def optimal_cut(n):
    """
    Computes (and returns) the optimal cut for n object. In other words,
    this number is the integer k that guarantees the best egalitarian expected
    utility for Alice and Bob if Alice picks the first k items and Bob the n-k
    remaining ones.
    """
    total_utility = int(n * (n + 1) / 2)
    last_min = 0
    memo = -np.ones((n + 1, total_utility + 1, total_utility + 1), dtype=np.float)
    for k in range(1, n + 1):
        alice = total_utility - int((n - k) * (n - k + 1) / 2)
        bob = bobs_expected_utility(n, k, memo)
        if alice > bob:
            if last_min > min(alice, bob):
                k--
                alice = total_utility - int((n - k) * (n - k + 1) / 2)
                bob = bobs_expected_utility(n, k, memo)
            return (k , alice, bob)
        last_min = min(alice, bob)
    assert False, "We shouldn't be here..."
    return


print(optimal_cut(60))
