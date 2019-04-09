from permutation.perm import*

def inverse(p):
    res = []
    for i in range(len(p)):
        for j in range(len(p)):
            if p[j] == i:
                res.append(p[j])
    return res

p = [2, 1, 3, 0]
# print(inverse(p))
