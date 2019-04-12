from graph_io import load_graph, save_graph, write_dot
from graph import *
from refined_colouring import refine_colour
from automorphismGenerator import generateAutomorphism, compute_order
from individualization import count_isomorphism, disjointUnion
from permv2 import *
import time
import os
from individualization import testIsomorphism

abspath = os.path.abspath('.\\graphs\\torus24.grl')

with open(abspath) as f:
    G = load_graph(f, read_list = True)
g1 = G[0][0]
with open(abspath) as f:
    G = load_graph(f, read_list = True)
g2 = G[0][0]
#
startTime = time.time()

refine_colour(g1, [])

endTime = time.time()


print('Time taken : ', endTime - startTime)
# nicePrinting(res)
# print(G)
