#!/usr/bin/python3

from math import factorial
import numpy as np
import matplotlib.pyplot as plt
import copy


# J'ai l'impression que boucler dans l'autre sens i.e dans le sens décroissant on aura moins de branches possible car de plus nombreuses fois on pourra cesser la recherche plus tôt car V[n] trop grand
def subset_sum(n, k, target, V, memo=None):
    """
    Computes (and returns) the number of possibilities
    of taking k different integers between 1 and n who sum
    up to target.
    """
    if memo is None:
        return subset_sum(n, k, target,V,
                          [[[-1 for _ in range(target + 1)]
                            for _ in range(k + 1)] for _ in range(n + 1)])
    if k == 0:
        return int(target == 0)
    elif target <= 0 or n == 0: #target <= V[n] or n == 0:
        return 0
    if memo[n][k][target] == -1:
        memo[n][k][target] = (
            subset_sum(n - 1, k - 1, target - V[n],V, memo) +
            subset_sum(n - 1, k, target,V, memo))
    return memo[n][k][target]


def bobs_expected_utility(n, k, V , memo=None):
    """
    Computes (and returns) the expected utility for Bob, assuming
    that there are n objects pickable, and Alice picks the first k ones.
    V is the scoring vector of the M objects (1 to M) which is the total number of objects
    """
    total_utility = sum( V[i]  for i in range(1,n+1))
    min_picked = total_utility - sum( V[i]  for i in range(1,k+1))
    max_picked = total_utility - sum( V[i]  for i in range(n-k+1,n+1))
    
    return (sum(picked * subset_sum(n, k, total_utility - picked,V, memo)
               for picked in range(min_picked, max_picked + 1)) * factorial(k) * factorial(n - k)) / factorial(n)

        
def optimal_egalitarian_cut(n,V):
    """
    Computes (and returns) the optimal cut for n object. In other words,
    this number is the integer k that guarantees the best egalitarian expected
    utility for Alice and Bob if Alice picks the first k items and Bob the n-k
    remaining ones.
    """
    total_utility = sum( V[i]  for i in range(1,n+1))
    last_min = 0
    memo = -np.ones((n + 1, total_utility + 1, total_utility + 1), dtype=np.float)
    for k in range(1, n + 1):
        alice = total_utility - sum( V[i] for i in range(k+1,n+1))
        bob = bobs_expected_utility(n, k, V, memo)
        print(k, alice,bob)
        if alice > bob:
            if last_min > min(alice, bob):
                k-=1
                alice = total_utility - sum( V[i] for i in range(k+1,n+1))
                bob = bobs_expected_utility(n, k, V, memo)
            return (k , alice, bob)
        last_min = min(alice, bob)
    assert False, "We shouldn't be here..."
    return


def Borda(n):
    return [0] + [ n - i + 1 for i in range(1,n+1)] # le premier element ne sert à rien

print(optimal_egalitarian_cut(50,Borda(50)))

