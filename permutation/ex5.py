from permutation.perm import *
from permutation.ex4 import power
from permutation.ex2 import composition
import time

def lcm(x, y):
    if x > y:
        z = x
    else:
        z = y

    while(True):
        if((z % x == 0) and (z % y == 0)):
            lcm = z
            break
        z += 1
    return lcm

def period(p):
    trivial = trivial_permutation(len(p))
    i = 1
    pp = p
    while True:
        if pp == trivial:
            return i
        else:
           #print("{} x {} = ".format(p, pp), end="")
           pp =  composition(p, pp)
           #print("{} vs {}".format(pp, trivial))
           i += 1
    #return i

def period2(p):
    # trivial = trivial_permutation(len(p))
    cycless = cycles(p)
    lens = []
    power = -1
    for i in range(len(cycless)):
        lens.append(len(cycless[i]))
        if i == 1:
            power = lcm(lens[i], lens[i-1])
        elif i > 1:
            power = lcm(lens[i], power)
    return power

# time_now = time.time()
# p = test_permutation(100)
# print("Period:", period2(p))
# print(period2(p))
# print("Time taken:", time.time() - time_now)