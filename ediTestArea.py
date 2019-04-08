from graph_io import load_graph, save_graph, write_dot
from graph import *
from refined_colouring import refine_colour
from individualization import count_isomorphism, disjointUnion, disjointUnionCata
import time

with open("Autom3.grl") as f:
    G = load_graph(f, read_list = True)

# with open("test2.gr") as g:
    # G = load_graph(g)

g1 = G[0][0]
g2 = G[0][1]
#
startTime = time.time()

# print(count_isomorphism(g1, g2, [], []))

GuG = disjointUnion(g1, g2)

endTime = time.time()


# with open("g1.dot", "w") as x:
#     write_dot(g1, x)
# with open("g2.dot", "w") as x:
#     write_dot(g2, x)
with open("output.dot", "w") as x:
    write_dot(GuG, x)
# with open("output2.dot", "w") as x:
#     write_dot(GuG2, x)
    # write_dot(GuG, x)
print('Time taken : ', endTime - startTime)
# nicePrinting(res)
# print(G)
