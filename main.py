from automorphismGenerator import countAutomorphism
from individualization import testIsomorphism
from graph_io import *
from graph import *
from preprocessing import *
import os
import time, getopt


"""
---------------> Main file <----------------
--> Graph Isomorphism Check and |Aut(G)| <-
--------------------------------------------
"""


def readFromFile(file):
    """
    Read from a specified file.
    :param file: The file to read from.
    :param is_list: Flag for reading a graph list.
    :return: The graph list / object read from the file.
    """
    abspath = os.path.abspath(file)
    with open(file) as f:
        G = load_graph(f, read_list = True)
    return G[0]


def initialTest(g1, g2):
    """
    Attempt to pass the initial checkings.
    If one of the test is not passed, abort since there is no possible isomorphism.
    :param g1: The first graph.
    :param g2: The second graph.
    :return: True if the graphs pass the tests. False, otherwise.
    """
    return testNumberVertices(g1, g2) and testNumberEdges(g1, g2) and testDegrees(g1, g2)


def main(argv):
    """
    Main procedure for handling user input and running the required tasks.
    """

    file = '.\\graphs\\'  # File path.
    testIsomorphismFlag = ''  # Flag for running the graph isomorphism procedure.
    countAutomorphismFlag = '' # Flag for running the automorphisms count procedure.
    totalTime = 0

    try:
        opts, args = getopt.getopt(argv, "hi:g:c:", ["input_file=", "graph_iso=", "count_auto="])
    except getopt.GetoptError:
        print("Usage: main.py -i <input_file> -g <1 / 0> -c <1 / 0>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("Usage: main.py -i <input_file> -L <1 / 0> -g <1 / 0> -c <1 / 0>")
            print("-i or --input_file=  <-> specifies the name of the file with extension eg. \"torus24.grl\" or \"threepaths160.gr\"")
            print('-g or --graph_iso=   <-> set to 1 if you want to run the graph isomorphism test, set to 0 if not')
            print('-c or --count_auto=  <-> set to 1 if you want to count the number of automorphisms, set to 0 if not')
            sys.exit()
        elif opt in("-i", "--input_file"):
            file += arg
        elif opt in("-g", "--graph_iso"):
            testIsomorphismFlag = arg
        elif opt in("-c", "--count_auto"):
            countAutomorphismFlag = arg

    if file == '.\\graphs\\':
        print("Please make sure to add a file!\nUsage: main.py -i <input_file> -g <1 / 0> -c <1 / 0>")
        sys.exit(2)

    if testIsomorphismFlag == '1':
        graphs = readFromFile(file)

        isoClasses = []  # Keep track of found isomorphisms.
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
                        totalTime += endTime - startTime

                        if status == 1:
                            print('Graphs {} and {} are isomorphic!\t\t{}'.format(i, j, endTime - startTime))
                            isoClasses[i].append(j)
                            isoClasses[j].append(i)
                        else:
                            print('Graphs {} and {} are not isomorphic...\t\t{}'.format(i, j, endTime - startTime))

        for i in range(len(isoClasses)):
            print('Isomorphic with {}: {}'.format(i, isoClasses[i]))

    if countAutomorphismFlag == '1':
        print('Graph \t#Aut\tTime taken')
        graphs = readFromFile(file)
        graphs2 = readFromFile(file)
        for i in range(len(graphs)):
            g1 = graphs[i]
            g2 = graphs2[i]

            startTime = time.time()
            res = countAutomorphism(g1, g2)
            endTime = time.time()
            print('%d:\t\t%d\t\t%f'%(i, res, endTime - startTime))
            totalTime += endTime - startTime

    print('Finished! Total time taken = {}'.format(totalTime))


if __name__ == "__main__":
    main(sys.argv[1:])