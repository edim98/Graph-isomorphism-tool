from permv2 import *
from basicpermutationgroup import *
from permutation.ex5 import period2 as period
from graph import *
from coloring import frequencies
from individualization import balanced, bijection, disjointUnion
from refined_colouring import refine_colour
from preprocessing import removeNoDegrees

def compute_order(H):
    if len(H) == 1 and H[0].istrivial():
        return 1
    alpha = FindNonTrivialOrbit(H)
    if alpha is not None:
        orbitAlpha = Orbit(H, alpha, returntransversal = False)
        stabilizerAlpha = Stabilizer(H, alpha)
        orderOrbit = len(orbitAlpha)
        if len(stabilizerAlpha) == 0:
            return orderOrbit
        else:
            return orderOrbit * compute_order(stabilizerAlpha)

def is_permutation_new(f, H):
    if len(H) == 0:
        return f.istrivial()
    if f.istrivial():
        return True
    if len(H) == 1 and H[0].istrivial():
        return False

    alpha = FindNonTrivialOrbit(H)
    orbit, transversal = Orbit(H, alpha, returntransversal = True)
    beta = f.P[alpha]

    if beta not in orbit:
        return False
    else:
        stabilizerAlpha = Stabilizer(H, alpha)
        u = transversal[orbit.index(beta)]
        inverseOfU = -u
        newPerm = inverseOfU * f

        return is_permutation_new(newPerm, stabilizerAlpha)

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



def generateAutomorphism(G, D, I, X, lenSimpleG, trivial):
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
        f = create_permutation(lenSimpleG, dll)
        if f is None:
            return False
        elif not is_permutation_new(f, X):
            X.append(f)
            return True
        return False

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

    returnToAncestor = False
    for i in range(lenG//2, lenG):
        if colorings[i] == chosenColor:
            vertex = G.vertices[i]
            if vertex not in I:
                if vertex.degree == chosenVertex.degree:
                    I.append(vertex)
                    if vertex.label % lenSimpleG != chosenVertex.label % lenSimpleG:
                        # currentTrivial = False
                        returnToAncestor = generateAutomorphism(G, D, I, X, lenSimpleG, False)
                    else:
                        # currentTrivial = True
                        returnToAncestor = generateAutomorphism(G, D, I, X, lenSimpleG, True)

                    # returnToAncestor = generateAutomorphism(G, D, I, X, lenSimpleG)
                    I.remove(vertex)
                    if returnToAncestor and not trivial:
                        break
    D.remove(chosenVertex)
    return returnToAncestor

def countAutomorphism(g1, g2):
    G = disjointUnion(g1, g2)
    X = []
    removeNoDegrees(G)
    generateAutomorphism(G, [], [], X, len(g2), True)
    return compute_order(X)
