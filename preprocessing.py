def testNumberVertices(g1, g2):
    return len(g1.vertices) == len(g2.vertices)

def testNumberEdges(g1, g2):
    return len(g1.edges) == len(g2.edges)

def testDegrees(g1, g2):
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

def removeNoDegrees(G):
    for v in G.vertices:
        if v.degree == 0:
            G.del_vertex(v)
