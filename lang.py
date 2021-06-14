from math import factorial
import numpy as np
import matplotlib.pyplot as plt
import copy


def F(i,k,t,m,V,T):
    #print(i,k,t) 
    """
    Sans perte de généralité on considère que l'agent classe les objets dans l'ordre 1...n.
    T[i,k,t] - i because we cause on the objects from {i,...,m}
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
            #T[i,k,t] /= (m+1-i)
        
        elif t == 0:
            return 0
        
        else:           
            T[i,k,t] = k/(m+1-i) * F(i+1,k-1,t,m,V,T) + (1 - k/(m+1-i)) * ( V[i] + F(i+1,k,t-1,m,V,T))
        
    #print(i,k,t,T[i,k,t])
    return T[i,k,t]
    

def E(k,t,m,V,T):
    """
    Compute the mean value of an agent picking t objects starting while k objets already been taking.
    For m objets and the vector score V
    """
    #T = np.full((m+1,m+1,m+1),-1.)
    return F(1,k,t,m,V,T)


def Borda(n):
    return [0] + [ n - i + 1 for i in range(1,n+1)] # le premier element ne sert à rien


#m=4
#print(E(3,1,4,Borda(4)))
#print(F(1,0,1,m,Borda(m),np.full((m+1,m+1,m+1),-1.)))

def algo_gen(n,m,V):
    T = np.full((m+1,m+1,m+1),-1.)
    M = np.full((m+1,n+1,n+1,2),-1.)
    return algo_aux(1,0,n,m,V,T,M)
    
def algo_aux(i,k,n,m,V,T,M): #user i, k objets already selected, n users, m objets in total, V socring, T memo des E(k,t), T memo des meilleurs select
    print(i,k,n,m)
    
    if M[k,n,0,0] == -1:
        M[k,n,0,0] = 0
        if n == 1 :
            M[k,1,i,0] = len(V) - k
            M[k,1,i,1] = sum(V[k:])/(m-k)
            M[k,1,0,1] = M[k,1,i,1]
            print("prout")
        else:
            
            for t in range(1,m-k+1): # break à faire
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

m = 3
print(algo_gen(2,m,Borda(m)))        

