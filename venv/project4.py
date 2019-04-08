from project.permv2 import *
from project.basicpermutationgroup import *
from permutation.ex5 import period2 as period
from project.graph import *

def compute_order(H, G):
    alpha = None
    order_alpha = -1
    k = len(H)
    if k == 1:
        return period(list(H[0]))
    for v in G.vertices:
        alpha_H = Orbit(H, v.label)
        if len(alpha_H) >= 2:
            order_alpha = len(alpha_H)
            alpha = v.label
            break

    H_alpha = Stabilizer(H, alpha)
    return order_alpha * compute_order(H_alpha, G)


def is_permutation_new(f, H, G):
    alpha = None
    transversal = None
    if len(H) == 1 and H[0].is_trivial():
        if f.is_trivial():
            return "yes"
        else:
            return "no"

    for v in G.vertices:
        alpha_H, transversal = Orbit(H, v.label, True)
        if len(alpha_H) >= 2:
            alpha = v.label
            break

    beta = f * alpha
    if beta not in alpha_H:
        return "yes"
    else:
        composition = (-transversal[beta]) * f
        H_alpha = Stabilizer(H, alpha)
        return is_permutation_new(composition, H_alpha, G)
    
def test_compute_order():
    p = permutation(6, cycles=[[0,1,2],[4,5]])
    q = permutation(6, cycles=[[0],[1],[2],[2,3],[4],[5]])
    H = [p, q]
    G = Graph(False, 6)
    print("Order:",compute_order(H, G))


