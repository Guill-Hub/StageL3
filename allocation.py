from math import factorial
import numpy as np
import matplotlib.pyplot as plt
import copy

import matplotlib.cm as cm

# Scoring vector

def Borda(n):
    return [0] + [ n - i + 1 for i in range(1,n+1)] # The first element is not used

def Lexicographic(m):
    return [0] + [ 2 ** ( m - i ) for i in range(m)]

eps = 5.e-2

def QI(m):
    return [0] + [ 1 + eps * (m - i) for i in range(m) ]

# Social welfare

def egalitarian(x,y):
    return min(x,y)

def utilitarian(x,y):
    return x + y

def nash(x,y):
    return x * y



def U_FC(k,t,m,V):
    """
    Compute the utility of an agent picking t objects knowing that k already have been picked under FC.
    """
    return sum(V[k+1:t+k+1]) # +1 because the first value of scoring vector are not used.


def G(i,k,t,m,V,T): 
    """
    Compute the expected utility of an agent picking t objects among objetcs i to m knowing that k already have been picked under FI and with the vector score V.
    T is used for memoisation such as :
    T[i,k,t] - i for the objects from {i,...,m}
             - k objects are not pickable on {i,...,m}
             - t objects will be picked by the agent
    and T[i,k,t] is the mean value
    
    k + t <= m
    """
    
    if T[i,k,t] == -1: # if not called yet
        T[i,k,t] = 0 # we start processing
        
        if k == 0: # if every objects are selectable
            for j in range(t): # the agent select her first t objetcs
                T[i,k,t] += V[i+j]
        
        elif t == 0: # if there is no more objects to share
            return 0 #the utility is 0
        
        else: #
            T[i,k,t] = k/(m+1-i) * G(i+1,k-1,t,m,V,T) + (1 - k/(m+1-i)) * ( V[i] + G(i+1,k,t-1,m,V,T))
        
    return T[i,k,t]
    

def U_FI(k,t,m,V,T):
    """
    Compute the expected utility of an agent picking t objects knowing that k already have been picked under FI and with the vector score V.
    """
    return G(1,k,t,m,V,T)

def Alloc_aux(a,i,k,l,m,V,T,M,F):
    """
    Compute the optimal (partial) social welfare (and the policy) for :
    - a the coefficient of correlation
    - i the i-th agent ( to fill M)
    - k objets already selected
    - l users left
    - m objects in total
    - V the vector of score
    - T array used for the memoisation of U_FI(k,t)
    - M array used for the memoisation of G(i,l)
    
    """
    
    if M[k,l,0,0] == 0: # if not already computed
        M[k,l,0,0] = m   # set as computed
        if l == 1 :      # if there is just one agent
            M[k,1,i,0] = m - k  # then he takes all remaining objetcs
            M[k,1,i,1] = a * sum(V)* (1-k/m)  # FI : every object can be selected and has not been taken before with the probability of 1-k/m 
            M[k,1,i,1] += (1-a) * sum(V[k+1::]) # FC : the remaining objects are objects k+1, k+2 , ... , m (there is an offset of 1 because V[0] is not used)
            M[k,1,0,1] = M[k,1,i,1] #there is one agent so the partial social welfare is her utility
            
        else:
                        
            SW_max = 0   #  we want to keep the utility which optimize the social welfare
            for t in range(m-k+1): # we will give t=0...(m-k) objets to agent i
                U_k = a * U_FI(k,t,m,V,T) + (1-a) * U_FC(k,t,m,V) # we compute his expected utility
                partiel = Alloc_aux(a,i+1,k+t,l-1,m,V,T,M,F) # compute the sub-problem solution
                SW = F(partiel[0][1],U_k) # compute the expected social welfare
                if SW > SW_max: #if the policy maximize the social welfare
                    M[k,l] = copy.deepcopy(partiel)  # save policy of the sub-problem
                    M[k,l,0,1] = SW # change the social welfare
                    M[k,l,i,0] = t # add the number of objects given to agent i
                    M[k,l,i,1] = U_k #add the expected utility of agent i 
                    SW_max = SW
                                
    return M[k,l]

def Allocation(a,n,m,V,F):
    """
    Compute the optimal policy for :
    - a the coefficient of correlation
    - n the number of agents
    - m the number of objetcs
    - V the scoring vectore
    - F the social welfare
    """
    T = np.full((m+1,m+1,m+1),-1.)
    M = np.full((m+1,n+1,n+1,2),0.)
    return Alloc_aux(a,1,0,n,m,V,T,M,F)

n = 5
m = 30
print(Allocation(1,n,m,Borda(m),egalitarian))
