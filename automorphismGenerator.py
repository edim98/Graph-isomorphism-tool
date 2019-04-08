from permv2 import *
from basicpermutationgroup import *
from permutation.ex5 import period2 as period
from graph import *
from coloring import frequencies
from individualization import balanced, bijection
from refined_colouring import refine_colour

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

    if f.istrivial():
        return False
    # if len(H)==1 and H[0].istrivial():
    #     if f.istrivial():
    #         return False
    #     return True

    for v in G.vertices:
        alpha_H, transversal = Orbit(H, v.label, returntransversal = True)
        if len(alpha_H) >= 2:
            alpha = v.label
            beta = f[alpha]
            if beta not in alpha_H:
                return True
            else:
                for perm in transversal:
                    if perm[alpha] == beta:
                        composition = -perm * f
                        H_alpha = Stabilizer(H, alpha)
                        return is_permutation_new(composition, H_alpha, G)

def create_permutation(lenG, dll):
    lenDll = len(dll)
    mapping = [0] * lenG
    for i in range(lenDll):
        d = dll[i]
        if d.size > 0:
            c1 = d.start.state % lenG
            c2 = d.end.state % lenG
            mapping[c1] = c2
    try:
        p = permutation(lenG, mapping = mapping)
    except:
        return None
    return p



def generateAutomorphism(G, D, I, X, trivial, simpleG):
    max_color = 1
    colorings = [0] * len(G.vertices)
    dll = None
    if D != [] and I != []:
        for i in D:
            colorings[i.label] = max_color
            max_color += 1


        max_color = 1
        for j in I:
            colorings[j.label] = max_color
            max_color += 1
        colorings, dll = refine_colour(G, colorings)

    frequency = frequencies(colorings)

    if not balanced(frequency): # no auto that follows (D, I)
        return False

    if bijection(frequency): # follows (D, I)
        f = create_permutation(len(simpleG), dll)
        if f is None:
            return False
        # elif f.istrivial():
            # return True
        if len(X) == 0 or (len(X) == 1 and X[0].istrivial()):
            X.append(f)
        elif is_permutation_new(f, X, simpleG):
            X.append(f)
        return True

    chosenColor = -1
    for i in range(len(frequency)):
        if frequency[i] >= 4:
            chosenColor = i
            break

    chosenVertex = None
    lenG = len(G.vertices)
    for i in range(lenG//2):
        if colorings[i] == chosenColor:
            vertex = G.vertices[i]
            if vertex not in D:
                chosenVertex = vertex
                D.append(vertex)
                break

    for i in range(lenG//2, lenG):
        if colorings[i] == chosenColor:
            vertex = G.vertices[i]
            if vertex not in I:
                if vertex.degree == chosenVertex.degree:
                    I.append(vertex)
                    generateAutomorphism(G, D, I, X, False, simpleG)
                    # if vertex.label - lenG //2 != chosenVertex.label: # if we choose a mapping x -> y
                        # returnToAncestor = generateAutomorphism(G, D, I, X, False)

                    # else: # if we choose a mapping x -> x
                    #     returnToAncestor = generateAutomorphism(G, D, I, X, True)
                    I.remove(vertex)
                    # if returnToAncestor and not trivial:
                    #     break
    D.remove(chosenVertex)
    return False
    # return returnToAncestor
