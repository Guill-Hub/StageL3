from math import factorial
import numpy as np
import matplotlib.pyplot as plt
import copy

import matplotlib.cm as cm
from random import sample

def E(i,m,V,p,Em):
    """
    i objects already selected
    m objets in total
    V scoring
    p precision ( number of loop)
    Em memo for E
    return an array such as Em[i,j] correspond to the mean value of the object j, knowing that the user begin to select object by the i+1 ths
    in fact it will be E[i,j-i]
    """
    if Em[i,m] == - 1:
        Em[i,m] = 0
        M = np.zeros((p,m))
        for j in range(p):
            M[j] = T(i,m,V)
        #print(M)
        Em[i] = np.mean(M,axis=0) # est-ce qu'il y a pleins de moyennes de 0 ? J'ai bien peur
    
    return Em[i,m]


def T(i,m,V):
    """
    return one of the attempt of what an user could take if he start choosing after the i th object
    """
    
    return np.concatenate( np.full((i,1),-1), sorted(sample(V,m-i),reverse = True))

def Borda(n):
    return [ n - i + 1 for i in range(1,n+1)] # le premier element ne sert à rien

m = 300
n = 2
V = Borda(m)
p = 1000

print(E(50,m,V,p))

def gen(n,m,V):
    """
    n users
    m objects
    """
    Em = np.full((m+1,m+1),-1)
    M = np.full((m+1,n+1,n+1,2),-1)
    aux(0,1,n,m,V,M,Em)

def aux(i,j,n,m,V,M,Em):
    """
    i objetcs already selected
    j it's the j th agent
    n agnts
    m objetcs in total
    V scoring vector
    M memo
    
    T[i,n] : 
            -i objects are already been selected by the previous participent
            - there is still n agents
    """
    if M[i,n,0,0] == -1:
        M[i,n,0,0] = 0
        if i == m :
            return 0
        if n == 1:
            for k in range(i+1,m+1):
                M[i,n,j,1] += E(i,k)
            M[i,n,j,0] = m # endroit limite où on coupe
            
        else:
            S = 0
            for nb_object in range(i+1,m+1):
                S += E(i,nb_object,V,p,Em)
                if S > aux(nb_object,j+1,n-1,m,V,M,Em)[0,1]:
                    if min(aux(nb_object-1,j+1,n-1,m,V,M,Em)[0][1],S - E(i,nb_object,V,p,Em) ) > S:
                        nb_object -= 1
                        S -= E(i,nb_object,V,p,Em)
                    M[i,n] = aux(nb_object,j+1,n-1,m,V,M,Em)
                    M[i,n,j,0] = nb_object
                    M[i,n,j,1] = S
                    M[i,n,0,1] = min(S,aux(nb_object,j+1,n-1,m,V,M,Em)[0,1])
                    break
        return M[i,n]
                    
                
