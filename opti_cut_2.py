#!/usr/bin/python3

from math import factorial
import numpy as np
import matplotlib.pyplot as plt
import copy


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

        
def optimal_egalitarian_cut(n):
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
                k-=1
                alice = total_utility - int((n - k) * (n - k + 1) / 2)
                bob = bobs_expected_utility(n, k, memo)
            return (k , alice, bob)
        last_min = min(alice, bob)
    assert False, "We shouldn't be here..."
    return


def optimal_utilitarian_cut(n):
    total_utility = int(n * (n + 1) / 2)
    memo = -np.ones((n + 1, total_utility + 1, total_utility + 1), dtype=np.float)
    sum_utility_max = int(n * (n + 1) / 2) # k = 0
    argmax = 0
    alice_max = total_utility
    bob_max = 0
    for k in range(1, n+1):
        alice = total_utility - int((n - k) * (n - k + 1) / 2)
        bob = bobs_expected_utility(n, k, memo)
        sum_utility = alice + bob
        if sum_utility > sum_utility_max:
            sum_utility_max = sum_utility
            argmax = k
            bob_max = bob
            alice_max = alice
    return (argmax,alice_max,bob_max)


def optimal_nash_cut(n):
    total_utility = int(n * (n + 1) / 2)
    memo = -np.ones((n + 1, total_utility + 1, total_utility + 1), dtype=np.float)
    prod_utility_max = int(n * (n + 1) / 2) # k = 0
    argmax = 0
    alice_max = total_utility
    bob_max = 0
    for k in range(1, n+1):
        alice = total_utility - int((n - k) * (n - k + 1) / 2)
        bob = bobs_expected_utility(n, k, memo)
        prod_utility = alice * bob
        if prod_utility > prod_utility_max:
            prod_utility_max = prod_utility
            argmax = k
            bob_max = bob
            alice_max = alice
    return (argmax,alice_max,bob_max)       


#####
"""
Au lieu de mettre les 3 je pourrai mettre F la fct d'aggreg en param puis faire F(x1,x2) à chaque fois ( en faire ne marche pas pour * )
"""
#####

def test(n):
    u,e,n = optimal_utilitarian_cut(n),optimal_egalitarian_cut(n),optimal_nash_cut(n)
    print(u,e,n)
    return (u,e,n)

def ploting(n):
    U = []
    E = []
    N = []
    X = []
    for i in range(1,n):
        U.append(optimal_utilitarian_cut(i)[0])
        E.append(optimal_egalitarian_cut(i)[0])
        N.append(optimal_nash_cut(i)[0])
        X.append(i)
    plt.plot(X,U)
    plt.plot(X,E)
    plt.plot(X,N)
    plt.show()

def ploting2(n):
    A = []
    B = []
    X = []
    for i in range(1,n):
        o = optimal_egalitarian_cut(i)
        A.append(o[1])
        B.append(o[2])
        X.append(i)
    plt.plot(X,A, color = 'r')
    plt.plot(X,B)
    plt.show()

def ploting3(n):
    A = []
    B = []
    X = []
    for i in range(2,n):
        o = optimal_egalitarian_cut(i)
        A.append(o[0]/i)
        X.append(i)
    plt.plot(X,A, color = 'r')
    plt.show()


