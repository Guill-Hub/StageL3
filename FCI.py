from math import factorial
import numpy as np
import matplotlib.pyplot as plt
import copy

import matplotlib.cm as cm

def Borda(n):
    return [0] + [ n - i + 1 for i in range(1,n+1)] # le premier element ne sert à rien

m = 12
n = 4
V = Borda(m)
k = 3


#utilitarian = lambda x,y : x + y   les lambdas ne se plot pas bien après
#nash = lambda x,y : x * y

def egalitarian(x,y):
    return min(x,y)

def utilitarian(x,y):
    return x + y

def nash(x,y):
    return x * y

def FC(k,t,m,V):
    return sum(V[k+1:t+k+1]) # +1 because the first value is 0

def U_cor(a,k,t,m,V,T):
    return a * FC(k,t,m,V) + (1-a) * G(i,k,t,m,V,T)

def G(i,k,t,m,V,T): 
    """
    Sans perte de généralité on considère que l'agent classe les objets dans l'ordre 1...n.
    T[i,k,t] - i for the objects from {i,...,m}
             - k objects are not pickable on {i,...,m}
             - t objects will be picked by the agent
    and T[i,k,t] is the mean value
    
    k + t <= m
    """
    
    if T[i,k,t] == -1: # if not called yet
        T[i,k,t] = 0 # we start processing
        
        if k == 0:
            for j in range(t):
                T[i,k,t] += V[i+j]
        
        elif t == 0:
            return 0
        
        else:           
            T[i,k,t] = k/(m+1-i) * G(i+1,k-1,t,m,V,T) + (1 - k/(m+1-i)) * ( V[i] + G(i+1,k,t-1,m,V,T))
        
    return T[i,k,t]
    

def E(k,t,m,V,T):
    """
    Compute the mean value of an agent picking t objects starting while k objets already been taking.
    For m objets and the vector score V
    """
    #T = np.full((m+1,m+1,m+1),-1.)
    return G(1,k,t,m,V,T)

T = np.full((m+1,m+1,m+1),-1.)
#print(E(k,m-k,m,V,T)) # pour comparer avec sylvain.py



def algo_verif(a,i,k,n,m,V,T,M,F):
    """
    return 
    - i the i-th agent so i can fill M
    - k objets already selected
    - n users left
    - m objects in total
    - V the vector of score
    - T array used for the memoisation of E(k,t)
    - M array used for the memoisation of G(i,r)
    
    """
    
    if M[k,n,0,0] == 0: #if not already computed
        M[k,n,0,0] = m   # set as computed
        if n == 1 :      # if there is just one more agent
            M[k,1,i,0] = m - k  # then he take all objets lefts
            M[k,1,i,1] = a * sum(V)* (1-k/m)  + (1-a) * sum(V[k+1::])
            # sum(V)* (1-k/m) because every object can be selected and has not been taken before with the probability of 1-k/m with FI, sum(V[k+1::]) is the rest on FC
            M[k,1,0,1] = M[k,1,i,1] #there is one agent so the social welfare is its utility
            
        else:
                        
            U_max = 0   #  we want to keep the utility which optimize the social welfare
            for t in range(m-k+1): # we will give t=0...(m-k) objets to agent i
                U_first = a * E(k,t,m,V,T) + (1-a) * FC(k,t,m,V) # we compute his expected utility
                partiel = algo_verif(a,i+1,k+t,n-1,m,V,T,M,F) # compute the sub-problem
                min_U = F(partiel[0][1],U_first) # compute the expected social welfare
                #print(t,partiel)
                if min_U > U_max: #if the policy maximize the social welfare
                    M[k,n] = copy.deepcopy(partiel)  # save policy of the sub-problem
                    M[k,n,0,1] = min_U # social welfare
                    M[k,n,i,0] = t #numbers of objects given to agent i
                    M[k,n,i,1] = U_first #expected utility of agent i 
                    U_max = min_U
                                
    return M[k,n]

def var(a,n,m,V,F):
    T = np.full((m+1,m+1,m+1),-1.)
    M = np.full((m+1,n+1,n+1,2),0.)
    return algo_verif(a,1,0,n,m,V,T,M,F)


V_exp = [0, 97.08928571428571, 85.92857142857143, 79.28571428571429, 69.55357142857143, 63.017857142857146, 50.625, 40.642857142857146, 29.785714285714285, 22.053571428571427, 15.5, 9.928571428571429, 5.196428571428571]

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
print(var(0.74,n,m,V_exp,egalitarian))

print(var(0.74,n,m,V_exp,utilitarian))

print(var(0.74,n,m,V_exp,nash))
#print(X[1,1] + X[2,1] + X[3,1])
print(Borda(m))
print(sum(Borda(m)))
np.set_printoptions(precision=6)
np.set_printoptions(suppress=True)
#print(var(n,m,Borda(m),utilitarian))
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
#print(optimal(n,m,Borda(m),utilitarian))
#print(optimal(n,m,Borda(m),egalitarian))
#print(optimal(n,m,Borda(m),nash))
