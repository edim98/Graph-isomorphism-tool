import math

from graph_io import *
from coloring import *
from refined_colouring import *

def disjointUnion(self, H):
    lenG = len(self.vertices)
    lenH = len(H.vertices)
    eG = self.edges
    eH = H.edges
    R = Graph(False, lenG + lenH)

    for i in range(lenG):
        for j in range(i, lenG):
            if self.vertices[i].is_adjacent(self.vertices[j]):
                edge_g = Edge(self.vertices[i], self.vertices[j])

                for e in eG:
                    if edge_g.tail == e.tail and edge_g.head == e.head:
                        edge = Edge(R.vertices[j], R.vertices[i])
                        R.add_edge(edge)
                        # print("!G: connect edge {} and edge {}".format(j, i))
                    elif edge_g.tail == e.head and edge_g.head == e.tail:
                        edge = Edge(R.vertices[i], R.vertices[j])
                        R.add_edge(edge)
                        # print("G: connect edge {} and edge {}".format(i, j))

    for i in range(lenH):
        for j in range(i, lenH):
            if H.vertices[i].is_adjacent(H.vertices[j]):
                edge_h = Edge(H.vertices[i], H.vertices[j])

                for e in eH:
                    if edge_h.tail == e.tail and edge_h.head == e.head:
                        edge = Edge(R.vertices[lenG + j], R.vertices[lenG + i])
                        R.add_edge(edge)
                        # print("!H: connect edge {} and edge {}".format(j, i))
                    elif edge_h.tail == e.head and edge_h.head == e.tail:
                        edge = Edge(R.vertices[lenG + i], R.vertices[lenG + j])
                        R.add_edge(edge)
                        # print("H: connect edge {} and edge {}".format(i, j))

    return R


def get_vertex_by_label(G, label):
    for i in G.vertices:
        if i.label == label:
            return i

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



test_countIsomorphism()
