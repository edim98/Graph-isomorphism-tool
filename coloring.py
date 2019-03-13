from graphs.graph_io import load_graph, save_graph, write_dot
from graphs.graph import *


def neighbourscolour(v):
    result = []
    for i in v.neighbours:
        result.append(i.colornum)
    for i in range(len(result)):
        for j in range(len(result)):
            if result[i] > result[j]:
                result[i], result[j] = result[j], result[i]
    return result

def coloring(G):
    colour = {}
    maxcolour = 0
    for i in G.vertices:
        i.colornum = 1
        colour[i] = i.colornum
        maxcolour = max(maxcolour, i.colornum)
    copy = {}
    visited = {}
    while copy != colour:
        copy = colour.copy()
        for i in G.vertices:
            for j in G.vertices:
                if i != j and i.colornum == j.colornum:
                    list1 = neighbourscolour(i)
                    list2 = neighbourscolour(j)
                    if list2 == list1 and copy[i] == copy[j]:
                        # visited[copy[i]] = list1
                        colour[i] = copy[i]
                        colour[j] = copy[j]
                    else:
                        if list2 not in visited.values():
                            maxcolour += 1
                            visited[maxcolour] = list2
                            j.colornum = maxcolour
                            colour[j] = j.colornum
                        else:
                            for color, list3 in visited.items():
                                if list3 == list2:
                                    j.colornum = color
                                    colour[j] = j.colornum
    return colour


def isomorph(G, G2):
    color1 = coloring(G)
    color2 = coloring(G2)
    maxvalue = -1
    for i in color1.values():
        maxvalue = max(maxvalue, i)
    frequency1 = [0]*(maxvalue + 1)

    maxvalue = -1
    for i in color2.values():
        maxvalue = max(maxvalue, i)
    frequency2 = [0]*(maxvalue + 1)

    for i in color1.values():
        frequency1[i] += 1

    for i in color2.values():
        frequency2[i] += 1
    return frequency1, frequency2
