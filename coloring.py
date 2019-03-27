from graph_io import load_graph, save_graph, write_dot
from graph import *


def neighbourscolour(v):
    result = []
    for i in v.neighbours:
        result.append(i.colornum)
    for i in range(len(result)):
        for j in range(len(result)):
            if result[i] > result[j]:
                result[i], result[j] = result[j], result[i]
    return result

def coloring(G, colors = {}):
    colour = {}
    maxcolour = -1
    if colors == {}:
        for i in G.vertices:
            i.colornum = 1
            colour[i] = i.colornum
            maxcolour = max(maxcolour, i.colornum)
    else:
        colour = colors
        for i in G.vertices:
            if i in colour:
                i.colornum = colour[i]
            else:
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
                    if list1 != list2:
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


def frequencies(color1):
    maxvalue = -1
    for i in color1.values():
        maxvalue = max(maxvalue, i)
    frequency1 = [0]*(maxvalue + 1)

    for i in color1.values():
        frequency1[i] += 1

    return frequency1


def test_countIsomorphism():
    with open("colorref_smallexample_4_7.grl") as f:
        L = load_graph(f, read_list=True)
    g = L[0][3]
    h = L[0][1]

    c1 = coloring(g)
    c2 = coloring(h)

    print(frequencies(c1))
    print(frequencies(c2))
    print(frequencies(c1) == frequencies(c2))
    with open("graph.dot", "w") as w:
        write_dot(h, w)
# test_countIsomorphism()