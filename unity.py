from hugo import *
from algo_gen import *

eps = 000.1


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
