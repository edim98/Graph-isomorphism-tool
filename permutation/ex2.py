from permutation.perm import *

def composition(p, q):
    res = []
    for i in range(len(p)):
        res.append(p[q[i]])
    return res

