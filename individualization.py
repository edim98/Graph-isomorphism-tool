from graphs.graph_io import load_graph
from project.coloring import *
import graphs.graph

from graphs.graph import Graph, Edge
from project.coloring import isomorph, coloring


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


def is_bijection(f1, f2):
    for i in range(1, len(f1)):
        if f1[i] == f2[i] and f1[i] == 1:
            continue
        else:
            return 0
    return 1


def frequencies(color1):
    maxvalue = -1
    for i in color1.values():
        maxvalue = max(maxvalue, i)
    frequency1 = [0]*(maxvalue + 1)

    for i in color1.values():
        frequency1[i] += 1
    return frequency1


def subgraph(G, D, I):
    R = Graph(False, 0)
    for i in D:
        for j in D:
            if i != j:
                if i.is_adjacent(j):
                    R.add_vertex(i)
                    R.add_vertex(j)
                    e = Edge(i, j)
                    R.add_edge(e)
    for i in I:
        for j in I:
            if i != j:
                if i.is_adjacent(j):
                    R.add_vertex(i)
                    R.add_vertex(j)
                    e = Edge(i, j)
                    R.add_edge(e)
    return R


def get_same_vertex(G, label):
    for g in G.vertices:
        if g.label == label:
            return g


def countIsomorphism(G, H, A=None, B=None, D=[], I=[],):
    if D == []:
        A = Graph(False, 1)
    if I == []:
        B = Graph(False, 1)

    beta_coloring = coloring(disjointUnion(A, B))
    frequencies1, frequencies2 = isomorph(G, H)
    is_unbalanced = (frequencies1 != frequencies2)
    freq = frequencies(beta_coloring)
    if is_unbalanced:
        return 0
    if is_bijection(frequencies1, frequencies2):
        return 1

    chosenColor = 0
    for i in range(len(freq)):
        if frequencies1[i] >= 4:
            chosenColor = i
            break
    for node, color in beta_coloring.items():
        if color == chosenColor or chosenColor == 0:
            nodeG = get_same_vertex(G, node.label)
            node_G = Vertex(A, nodeG.label)
            print("ia man")
            for g in G.vertices:
                if g == node_G:
                    continue
                if G.is_adjacent(node_G, g):
                    A.add_vertex(node_G)
                if A.find_edge(node_G, g) == None:
                    v = Vertex(A, g.label)
                    e = Edge(node_G, v)
                    A.add_edge(e)
            D.append(node)
            break

    num = 0

    for node, color in beta_coloring.items():
        if get_same_vertex(H, node.label) in H.vertices :
            # print("man ia")
            nodeH = get_same_vertex(H, node.label)
            print(beta_coloring.items())
            node_H = Vertex(B, nodeH.label)
            for g in H.vertices:
                if g == node_H:
                    continue
                if H.is_adjacent(node_H, g):
                    B.add_vertex(node_H)
                if B.find_edge(node_H, g) == None:
                    v = Vertex(B, g.label)
                    e = Edge(node_H, v)
                    B.add_edge(e)
            I.append(node)
            # print(I)
            num += countIsomorphism(G, H, A, B, D, I)
    return num

def test_countIsomorphism():
    with open("test_individualization/cubes3.grl") as f:
        L = load_graph(f, read_list=True)
    g = L[0][0]
    h = L[0][1]
    print("Number of isomorphisms found: {}".format(countIsomorphism(g, h)))


test_countIsomorphism()

