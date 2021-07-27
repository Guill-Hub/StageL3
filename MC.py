from math import factorial
import numpy as np
import matplotlib.pyplot as plt
import copy

import matplotlib.cm as cm
from random import sample



def Borda(n):
    return [ n - i + 1 for i in range(1,n+1)] # !!! attention pas ce premier el nul comme pour les autres


import profile_generator

m = 10
n = 10
p = 10
V = Borda(m)



def fct_naive(n,m):
    gen = profile_generator.RandomSampleMallows(m,n,p)
    gen.refs = [[ m - i for i in range(m)]]
    
    
    

               
def recup_pref_libre(deja_select,pref):
    """
    fct qui récupère l'objet le plus aimé parmis les objets disponibles
    """
    maxi = - 1
    i_max =  -1 
    for i in range(n):
        if not deja_select[i] && pref[i] > maxi:
            maxi = pref[i]
            i_max = i
    deja_select[i_max] = True
    return maxi
               
def ExpectU(deja_select,j,k,P):
    """
    étant donné un profile de préférence P
    quel va être l'utilité du j eme agent sachant que l'agent 1 a prit k1 objet ... j - 1 k(j-1) et que le j eme en prend k
    en fait j'ai l'impression qu'on n'a pas besoin de savoir qui a prit quoi si déja select est une liste de bool, qu'on construit au fur et à mesure
    Deja select est un tableau de bool qui dit siobjet déjà select ou non
    """
    pref = P[k]
    U = 0
    for i in range(k):
         U += recup_pref_libre(deja_select,pref)
    return U

def algo_gen(
        
