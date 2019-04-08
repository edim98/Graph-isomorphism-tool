import math

from graph_io import *
from refined_colouring import *

# def disjointUnionCata(G, H): #test for large instances
#     lenG = len(G.vertices)
#     lenH = len(H.vertices)
#     eG = G.edges
#     eH = H.edges
#     R = Graph(False, lenG + lenH)
#
#     for i in range(lenG):
#         for j in range(i, lenG):
#             if G.vertices[i].is_adjacent(G.vertices[j]):
#                 edge_g = Edge(G.vertices[i], G.vertices[j])
#
#                 for e in eG:
#                     if edge_g.tail == e.tail and edge_g.head == e.head:
#                         edge = Edge(R.vertices[j], R.vertices[i])
#                         R.add_edge(edge)
#                         # print("!G: connect edge {} and edge {}".format(j, i))
#                     elif edge_g.tail == e.head and edge_g.head == e.tail:
#                         edge = Edge(R.vertices[i], R.vertices[j])
#                         R.add_edge(edge)
#                         # print("G: connect edge {} and edge {}".format(i, j))
#
#     for i in range(lenH):
#         for j in range(i, lenH):
#             if H.vertices[i].is_adjacent(H.vertices[j]):
#                 edge_h = Edge(H.vertices[i], H.vertices[j])
#
#                 for e in eH:
#                     if edge_h.tail == e.tail and edge_h.head == e.head:
#                         edge = Edge(R.vertices[lenG + j], R.vertices[lenG + i])
#                         R.add_edge(edge)
#                         # print("!H: connect edge {} and edge {}".format(j, i))
#                     elif edge_h.tail == e.head and edge_h.head == e.tail:
#                         edge = Edge(R.vertices[lenG + i], R.vertices[lenG + j])
#                         R.add_edge(edge)
#                         # print("H: connect edge {} and edge {}".format(i, j))
#
#     return R

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

    # maxvalue = -1
    # for i in colorings:
    #     maxvalue = max(maxvalue, i)
    # frequency1 = [0]*(maxvalue + 1)
    #
    # for i in colorings:
    #     frequency1[i] += 1
    # return frequency1


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
        return 0

    if bijection(frequency):
        return 1

    chosenColor = -1
    for i in range(len(frequency)):
        if frequency[i] >= 4:
            chosenColor = i
            break
    num = 0

    chosenVertex = None
    for i in range(len(colorings)):
        if colorings[i] == chosenColor and i >= 0 and i < len(G.vertices)//2:
            # vertex = get_vertex_by_label(A, i)
            vertex = G.vertices[i]
            if vertex not in D:
                chosenVertex = vertex
                D.append(vertex)
                break

    # print(chosenVertex)
    for i in range(len(colorings)):
        if colorings[i] == chosenColor and i >= len(G.vertices)//2 and i < len(G.vertices):
            # vertex = get_vertex_by_label(B, i)
            vertex = G.vertices[i]
            if vertex not in I:
                if vertex.degree == chosenVertex.degree:
                    I.append(vertex)
                    num = num + count_isomorphism(G, D, I)
                    I.remove(vertex)

    D.remove(chosenVertex)
    return num


def test_countIsomorphism():

    with open("cubes3.grl") as f:
        G = load_graph(f, read_list = True)
    L = G[0][0]
    H = G[0][0]
    G = disjointUnion(L, H)
    print("Number of isomorphisms found: {}".format(count_isomorphism(G, [], [])))



# test_countIsomorphism()
