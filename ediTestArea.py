from graph_io import load_graph, save_graph, write_dot
from graph import *
from refined_colouring import refine_colour, nicePrinting, colourGraph
from individualization import testDisjointUnion
import time

with open("test.gr") as f:
    G = load_graph(f)

# with open("test.gr") as f:
#     G = load_graph(f)
#
# with open("test.gr") as g:
#     H = load_graph(g)
#
startTime = time.time()
#
res = refine_colour(G, [])

#
# GuG = testDisjointUnion(G, H)
initial_colouring = [0]*(len(G))
initial_colouring[0] = 1
# # initial_colouring[10] = 1
initial_colouring[2] = 2
# # initial_colouring[13] = 2
# res = refine_colour(GuG, [])

endTime = time.time()

# newG = colourGraph(res, GuG)

with open("output.dot", "w") as x:
    # write_dot(newG, x)
    write_dot(G, x)
    # write_dot(GuG, x)
print('Time taken : ', endTime - startTime)
nicePrinting(res)
# print(G)
