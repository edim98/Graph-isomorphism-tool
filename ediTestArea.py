from graph_io import load_graph, save_graph, write_dot
from graph import *
from refined_colouring import refine_colour
from automorphismGenerator import generateAutomorphism, compute_order, is_permutation_new
from individualization import count_isomorphism, disjointUnion
from permv2 import *
import time
import os
from individualization import testIsomorphism

abspath = os.path.abspath('.\\graphs\\bigtrees3.grl')

with open(abspath) as f:
    G = load_graph(f, read_list = True)
g1 = G[0][1]
with open(abspath) as f:
    G = load_graph(f, read_list = True)
g2 = G[0][3]
#
startTime = time.time()

print(testIsomorphism(g1, g2))

endTime = time.time()


# with open("g1.dot", "w") as x:
#     write_dot(g1, x)
# with open("g2.dot", "w") as x:
#     write_dot(g2, x)
# with open("output.dot", "w") as x:
#     write_dot(GuG, x)
# with open("output2.dot", "w") as x:
#     write_dot(GuG2, x)
    # write_dot(GuG, x)
print('Time taken : ', endTime - startTime)
# nicePrinting(res)
# print(G)
