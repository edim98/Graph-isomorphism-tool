"""
Preprocessing operations are executed before running the main algorithm.
A false result in any of these checks ensures that no isomorphism can exist between two given graphs.
"""


def testNumberVertices(g1, g2):
    """"
    Check if the graphs have an equal number of vertices.
    :param g1: The first graph.
    :param g2: The second graph.
    :return: True if both graphs have the same number of vertices. False, otherwise.
    """
    return len(g1.vertices) == len(g2.vertices)


def testNumberEdges(g1, g2):
    """"
    Check if the graphs have an equal number of edges.
    :param g1: The first graph.
    :param g2: The second graph.
    :return: True if both graphs have the same number of vertices. False, otherwise.
    """
    return len(g1.edges) == len(g2.edges)

def testDegrees(g1, g2):
    """
    Check if the graphs have the same number of vertices of different degrees.
    :param g1: The first graph.
    :param g2: The second graph.
    :return: True if both graphs have the same number of vertices of different degrees. False, otherwise.
    """
    degreesG1 = [0] * len(g1.vertices)
    degreesG2 = [0] * len(g2.vertices)
    for v in g1.vertices:
        degreesG1[v.degree] += 1
    for v in g2.vertices:
        degreesG2[v.degree] += 1

    for d in range(len(degreesG1)):
        if degreesG1[d] != degreesG2[d]:
            return False
    return True