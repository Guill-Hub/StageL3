from math import factorial
import numpy as np
import matplotlib.pyplot as plt
import copy

import matplotlib.cm as cm

def Borda(n):
    return [0] + [ n - i + 1 for i in range(1,n+1)] # le premier element ne sert à rien

m = 150
n = 5
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

def G(i,k,t,m,V,T):
    #print(i,k,t) 
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
        
    #print(i,k,t,T[i,k,t])
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



#m=4

#print(F(1,0,1,m,Borda(m),np.full((m+1,m+1,m+1),-1.)))

def algo_gen(n,m,V):
    T = np.full((m+1,m+1,m+1),-1.)
    M = np.full((m+1,n+1,n+1,2),-1.)
    return algo_aux(1,0,n,m,V,T,M)
    
def algo_aux(i,k,n,m,V,T,M): #user i, k objets already selected, n users, m objets in total, V scoring, T memo des E(k,t), M memo des meilleurs select
    #print(i,k,n,m)
    
    if M[k,n,0,0] == -1:
        M[k,n,0,0] = 0
        if n == 1 :
            M[k,1,i,0] = m - k
            M[k,1,i,1] = sum(V)* (1-k/m)
            M[k,1,0,1] = M[k,1,i,1]
        else:
            
            for t in range(1,m-k+1): 
                U_first = E(k,t,m,V,T)
                partiel = algo_aux(i+1,k+t,n-1,m,V,T,M)
                min_U = partiel[0][1]
                if min_U < U_first:
                    if min_U < min(algo_aux(i+1,k+t-1,n-1,m,V,T,M)[0][1],E(k,t-1,m,V,T)):
                        t -=1
                    
                    M[k,n] = algo_aux(i,k+t,n-1,m,V,T,M)
                    M[k,n,0,1] = min(M[k,n,0,1],E(k,t,m,V,T))
                    M[k,n,i,0] = t # nombre d'objets, k+t pour savoir où couper
                    M[k,n,i,1] = E(k,t,m,V,T)
                    break
                        
        
    return M[k,n]


#print(algo_gen(n,m,Borda(m)))   

#print(E(200-11,11,m,Borda(m),np.full((m+1,m+1,m+1),-1.)))



# Je ne peux plus utiliser le fait que dès que le min_U < U_fist il y a bascule car rien n'implique que ça reste vrai avec le + et le *,du coup je dois faire une exploration

def algo_verif(i,k,n,m,V,T,M,F):
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
    
    if M[k,n,0,0] == -1: #if not already computed
        M[k,n,0,0] = 0   # set as computed
        if n == 1 :      # if there is just one more agent
            M[k,1,i,0] = m - k  # then he take all objets lefts
            M[k,1,i,1] = sum(V)* (1-k/m) #every object can be selected and has not been taken before with the probability of 1-k/m
            M[k,1,0,1] = M[k,1,i,1] #there is one agent so the social welfare is its utility
            
        else:
                        
            U_max = 0   #  we want to keep the utility which optimize the social welfare
            for t in range(m-k+1): # we will give t=0...(m-k) objets to agent i
                U_first = E(k,t,m,V,T) # we compute his expected utility
                partiel = copy.deepcopy(algo_verif(i+1,k+t,n-1,m,V,T,M,F)) # compute the sub-problem
                min_U = F(partiel[0][1],U_first) # compute the expected social welfare

                if min_U > U_max: #if the policy maximize the social welfare
                    M[k,n] = partiel # save policy of the sub-problem
                    M[k,n,0,1] = min_U # social welfare
                    M[k,n,i,0] = t #numbers of objects given to agent i
                    M[k,n,i,1] = U_first #expected utility of agent i
                    U_max = min_U
                                
    return M[k,n]

def var(n,m,V,F):
    T = np.full((m+1,m+1,m+1),-1.)
    M = np.full((m+1,n+1,n+1,2),-1.)
    return algo_verif(1,0,n,m,V,T,M,F)

def optimal(n,m,V,F):
    T = np.full((m+1,m+1,m+1),-1.)
    M = np.full((m+1,n+1,n+1,2),-1.)
    return algo_opt(1,0,n,m,V,T,M,F)

def algo_opt(i,k,n,m,V,T,M,F):
    
    if M[k,n,0,0] == -1:
        M[k,n,0,0] = 0
        if n == 1 :
            M[k,1,i,0] = m - k
            M[k,1,i,1] = sum(V[1:m-k+1])
            M[k,1,0,1] = M[k,1,i,1]
            #print("test")
        else:
            
            
            U_max = 0
            for t in range(m-k+1): 
                U_first = Opt(k,t,m,V,T)
                partiel = copy.deepcopy(algo_opt(i+1,k+t,n-1,m,V,T,M,F))
                min_U = F(partiel[0][1],U_first)
                #print(U_max,min_U,t,i)

                if min_U > U_max:
                    M[k,n] = partiel
                    M[k,n,0,1] = min_U
                    M[k,n,i,0] = t # nombre d'objets, k+t pour savoir où couper
                    M[k,n,i,1] = U_first
                    U_max = min_U
                    #print("WHOLOLO")
                        
        
    return M[k,n]

def Opt(k,t,m,V,T):
    return sum(V[1:t+1])

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
print(var(n,m,Borda(m),egalitarian))
np.set_printoptions(precision=6)
np.set_printoptions(suppress=True)
#print(var(n,m,Borda(m),utilitarian))
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
#print(optimal(n,m,Borda(m),utilitarian))
#print(optimal(n,m,Borda(m),egalitarian))
#print(optimal(n,m,Borda(m),nash))

#test
