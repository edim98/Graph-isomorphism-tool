from graph_io import load_graph, save_graph, write_dot
from graph import *
from refined_colouring import refine_colour, nicePrinting
import time

startTime = time.time()

with open('threepaths10240.gr') as f:
    G = load_graph(f)

res = refine_colour(G, [])

endTime = time.time()

print('Time taken : ', endTime - startTime)
# nicePrinting(res)
# print(G)
