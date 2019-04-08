from permv2 import *
from basicpermutationgroup import *
from permutation.ex5 import period2 as period
from graph import *
from individualization import disjointUnion

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
    
def test_compute_order():
    p = permutation(6, cycles=[[0,1,2],[4,5]])
    q = permutation(6, cycles=[[0],[1],[2],[2,3],[4],[5]])
    H = [p, q]
    G = Graph(False, 6)
    print("Order:",compute_order(H, G))


def get_color_classes(frequency):
    max_color = None
    max_value = -1
    for i in range(len(frequnecy)):
        if frequency[i] > max_value and frequency[i] >= 2:
            max_value = frequency[i]
            max_color = i
    return max_color


def chosen_color_class(color):


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

    big_color_classes = get_color_classes(coloring) # |C| >=2 or |C| >=4 #TODO
    chosen_color = choose_color_class(big_color_classes) # Try big ones first. #TODO
    chosen_vertex = choose_vertext(chosen_color) # Random choice is still OK. Try not to choose a previous node # TODO

    nodes_visited.append(chosen_vertex)
    y = chosen_vertex # first try y == x ("if possible"?)
    D.append(chosen_vertex)
    I.append(y)
    coloring = disjoint_union.get_coloring(D, I) # get_coloring() equivalent
    generate_automorphism(G1, G2, D, I, coloring, nodes_visited, generator)
    chosen_color.remove(chosen_vertex) # try the rest of the nodes in that color class
    for j in G2.vertices: #TODO: the .vertices stuff somehow
        if j.colornum == chosen_color:
            I.append(j)
            coloring = disjoint_union.get_coloring(D, I) # get_coloring() equivalent
            generate_automorphism(G1, G2, D, I, coloring, nodes_visited, generator)
            I.remove(j)

    return generator
