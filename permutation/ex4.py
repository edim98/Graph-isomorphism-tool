from permutation.perm import *
from permutation.ex2 import composition
from permutation.ex3 import inverse

def power(p, i):
    res = p
    if i == 0:
        return trivial_permutation(len(p))
    elif i < 0:
        for j in range(-1, i, -1):
            res = inverse(res)
    elif i == 1:
        return p
    else:
        for j in range(1, i - 1):
            res = composition(res, p)
    return res