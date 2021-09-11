import matplotlib.pyplot as plt
import matplotlib.cm as cm
from allocation import *

n = 5
m = 30


def U_max(T):
    maxi = 0 
    for e in [ el[1] for el in T[1:]]:
        maxi = max(maxi,e)
    return maxi

def SumU(T):
    S = 0 
    for e in [ el[1] for el in T[1:]]:
        S += e
    return S

def U_min(T):
    mini = T[1,1]
    for e in [ el[1] for el in T[1:]]:
        mini = min(mini,e)
    return mini


def nb_max(T):
    maxi = 0
    for e in [ el[0] for el in T[1:]]:
        maxi = max(maxi,e)
    return maxi

def m_variation(a,n,m,S,F,step):
    M = []
    O = [ [] for i in range(n)]
    U = [ [] for i in range(n)]
    for nb_object in range(n,m+step,step):
        M.append(nb_object)
        V = S(nb_object)
        alloc = Allocation(a,n,nb_object,V,F)
        Su = SumU(alloc)
        print(nb_object,alloc)
        for agent in range(1,n+1):
            O[agent-1].append(alloc[agent][0]/nb_object)
            U[agent-1].append(alloc[agent][1]/Su)
    print(O,U)
    fig, axs = plt.subplots(1, 2, constrained_layout=True)
    axs[0].stackplot(M,U)
    axs[0].set_title('Utility')
    axs[0].set_xlabel('m')
    axs[0].set_ylabel('Proportion of utility')
    title = str(n) + " agents sharing "+ str(n) + " to " + str(m) + " objects, with alpha = " + str(a) + ", " + S.__name__ + " scoring vector and " + F.__name__ + " social-welfare"
    fig.suptitle(title, fontsize=16)

    axs[1].stackplot(M,O)
    axs[1].set_title('Objects')
    axs[1].set_xlabel('m')
    axs[1].set_ylabel('Proportion of objects')
    L = []
    for i in range(1,n+1):
        L.append("Agent " + str(i))
    fig.legend(L)


    plt.legend()
    plt.show()
    

def alpha_variation(n,m,S,F,step):
    M = []
    O = [ [] for i in range(n)]
    U = [ [] for i in range(n)]
    V = S(m)
    for alpha in np.arange(0,1+step,step):
        M.append(alpha)
        alloc = Allocation(alpha,n,m,V,F)
        print(m,alloc)
        for agent in range(1,n+1):
            O[agent-1].append(alloc[agent][0])
            U[agent-1].append(alloc[agent][1])
    print(O,U)
    fig, axs = plt.subplots(1, 2, constrained_layout=True)
    axs[0].stackplot(M,U)
    axs[0].set_title('Utility')
    axs[0].set_xlabel('alpha')
    axs[0].set_ylabel('Utility per agent')
    title = str(n) + " agents sharing "+ str(m) + " objects, with alpha varying from 0 to 1 with a step of " + str(step) + ", " + S.__name__ + " scoring vector and " + F.__name__ + " social-welfare"
    fig.suptitle(title, fontsize=16)

    axs[1].stackplot(M,O)
    axs[1].set_title('Objects')
    axs[1].set_xlabel('alpha')
    axs[1].set_ylabel('Number of Object per agent')
    L = []
    for i in range(1,n+1):
        L.append("Agent " + str(i))
    fig.legend(L)


    plt.legend()
    plt.show()
    
def n_variation(a,n,m,S,F,step):
    M = []
    O = [ [] for i in range(n)]
    U = [ [] for i in range(n)]
    V = S(m)
    for nb_agent in range(1,n+step,step):
        M.append(nb_agent)
        alloc = Allocation(a,nb_agent,m,V,F)
        Su = SumU(alloc)
        print(m,alloc)
        for agent in range(1,n+1):
            if agent <= nb_agent:
                O[agent-1].append(alloc[agent][0])
                U[agent-1].append(alloc[agent][1])
            else:
                O[agent-1].append(0)
                U[agent-1].append(0)
    print(O,U)
    fig, axs = plt.subplots(1, 2, constrained_layout=True)
    axs[0].stackplot(M,U)
    axs[0].set_title('Utility')
    axs[0].set_xlabel('n')
    axs[0].set_ylabel('Utility per agent')
    title = "1 to " + str(n) + " agents sharing " + str(m) + " objects, with alpha = " + str(a) + " " + S.__name__ + " scoring vector and " + F.__name__ + " social-welfare"
    fig.suptitle(title, fontsize=16)

    axs[1].stackplot(M,O)
    axs[1].set_title('Objects')
    axs[1].set_xlabel('n')
    axs[1].set_ylabel('Number of object per agent')
    L = []
    for i in range(1,n+1):
        L.append("Agent " + str(i))
    fig.legend(L)

    plt.show()
    


    

#print(Allocation(1,n,m,Borda(m),egalitarian))
m_variation(1,n,m,Lexicographic,egalitarian,5)
#alpha_variation(n,m,Lexicographic,egalitarian,0.1)
#n_variation(1,n,m,Lexicographic,egalitarian,1)
