import functools
import numpy as np

np.random.seed(41)

def factorial(n):
    return functools.reduce((lambda x,y: x*y), range(1, n+1))

def perm_given_index(alist, apermindex):
    alist = alist[:]
    for i in range(len(alist)-1):
        apermindex, j = divmod(apermindex, len(alist)-i)
        alist[i], alist[i+j] = alist[i+j], alist[i]
    return alist

# https://stackoverflow.com/questions/5602488/random-picks-from-permutation-generator
# This code generate a random profil amoung the (m!)^(n-1) to test the code bellow
def generate_preference_profiles(n, m): 
    base_profile = list(range(1, m + 1))
    preference_profiles = [base_profile]
    fact = factorial(len(base_profile))

    for _ in range(n - 1):
        i = np.random.randint(0,fact)
        preference_profiles.append(perm_given_index(base_profile,i))
    
    
    return preference_profiles

n = 5
m = 10
profiles = generate_preference_profiles(n, m)
print(profiles)


def allocate_objects(policy, profiles):
    """
    Given a policy and profiles this function allocate objects to agents
    """
    allocation = []
    available_objects = set(range(1, len(profiles[0]) + 1))

    for i, k in enumerate(policy):
        agent_profile = profiles[i]
        agent_allocation = []

        for obj in agent_profile:
            if len(agent_allocation) < k and obj in available_objects:
                agent_allocation.append(obj)
                available_objects.remove(obj)

        allocation.append(agent_allocation)
    
    return allocation

# https://stackoverflow.com/questions/58915599/generate-restricted-weak-integer-compositions-or-partitions-of-an-integer-n-in
def generate_policy(n, m):
    def helper(remaining_objects, agents_left, current_policy):
        if agents_left == 0:
            if remaining_objects == 0:
                yield current_policy
        elif agents_left == 1:
            if 0 <= remaining_objects <= m:
                yield current_policy + (remaining_objects,)
        elif 0 <= remaining_objects <= m * agents_left:
            for v in range(m, -1, -1):
                yield from helper(remaining_objects - v, agents_left - 1, current_policy + (v,))
    
    return helper(m, n, ())

policy = next(generate_policy(n,m))

allocation = allocate_objects(policy, profiles)
print(allocation)


# Peut être implémenter cela avec un vecteur numpy et faire un dot product serait plus rapide (mais le temps n'est pas perdu ici)
def compute_utility(profile, allocation, score_vector):
    """
    Compute the utility of an agent given her allocation, preference and scoring vector 
    """
    utility = 0
    for obj in allocation:
        rank = profile.index(obj) + 1
        utility += score_vector[rank - 1]
    return utility

def compute_social_welfare(allocation, profiles, score_vector, aggregation_function):
    utilities = [compute_utility(profiles[i], allocation[i], score_vector) for i in range(len(profiles))]
    
    if aggregation_function == 'utilitarian':
        return sum(utilities)
    elif aggregation_function == 'egalitarian':
        return min(utilities)
    elif aggregation_function == 'nash':
        return np.prod(utilities)


def compute_score_vector(m, score_function):
    if score_function == "Borda":
        return  [m - k + 1 for k in range(1, m + 1)]
    elif score_function == "Lexicographic":
        return [2 ** (m - k) for k in range(1, m + 1)]
    elif score_function == "QI":
        return [1 + 0.1 * (m - k) for k in range(1, m + 1)]


score_vector = compute_score_vector(m,"Borda")
print(score_vector)
social_welfare = compute_social_welfare(allocation, profiles, score_vector, 'utilitarian')
print(social_welfare)


def bruteforce_optimal_policy(profiles, score_function, aggregation_function):
    n = len(profiles)
    m = len(profiles[0])
    score_vector = compute_score_vector(m, score_function)
    max_welfare = -float('inf')
    best_policy = None

    for policy in generate_policy(n, m):
        allocation = allocate_objects(policy, profiles)
        # print(allocation)
        social_welfare = compute_social_welfare(allocation, profiles, score_vector, aggregation_function)
        # print(social_welfare)
        if social_welfare > max_welfare:
            max_welfare = social_welfare
            best_policy = policy


    return best_policy, max_welfare


# best_policy, max_welfare, best_allocation = bruteforce_optimal_policy(profiles, "Borda", "utilitarian")
# print("Best policy:", best_policy, max_welfare, best_allocation)


def ESW(profiles, score_function):
    n = len(profiles)
    m = len(profiles[0])
    score_vector = compute_score_vector(m, score_function)
    
    current_policy = [0] * n
    max_min_utility = -float('inf')
    best_policy = None

    for i in range(m+1):
        allocation = allocate_objects(current_policy, profiles)
        utilities = [compute_utility(profiles[i], allocation[i], score_vector) for i in range(n)]

        min_utility = utilities[0]
        chosen_agent = 0
        for agent_id, utility in enumerate(utilities):
            if utility < min_utility:
                chosen_agent = agent_id
                min_utility = utility

        if min_utility > max_min_utility:
            max_min_utility = min_utility
            best_policy = current_policy.copy()

        if i<m: current_policy[chosen_agent] += 1 # Don't add m + 1 objects but the last loop test if the ESW is better at the end (when j=m) 


    # Complete the policy by giving all remaining objects to the last agent
    remaining_objects = m - sum(best_policy)
    best_policy[-1] += remaining_objects

    return best_policy, max_min_utility



best_policy, max_welfare = ESW(profiles, "Borda")
print("Best policy:", best_policy, max_welfare)

def test_bruteforce_equal_esw():
    """
    Test if bruteforce and esw have differents social welfares
    """
    for n in range(1,10):
        for m in range(n,15):
            profiles = generate_preference_profiles(n,m) # only one is selected amoung (m!)^(n-1)
            brute_force_sw = bruteforce_optimal_policy(profiles, "Borda", "egalitarian")[1]
            esw = ESW(profiles, "Borda")[1]
            assert(brute_force_sw == esw)
            print(n,m, brute_force_sw)


test_bruteforce_equal_esw()


from allocation import Allocation, Borda, egalitarian

def compare_esw_with_FC():
    "Compare the social welfare of esw and out prefious function"
    for n in range(2,10):
        for m in range(n,20):
            prog_dyn = Allocation(0,n,m,Borda(m), egalitarian) # a = 0 => FC
            profiles = [list(range(1,m+1))] * n # FC
            esw = ESW(profiles, "Borda")
            print(n,m, esw)
            print(prog_dyn)
            assert(prog_dyn[0,1] == esw[1])
            if not np.array_equal(prog_dyn[1:,0], np.array(esw[0], dtype=np.float64)):
                print("Two differents policy")


compare_esw_with_FC()

# n = 3
# m = 8
# profiles = [list(range(1,m+1))] * n
# print(profiles)
# print(ESW(profiles, "Borda"))