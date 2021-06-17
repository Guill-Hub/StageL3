from math import factorial
import numpy as np
import matplotlib.pyplot as plt
import copy

import matplotlib.cm as cm

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

#print(F(1,0,1,m,Borda(m),np.full((m+1,m+1,m+1),-1.)))

def algo_gen(n,m,V):
    T = np.full((m+1,m+1,m+1),-1.)
    M = np.full((m+1,n+1,n+1,2),-1.)
    return algo_aux(1,0,n,m,V,T,M)
    
def algo_aux(i,k,n,m,V,T,M): #user i, k objets already selected, n users, m objets in total, V socring, T memo des E(k,t), T memo des meilleurs select
    #print(i,k,n,m)
    
    if M[k,n,0,0] == -1:
        M[k,n,0,0] = 0
        if n == 1 :
            M[k,1,i,0] = m - k
            M[k,1,i,1] = sum(V)* (1-k/m)
            M[k,1,0,1] = M[k,1,i,1]
            #print("test")
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

m = 400
n = 15
V = Borda(m)
#print(algo_gen(n,m,Borda(m)))   

#print(E(200-11,11,m,Borda(m),np.full((m+1,m+1,m+1),-1.)))

def algo_verif(i,k,n,m,V,T,M):
    #print(i,k,n,m)
    
    if M[k,n,0,0] == -1:
        M[k,n,0,0] = 0
        if n == 1 :
            M[k,1,i,0] = m - k
            M[k,1,i,1] = sum(V)* (1-k/m)
            M[k,1,0,1] = M[k,1,i,1]
            #print("test")
        else:
            
            
            U_max = 0
            for t in range(1,m-k+1): # break à faire
                U_first = E(k,t,m,V,T)
                partiel = copy.deepcopy(algo_verif(i+1,k+t,n-1,m,V,T,M))
                min_U = min(partiel[0][1],U_first)
                #print(U_max,min_U,t,i)

                if min_U > U_max:
                    M[k,n] = partiel
                    M[k,n,0,1] = min_U
                    M[k,n,i,0] = t # nombre d'objets, k+t pour savoir où couper
                    M[k,n,i,1] = U_first
                    U_max = min_U
                    #print("WHOLOLO")
                        
        
    return M[k,n]

def var(n,m,V):
    T = np.full((m+1,m+1,m+1),-1.)
    M = np.full((m+1,n+1,n+1,2),-1.)
    return algo_verif(1,0,n,m,V,T,M)

def U_max(T):
    maxi = 0
    for e in [ el[1] for el in T ]:
        maxi = max(maxi,e)
    return maxi



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
        if 
        plt.plot(N, DIFF, label="m = " + str(nb_objet), color=cm.rainbow(nb_objet/m))
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


#plot_chaque(n,m,Borda)
#plot_fm(n,m,Borda)
#plot_fn(n,m,V)
#plot_fnm(n,m,Borda)
quick_plot_mn(n,m,Borda)
