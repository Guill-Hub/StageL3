from hugo import *
from sylvain import *

eps = 000.1

m = 100
n = 7
V = Borda(m)
p = 100
k = 3

def pretest(m,k):
    for i in range(k+1,m):
        V = Borda(i)
        T = np.full((i+1,i+1,i+1),-1.)
        print(i)
        if abs(compute_last_utility(i, k,V) -  E(k,i-k,i,V,T)) > 0.1 :
            return i


"""
def test(n,m):
    for i in range(2,n):
        for j in range(i,m):
            print(i,j)
            V = Borda(j)
            S = gen_egal(j,i,V)
            H = algo_gen(i,j,V)
            print("ok")
            if abs(H[0,1]- S[0,1]) > eps:
                print(H[0,1],S[0,1])
                return (i,j,S,H)
            

print(test(30,20))
"""
print(pretest(m,k))
