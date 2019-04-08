import math

from graph_io import *
from refined_colouring import *

def disjointUnion(G, H):
    lenG = len(G)
    for vertex in H.vertices:
        newVertex = Vertex(G)
        G.add_vertex(newVertex)
    for edge in H.edges:
        head = G.vertices[edge.head.label + lenG]
        tail = G.vertices[edge.tail.label + lenG]
        newEdge = Edge(tail, head)
        G.add_edge(newEdge)
    return G

def bijection(f):
    for i in range(len(f)):
        if f[i] != 2:
            return False
    return True


def balanced(f):
    for i in range(len(f)):
        if f[i] % 2 == 1:
            return 0
    return 1

def frequencies(colorings):
    maxvalue = -1
    frequency = [0] * (len(colorings))
    for i in colorings:
        maxvalue = max(maxvalue, i)
        frequency[i] += 1
    frequency = frequency[:maxvalue + 1]

    return frequency

# def trivial(D, I):
#     lenD = len(D)
#     for i in range(lenD - 1, -1, -1):
#         if D[i] != I[i]:
#             return False
#     return True

def count_isomorphism(G, D, I):
    max_color = 1
    colorings = [0] * len(G.vertices)
    if D != [] and I != []:
        for i in D:
            colorings[i.label] = max_color
            max_color += 1


        max_color = 1
        for j in I:
            colorings[j.label] = max_color
            max_color += 1
        colorings = refine_colour(G, colorings)

    frequency = frequencies(colorings)

    if not balanced(frequency):
        # return 0, 0
        return 0

    if bijection(frequency):
        # if trivial(D, I):
        #     return 1, 0
        # return 1, 1
        return 1

    chosenColor = -1
    for i in range(len(frequency)):
        if frequency[i] >= 4:
            chosenColor = i
            break
    num = 0

    chosenVertex = None
    lenG = len(G.vertices)
    for i in range(len(colorings)):
        if colorings[i] == chosenColor and i >= 0 and i < lenG//2:
            vertex = G.vertices[i]
            if vertex not in D:
                chosenVertex = vertex
                D.append(vertex)
                break

    for i in range(len(colorings)):
        if colorings[i] == chosenColor and i >= lenG//2 and i < lenG:
            vertex = G.vertices[i]
            if vertex not in I:
                if vertex.degree == chosenVertex.degree:
                    I.append(vertex)
                    # res, trivialJump = count_isomorphism(G, D, I)
                    res = count_isomorphism(G, D, I)
                    num += res
                    # if trivialJump:
                    #     if not trivial(D, I):
                    #         I.remove(vertex)
                    #         break
                    I.remove(vertex)
    D.remove(chosenVertex)
    # return num, trivialJump
    return num


def test_countIsomorphism():

    with open("cubes3.grl") as f:
        G = load_graph(f, read_list = True)
    L = G[0][0]
    H = G[0][0]
    G = disjointUnion(L, H)
    print("Number of isomorphisms found: {}".format(count_isomorphism(G, [], [])))



# test_countIsomorphism()
