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
            #print("prout")
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

m = 30
n = 20
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
            #print("prout")
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


def plot2(n,m,V):
    #fair un plot f(n) tq max_min / min ou max en fait mdr pour voir les bornes
    for i in range(2,n):
        MAX = []
        MIN = []
        DIFF = []
        N = []
        for j in range(n,m):
            T = algo_gen(i,j,V)
            MIN.append(T[0,1])
            MAX.append(U_max(T))
            DIFF.append((MAX[-1] - MIN[-1])/MAX[-1])
            N.append(i)
        plt.plot(N, DIFF , label= i)
    
    plt.legend()
    plt.title('(Umax(m) - Umin(m)) / Umax(m) ')
    print(DIFF)
    plt.show()


def plot(n,m,V):
    #fair un plot f(n) tq max_min / min ou max en fait mdr pour voir les bornes
    MAX = []
    MIN = []
    DIFF = []
    N = []
    for i in range(n,m):
        T = algo_gen(n,i,V)
        MIN.append(T[0,1])
        MAX.append(U_max(T))
        DIFF.append((MAX[-1] - MIN[-1])/MAX[-1])
        N.append(i)
    plt.plot(N, DIFF, label=" ")
    plt.title('(Umax(m) - Umin(m)) / Umax(m) pour n = 10')
    print(DIFF)
    plt.show()


def plot(n,m,V):
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
    plt.title('(Umax(n) - Umin(n)) / Umax(n) pour m = ' +  str(m) )
    plt.plot(N, DIFF, label=" ")
    print(DIFF)
    plt.show()

def plot2(n,m,V):
    #debile comme façon de faire étant donné que dans le calcul de T[m,n] on a déjà calculé les valeurs plus petites
    for nb_agent in range(2,n):
        MAX = []
        MIN = []
        DIFF = []
        N = []
        for nb_objet in range(n,m):
            T = algo_gen(nb_agent,nb_objet,V)
            MIN.append(T[0,1])
            MAX.append(U_max(T))
            DIFF.append((MAX[-1] - MIN[-1])/MAX[-1])
            N.append(nb_objet)
        plt.plot(N, DIFF, label="n = " + str(nb_agent), color=cm.cool(nb_agent/n))
        plt.legend()
    plt.title('(Umax(m) - Umin(m)) / Umax(m)' )
    plt.show()
#print(algo_gen(n,m,Borda(m)))
def quick_plot(n,m,V):
    T = np.full((m+1,m+1,m+1),-1.)
    M = np.full((m+1,n+1,n+1,2),-1.)
    algo_verif(1,0,n,m,V,T,M)
    for nb_agent in range(2,n):
        MAX = []
        MIN = []
        DIFF = []
        N = []
        for nb_objet in range(nb_agent,m):
            T = M[nb_objet,nb_agent]
            MIN.append(T[0,1])
            MAX.append(U_max(T))
            DIFF.append((MAX[-1] - MIN[-1])/MAX[-1])
            N.append(nb_objet)
        plt.plot(N, DIFF, label="n = " + str(nb_agent), color=cm.cool(nb_agent/n))
        #plt.legend()
    plt.title('(Umax(m) - Umin(m)) / Umax(m)' )

    plt.show()
    
def plot_chaque(n,m,V):
    N = [ i for i in range(n,m)]
    X = [ [] for i in range(n+1)]
    for nb_objet in range(n,m):
        for agent in range(1,n+1):
            #X.append(algo_verif(i,k,n,m,V,T,M))
            T = np.full((nb_objet+1,nb_objet+1,nb_objet+1),-1.)
            M = np.full((nb_objet+1,n+1,n+1,2),-1.)
            algo_verif(1,0,n,nb_objet,Borda(nb_objet),T,M)
            X[agent].append(M[0,n,agent,1])
    for agent in range(1,n+1):
                  plt.plot(N,X[agent])
    plt.show()

for i in range(m):
    print(algo_gen(n,i,V))
plot_chaque(n,m,V)