def opti(n,m):
    T = np.zeros((m+1,n+1,m+1,2)) # T[m][n] pour m agents et n objets renvoit un tableau t tq t[0][1] = social_welfare, t[i][0] = le nombre d'objets select par les i premiers agent (ie endroit de la ième coupe), t[i][1] = U(i)
    total_utility = int(n * (n + 1) / 2)
    for i in range(1,n+1):
        oeci = optimal_egalitarian_cut(i)
        T[2][i][1][1] = oeci[1]
        T[2][i][2][1] = oeci[2]
        T[2][i][1][0] = oeci[0]
        T[2][i][2][0] = i
        T[2][i][0][1] = min(oeci[1],oeci[2])
    for nb_agent in range(3,m+1):
        for nb_objet in range(1,n+1):
            
            #total_utility = int(nb_objet * (nb_objet + 1) / 2)
            social_welfare_max = 0
            Ulast_max = 0
            argmax = 0
            for nb_objet_last in range(1,nb_objet):
                #print(T[m-1,nb_objet - nb_objet_last,0,1])
                memo =  -np.ones((n + 1, total_utility + 1, total_utility + 1), dtype=np.float)
                Ulast = bobs_expected_utility(nb_objet,nb_objet - nb_objet_last,memo)
                partiel = copy.deepcopy(T[nb_agent-1,nb_objet - nb_objet_last])
                partiel[1][1] += partiel[1][0] * nb_objet_last #il faut ajouter le fait que chaque objet prit par les i premiers participants ont en fait une valeur += "le nombre d'objets laissé au dernier" 
                social_welfare = partiel[1][1]
                for i in range(2,nb_agent): 
                    partiel[i][1] +=  (partiel[i][0] - partiel[i-1][0] ) * nb_objet_last
                    social_welfare = min(social_welfare,partiel[i][1])
                    
                    
                social_welfare = min( Ulast, social_welfare)

                if social_welfare > social_welfare_max:
                    social_welfare_max = social_welfare
                    argmax = nb_objet - nb_objet_last
                    T[nb_agent][nb_objet] = partiel
                    T[nb_agent][nb_objet][0][1] = social_welfare_max
                    T[nb_agent][nb_objet][nb_agent][1] = Ulast
                #if Ulast > T[m-1,nb_objet - nb_objet_last,0,1]:   # car U(last) croissant strict et un des autres décroit strict aussi
                 #   break
            
            T[nb_agent][nb_objet][nb_agent][0] = nb_objet
    #print(T)
    return T[m,n]

# ok j'ai toruvé pb, le vecteur de borda est emputé des derniers el et donc les U perdent de la veleur

# print(opti(20,5))


def opti_mat(n,m):
    T = np.zeros((m+1,n+1,m+1,2)) # T[m][n] pour m agents et n objets renvoit un tableau t tq t[0][1] = social_welfare, t[i][0] = le nombre d'objets select par les i premiers agent (ie endroit de la ième coupe), t[i][1] = U(i)
    total_utility = int(n * (n + 1) / 2)
    for i in range(1,n+1):
        oeci = optimal_egalitarian_cut(i)
        T[2][i][1][1] = oeci[1]
        T[2][i][2][1] = oeci[2]
        T[2][i][1][0] = oeci[0]
        T[2][i][2][0] = i
        T[2][i][0][1] = min(oeci[1],oeci[2])
    for nb_agent in range(3,m+1):
        for nb_objet in range(1,n+1):
            
            #total_utility = int(nb_objet * (nb_objet + 1) / 2)
            social_welfare_max = 0
            Ulast_max = 0
            argmax = 0
            for nb_objet_last in range(1,nb_objet):
                #print(T[m-1,nb_objet - nb_objet_last,0,1])
                memo =  -np.ones((n + 1, total_utility + 1, total_utility + 1), dtype=np.float)
                Ulast = bobs_expected_utility(nb_objet,nb_objet - nb_objet_last,memo)
                partiel = copy.deepcopy(T[nb_agent-1,nb_objet - nb_objet_last])
                partiel[1][1] += partiel[1][0] * nb_objet_last #il faut ajouter le fait que chaque objet prit par les i premiers participants ont en fait une valeur += "le nombre d'objets laissé au dernier" 
                social_welfare = partiel[1][1]
                for i in range(2,nb_agent): 
                    partiel[i][1] +=  (partiel[i][0] - partiel[i-1][0] ) * nb_objet_last
                    social_welfare = min(social_welfare,partiel[i][1])
                    
                    
                social_welfare = min( Ulast, social_welfare)

                if social_welfare > social_welfare_max:
                    social_welfare_max = social_welfare
                    argmax = nb_objet - nb_objet_last
                    T[nb_agent][nb_objet] = partiel
                    T[nb_agent][nb_objet][0][1] = social_welfare_max
                    T[nb_agent][nb_objet][nb_agent][1] = Ulast
                #if Ulast > T[m-1,nb_objet - nb_objet_last,0,1]:   # car U(last) croissant strict et un des autres décroit strict aussi
                 #   break
            
            T[nb_agent][nb_objet][nb_agent][0] = nb_objet
    #print(T)
    return T

import matplotlib.cm as cm

def plot_opti_n(n,m):
    Y = opti_mat(n,m)
    X = [i for i in range(n+1)]
    for i in range(1,m+1):
        plt.plot(X,Y[m,:,i,1],color=cm.cool(i/m))
    plt.show()
    print(T[m,n])

#print(opti(4,3))

#incrémentale
print(optimal_egalitarian_cut(50))
