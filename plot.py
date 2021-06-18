from hugo import *
from math import factorial
import numpy as np
import matplotlib.pyplot as plt
import copy

import matplotlib.cm as cm


def plot_fm(n,m,S):
    #fair un plot f(n) tq max_min / min ou max en fait mdr pour voir les bornes
    MAX = []
    MIN = []
    DIFF = []
    N = []
    for nb_object in range(n,m):
        V = S(nb_object)
        T = algo_gen(n,nb_object,V)
        MIN.append(T[0,1])
        MAX.append(U_max(T))
        DIFF.append((MAX[-1] - MIN[-1])/MAX[-1])
        N.append(nb_object)
    plt.plot(N, DIFF, label=" ")
    plt.title("Relative difference of expected utility when there is m objects to share between " + str(n) + " agents ")
    plt.xlabel("m : the number of objects")
    plt.ylabel("(max(U)-min(U)/max(U))")
    plt.show()


def plot_fn(n,m,V):
    #fair un plot f(n) tq max_min / min ou max en fait mdr pour voir les bornes
    MAX = []
    MIN = []
    DIFF = []
    N = []
    for i in range(2,n):
        T = algo_gen(i,m,V)
        MIN.append(T[0,1])
        MAX.append(U_max(T))
        DIFF.append((MAX[-1] - MIN[-1])/MAX[-1])
        N.append(i)
    plt.title(" Relative difference of expected utility when there is " + str(m) + " objects to share between n agents")
    plt.plot(N, DIFF, label=" (max(n) - min(n))/max(n)")
    plt.xlabel("n : the number of agents")
    plt.ylabel("Relative difference of expected utility")
    plt.legend()
    print(DIFF)
    plt.show()

def plot_fnm(n,m,S):
    #debile comme façon de faire étant donné que dans le calcul de T[m,n] on a déjà calculé les valeurs plus petites
    for nb_agent in range(2,n):
        DIFF = []
        N = []
        for nb_objet in range(nb_agent,m):
            V = S(nb_objet)
            T = algo_gen(nb_agent,nb_objet,V)
            MIN = T[0,1]
            MAX = U_max(T)
            DIFF.append((MAX - MIN)/MAX)
            N.append(nb_objet)
        plt.plot(N, DIFF, label="n = " + str(nb_agent), color=cm.rainbow(nb_agent/n))
    plt.legend()
    plt.title(" Relative difference of expected utility when there is m objects to share between n agents")
    plt.xlabel("m : the number of objects")
    plt.ylabel("(max(U)-min(U)/max(U))")
    plt.show()

#plot_fnm(n,m,V)

def quick_plot_mn(n,m,S):
    for nb_objet in range(n,m):
        T = np.full((nb_objet+1,nb_objet+1,nb_objet+1),-1.)
        M = np.full((nb_objet+1,n+1,n+1,2),-1.)
        V = S(nb_objet)
        DIFF = []
        N = []
        for nb_agent in range(2,n):
            val = algo_aux(1,0,nb_agent,nb_objet,V,T,M)
            MAX = U_max(val)
            MIN = val[0][1]
            DIFF.append((MAX - MIN)/MAX)
            N.append(nb_agent)
        if (nb_objet % ( m // 20)) == 0:# pour n'avoir que 20 labels
            plt.plot(N, DIFF, label="m = " + str(nb_objet), color=cm.rainbow(nb_objet/m))
        else:
            plt.plot(N, DIFF, color=cm.rainbow(nb_objet/m))
    plt.legend()
    plt.title(" Relative difference of expected utility when there is m objects to share between n agents")
    plt.xlabel("n : the number of agents")
    plt.ylabel("(max(U)-min(U)/max(U))")

    plt.show()
    
def plot_chaque(n,m,S):
    N = [ i for i in range(n,m)]
    X = [ [] for i in range(n+1)]
    for nb_objet in range(n,m):
        V = S(nb_objet)
        val = algo_gen(n,nb_objet,V)
        #print(nb_objet,val)
        for agent in range(1,n+1):
            X[agent].append(val[agent][1])
    for agent in range(1,n+1):
                  plt.plot(N,X[agent], label = "agent " + str(agent), color=cm.rainbow(agent/n))
    plt.legend()
    plt.title("Partage entre " + str(n) + " agents pour m de "+ str(n) + " à " + str(m))
    plt.show()

def Borda(n):
    return [0] + [ n - i + 1 for i in range(1,n+1)] # le premier element ne sert à rien

m = 100
n = 5
V = Borda(m)

#plot_chaque(n,m,Borda)
#plot_fm(n,m,Borda)
#plot_fn(n,m,V)
#plot_fnm(n,m,Borda)
quick_plot_mn(n,m,Borda) 
