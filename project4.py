from permv2 import *
from basicpermutationgroup import *
from permutation.ex5 import period2 as period
from graph import *

def compute_order(H, G):
    alpha = None
    order_alpha = -1
    k = len(H)
    if k == 1:
        return period(list(H[0]))
    for v in G.vertices:
        alpha_H = Orbit(H, v.label)
        if len(alpha_H) >= 2:
            order_alpha = len(alpha_H)
            alpha = v.label
            break

    H_alpha = Stabilizer(H, alpha)
    return order_alpha * compute_order(H_alpha, G)


def is_permutation_new(f, H, G):
    alpha = None
    transversal = None
    if len(H) == 1 and H[0].is_trivial():
        if f.is_trivial():
            return "yes"
        else:
            return "no"

    for v in G.vertices:
        alpha_H, transversal = Orbit(H, v.label, True)
        if len(alpha_H) >= 2:
            alpha = v.label
            break

    beta = f * alpha
    if beta not in alpha_H:
        return "yes"
    else:
        composition = (-transversal[beta]) * f
        H_alpha = Stabilizer(H, alpha)
        return is_permutation_new(composition, H_alpha, G)

def generateAutomorphism(G, D, I, X):
    max_color = 1
    colorings = [0] * len(G.vertices)
    if D != [] and I != []:
        for i in D:
            colorings[i.label] = max_color
            max_color += 1


        max_color = 1
        for j in I:
            colorings[j.label] = max_color
            max_color += 1
        colorings = refine_colour(G, colorings)

    frequency = frequencies(colorings)

    if not balanced(frequency): # no auto that follows (D, I)
        # return 0, 0
        return X

    if bijection(frequency): # follows (D, I)
        # if trivial(D, I):
        #     return 1, 0
        # return 1, 1
        f = create_permutation(D, I)
        if is_permutation_new(f, X, G):
            X.append(f)
        return X

    chosenColor = -1
    for i in range(len(frequency)):
        if frequency[i] >= 4:
            chosenColor = i
            break
    num = 0

    chosenVertex = None
    lenG = len(G.vertices)
    for i in range(len(colorings)):
        if colorings[i] == chosenColor and i >= 0 and i < lenG//2:
            vertex = G.vertices[i]
            if vertex not in D:
                chosenVertex = vertex
                D.append(vertex)
                break

    for i in range(len(colorings)):
        if colorings[i] == chosenColor and i >= lenG//2 and i < lenG:
            vertex = G.vertices[i]
            if vertex not in I:
                if vertex.degree == chosenVertex.degree:
                    I.append(vertex)
                    generateAutomorphism(G, D, I, X)
                    # if trivialJump:
                    #     if not trivial(D, I):
                    #         I.remove(vertex)
                    #         break
                    I.remove(vertex)
    D.remove(chosenVertex)

    return X

def generate_automorphism(G1, G2, D, I, coloring, nodes_visited, generator=[]):
    if coloring.is_unbalanced(D, I): #TODO
        # There is no automorphism that follows (D, I)!
        return "No automorphism found: Coloring is unbalanced."

    current_node = nodes_visited[len(nodes_visited)-1]
    disjoint_union = disjointUnion(G1, G2)
    if coloring.defines_bijection():
        # There exists a unique automorphism that follows (D, I)!
        f = coloring.to_permutation(G1, G2) #TODO
        if is_permutation_new(f, generator, G1):
            generator.append(f)

            for i in range(len(nodes_visited)-2, -1, -1):
                if nodes_visited[i].is_ancestor_of(current_node): #TODO: .is_ancestor_of (possibly a tree structure or something)
                    nodes_visited = nodes_visited[:i]
                    D = D[:i]
                    I = I[:i] #might not keep I accurate
                    coloring = disjoint_union.get_coloring(D, I) # get_coloring() equivalent

                    generate_automorphism(G1, G2, D, I, coloring, nodes_visited, generator)
                    break

    big_color_classes = get_color_classes(coloring, 2) # |C| >=2 or |C| >=4 #TODO
    chosen_color = choose_color_class(big_color_classes) # Try big ones first. #TODO
    chosen_vertex = choose_vertext(chosen_color) # Random choice is still OK. Try not to choose a previous node # TODO

    nodes_visited.append(chosen_vertex)
    y = chosen_vertex # first try y == x ("if possible"?)
    D.append(chosen_vertex)
    I.append(y)
    coloring = disjoint_union.get_coloring(D, I) # get_coloring() equivalent
    generate_automorphism(G1, G2, D, I, coloring, nodes_visited, generator)
    chosen_color.remove(chosen_vertex) # try the rest of the nodes in that color class
    for j in chosen_color.vertices: #TODO: the .vertices stuff somehow
        I.append(j)
        coloring = disjoint_union.get_coloring(D, I) # get_coloring() equivalent
        generate_automorphism(G1, G2, D, I, coloring, nodes_visited, generator)

    return generator

def test_compute_order():
    p = permutation(6, cycles=[[0,1,2],[4,5]])
    q = permutation(6, cycles=[[0],[1],[2],[2,3],[4],[5]])
    H = [p, q]
    G = Graph(False, 6)
    print(is_permutation_new(p, H, G))
    print("Order:",compute_order(H, G))
<<<<<<< HEAD

def generate_automorphism(G1, G2, D, I, coloring, nodes_visited, generator=[]):
    if coloring.is_unbalanced(D, I): #TODO
        # There is no automorphism that follows (D, I)!
        return "No automorphism found: Coloring is unbalanced."

    current_node = nodes_visited[len(nodes_visited)-1]
    disjoint_union = disjointUnion(G1, G2)
    if coloring.defines_bijection():
        # There exists a unique automorphism that follows (D, I)!
        f = coloring.to_permutation(G1, G2) #TODO
        if is_permutation_new(f, generator, G1):
            generator.append(f)

            for i in range(len(nodes_visited)-2, -1, -1):
                if nodes_visited[i].is_ancestor_of(current_node): #TODO: .is_ancestor_of (possibly a tree structure or something)
                    nodes_visited = nodes_visited[:i]
                    D = D[:i]
                    I = I[:i] #might not keep I accurate
                    coloring = disjoint_union.get_coloring(D, I) # get_coloring() equivalent

                    generate_automorphism(G1, G2, D, I, coloring, nodes_visited, generator)
                    break

    big_color_classes = get_color_classes(coloring, 2) # |C| >=2 or |C| >=4 #TODO
    chosen_color = choose_color_class(big_color_classes) # Try big ones first. #TODO
    chosen_vertex = choose_vertext(chosen_color) # Random choice is still OK. Try not to choose a previous node # TODO

    nodes_visited.append(chosen_vertex)
    y = chosen_vertex # first try y == x ("if possible"?)
    D.append(chosen_vertex)
    I.append(y)
    coloring = disjoint_union.get_coloring(D, I) # get_coloring() equivalent
    generate_automorphism(G1, G2, D, I, coloring, nodes_visited, generator)
    chosen_color.remove(chosen_vertex) # try the rest of the nodes in that color class
    for j in chosen_color.vertices: #TODO: the .vertices stuff somehow
        I.append(j)
        coloring = disjoint_union.get_coloring(D, I) # get_coloring() equivalent
        generate_automorphism(G1, G2, D, I, coloring, nodes_visited, generator)

    return generator
=======
>>>>>>> 1cb146890dd86a5a667ef1779dedac96a176df87
