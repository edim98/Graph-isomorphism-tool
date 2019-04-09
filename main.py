from automorphismGenerator import countAutomorphism
from individualization import testIsomorphism
from graph_io import *
from graph import *
from preprocessing import *
import os
import time



def readFromFile(file):
    abspath = os.path.abspath(file)
    with open(file) as f:
        G = load_graph(f, read_list = True)
    return G[0]


def initialTest(g1, g2):
    return testNumberVertices(g1, g2) and testNumberEdges(g1, g2) and testDegrees(g1, g2)

if __name__ == '__main__':
    file = '.\\graphs\\cubes6.grl'
    testIsomporphismFlag = True
    countAutomorphismFlag = False

    if testIsomporphismFlag:


        graphs = readFromFile(file)
        # isoClasses = [[]] * len(graphs)
        isoClasses = []
        for i in range(len(graphs)):
            isoClasses.append([])
        for i in range(len(graphs)):
            for j in range(i+1, len(graphs)):
                if (not i in isoClasses[j]) and (not j in isoClasses[i]):
                    graphs2 = readFromFile(file)
                    g1 = graphs2[i]
                    g2 = graphs2[j]

                    if not initialTest(g1, g2):
                        print('Graphs {} and {} did not pass the initial test...'.format(i, j))
                    else:
                        startTime = time.time()
                        status = testIsomorphism(g1, g2)
                        endTime = time.time()

                        if status == 1:
                            print('Graphs {} and {} are isomorphic!\t\t{}'.format(i, j, endTime - startTime))
                            isoClasses[i].append(j)
                            isoClasses[j].append(i)
                        else:
                            print('Graphs {} and {} are not isomorphic...\t\t{}'.format(i, j, endTime - startTime))

        for i in range(len(isoClasses)):
            print('Isomorphic with {}: {}'.format(i, isoClasses[i]))

    if countAutomorphismFlag:
        print('Graph \t#Aut\tTime taken')
        graphs = readFromFile(file)
        graphs2 = readFromFile(file)
        for i in range(len(graphs)):
            g1 = graphs[i]
            g2 = graphs2[i]

            startTime = time.time()
            print('%d:\t\t%d\t\t%f'%(i, countAutomorphism(g1, g2), time.time() - startTime))
