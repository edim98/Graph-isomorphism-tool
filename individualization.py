from refined_colouring import *

"""
File containing the first algorithm of counting isomorphisms.
Now it is mainly used for checking the existence of one such isomorphism. 
"""


def disjointUnion(G, H):
    """
    Procedure for the disjoint-union operation between two graphs.
    This is done by adding the vertices and edges of H to G.
    :param G: The first graph.
    :param H: The second graph.
    :return: The disjoint-union of the two graphs.
    """
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
    """
    Check for a bijection in a colour frequency list.
    :param f: The colour frequency list.
    :return: True if a bijection exists, false otherwise.
    """
    for i in range(len(f)):
        if f[i] != 2:
            return False
    return True


def balanced(f):
    """
    Check if a given colouring is balanced.
    :param f: The colouring as a frequency list.
    :return: True if the colouring is balanced, false otherwise.
    """
    for i in range(len(f)):
        if f[i] % 2 == 1:
            return 0
    return 1


def frequencies(colorings):
    """
    Procedure for computing the frequency of each colour in a given coloring.
    :param colorings: The given coloring.
    :return: An array of colour frequencies.
    """
    maxvalue = -1
    frequency = [0] * (len(colorings))
    for i in colorings:
        maxvalue = max(maxvalue, i)
        frequency[i] += 1
    frequency = frequency[:maxvalue + 1]

    return frequency


def count_isomorphism(G, D, I):
    """
    Procedure for finding at least one isomorphism in G = disjoint_union(g1, g2) that follow (D, I).
    :param G: The disjoint-union of two graphs.
    :param D: The list of chosen vertices from the first graph.
    :param I: The list of chosen vertices from the second graph.
    :return: 1 if there is at least one isomorphism (other than the trivial one), 0 otherwise.
    """
    max_color = 1
    colorings = [0] * len(G.vertices)
    dll = None

    if D != [] and I != []:  # If the lists are not empty, proceed to generate an inital colouring.
        for i in D:
            colorings[i.label] = max_color
            max_color += 1

        max_color = 1
        for j in I:
            colorings[j.label] = max_color
            max_color += 1

        colorings, dll = refine_colour(G, colorings)  # Refine the colour classes.

    frequency = frequencies(colorings)

    if not balanced(frequency):  # Not balanced, return.
        return 0

    if bijection(frequency):  # Isomorphism found, return.
        return 1

    chosenColor = -1   # Undecided, continue in choosing a branching colour class.
    for i in range(len(frequency)):
        if frequency[i] >= 4:
            chosenColor = i
            break

    chosenVertex = None
    lenG = len(G.vertices)  # Choose a branching vertex x.
    for i in range(lenG // 2):
        if colorings[i] == chosenColor:
            vertex = G.vertices[i]
            if vertex not in D:
                chosenVertex = vertex
                D.append(vertex)
                break

    for i in range(lenG // 2, lenG):  # Try different values for vertex y.
        if colorings[i] == chosenColor:
            vertex = G.vertices[i]
            if vertex not in I:
                if vertex.degree == chosenVertex.degree:
                    I.append(vertex)
                    res = count_isomorphism(G, D, I)
                    if res == 1:
                        return res
                    I.remove(vertex)
    D.remove(chosenVertex)
    return 0


def testIsomorphism(g1, g2):
    """
    Procedure called from 'main.py'.
    Check for the existence of at least one isomorphism between g1 and g2.
    :param g1: The first graph.
    :param g2: The second graph.
    :return: 1 if there is at least one isomorphism (other than the trivial one), 0 otherwise
    """
    G = disjointUnion(g1, g2)

    return count_isomorphism(G, [], [])
