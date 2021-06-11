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
        #print(k, alice,bob)
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

def Lexico(n):
    return [0]+ [2**(n-i) for i in range(1,n+1)]
#print(optimal_egalitarian_cut(50,Borda(50)))


def gen_egal(n,m,V):
    T = np.zeros((m+1,n+1,m+1,2)) # T[m][n] pour m agents et n objets renvoit un tableau t tq t[0][1] = social_welfare, t[i][0] = le nombre d'objets select par les i premiers agent (ie endroit de la ième coupe), t[i][1] = U(i)
    total_utility = sum( V[i]  for i in range(1,n+1))
    for i in range(1,n+1):
        oeci = optimal_egalitarian_cut(i,V)
        T[2][i][1][1] = oeci[1]
        T[2][i][2][1] = oeci[2]
        T[2][i][1][0] = oeci[0]
        T[2][i][2][0] = i
        T[2][i][0][1] = min(oeci[1],oeci[2])
    for nb_agent in range(3,m+1):
        for nb_objet in range(1,n+1):
            
            for nb_objet_last in range(1,nb_objet):
                #print(T[m-1,nb_objet - nb_objet_last,0,1])
                memo =  -np.ones((n + 1, total_utility + 1, total_utility + 1), dtype=np.float)
                Ulast = bobs_expected_utility(nb_objet,nb_objet - nb_objet_last,V,memo)
                
                if Ulast > T[nb_agent-1,nb_objet - nb_objet_last,0,1]:   # car U(last) croissant strict et un des autres décroit strict aussi
                    U_before = bobs_expected_utility(nb_objet,nb_objet - nb_objet_last +1,V,memo)
                    if T[nb_agent-1,nb_objet - nb_objet_last,0,1] < min(U_before,T[nb_agent-1,nb_objet - nb_objet_last +1,0,1]):
                        nb_objet_last -= 1
                        Ulast = U_before
                    social_welfare = min( Ulast, T[nb_agent-1,nb_objet - nb_objet_last][0][1])
                    T[nb_agent][nb_objet] = copy.deepcopy(T[nb_agent-1,nb_objet - nb_objet_last])
                    T[nb_agent][nb_objet][0][1] = social_welfare
                    T[nb_agent][nb_objet][nb_agent][1] = Ulast
                    T[nb_agent][nb_objet][nb_agent][0] = nb_objet
                    break
                
            
    #print(T)
    return T[m,n]

#print(gen_egal(20,3,Lexico(20)))
print(gen_egal(50,7,Borda(50)))
