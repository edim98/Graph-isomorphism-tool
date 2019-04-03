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

def bijection(f1, f2):
    for i in range(0, len(f1)):
        if (f1[i] + f2[i]) != 2:
            return False
    return True


def balanced(f1, f2):
    for i in range(1, len(f1)):
        if f1[i] != f2[i]:
            return 0
    return 1


def get_max_color(colorings):
    res = []
    maxi = -math.inf
    for v, color in colorings.items():
        if color not in res:
            res.append(color)
            if color > maxi:
                maxi = color
    return maxi


def count_isomorphism(A, B, D, I):
    max_color = 1
    colorings1 = []
    colorings2 = []
    if D != [] and I != []:
        colorings1 = [0] * len(A.vertices)
        colorings2 = [0] * len(B.vertices)
        for i in A.vertices:
            if i not in D:
                colorings1[i.label] = 0
            else:
                colorings1[i.label] = max_color
                max_color += 1
        max_color = 1
        for i in B.vertices:
            if i not in I:
                colorings2[i.label] = 0
            else:
                colorings2[i.label] = max_color
                max_color += 1

    colorings1 = refine_colour(A, colorings1)
    colorings2 = refine_colour(B, colorings2)

    frequency1 = frequencies(colorings1)
    frequency2 = frequencies(colorings2)
    print(frequency1, frequency2)
    # if D != [] and I != []:
    if not balanced(frequency1, frequency2):
        return 0
    if bijection(frequency1, frequency2):
        return 1
    chosenColor = -1
    for i in range(len(frequency1)):
        if (frequency1[i] + frequency2[i]) >= 4:
            chosenColor = i
            break
    chosenVertex = None
    num = 0
    for i in range(len(colorings1)):
        if colorings1[i] == chosenColor:
            vertex = get_vertex_by_label(A, i)
            if vertex not in D:
                chosenVertex = vertex
                D.append(chosenVertex)
                break
    print(chosenVertex)
    for i in range(len(colorings2)):
        if colorings2[i] == chosenColor:
            vertex = get_vertex_by_label(B, i)
            if vertex not in I:
                I.append(vertex)
                num = num + count_isomorphism(A, B, D, I)
                I.remove(vertex)
    D.remove(chosenVertex)
    return num


def test_countIsomorphism():
    with open("cubes3.grl") as f:
        L = load_graph(f, read_list=True)
    g = L[0][0]
    h = L[0][1]
    print("Number of isomorphisms found: {}".format(count_isomorphism(g, h, [], [])))


test_countIsomorphism()