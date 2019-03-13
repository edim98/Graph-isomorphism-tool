from graph_io import load_graph, save_graph, write_dot
from graph import *
from queue import Queue


def refine(C): # C is a DLL
    states = C.get_states()
    L = []
    A = [0]*(C.size)
    for q in states:
        neighbours = nx[q.label]
        for n in neighbours:
            if COLOUR[n.label] not in L:
                L.append(COLOUR[n.label])
                A[COLOUR[n.label]] += 1
            else:
                A[COLOUR[n.label]] += 1

    for colour in L:
        if A[colour] < dll[colour].size:
             l = smallest_free_colour()
            # TODO: split up dll[colour] in two groups and update data structures
            # keep in mind that it is redundant to iterate over the states again


class DLLEntry(object):

    def __init__(self, colour, state, vertex):
        self._colour = colour
        self._state = state
        self._vertex = vertex
        self._left = None
        self._right = None

    def set_states(self, states):
        self._states = states

    def set_left(self, left):
        self._left = left

    def set_right(self, right):
        self._right = right

    @property
    def vertex(self):
        return self._vertex

    @property
    def size(self):
        return len(self._states)

    @property
    def colour(self):
        return self._colour

    @property
    def state(self):
        return self._state

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right


class DLL(object):

    def __init__(self):
        self._start = None
        self._end = None
        self._colour = None
        self._size = 0

    @property
    def size(self):
        return self._size

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def colour(self):
        return self._colour

    def set_colour(self, colour):
        self._colour = colour

    def __repr__(self):
        if self.start is None:
            return ''
        s = 'Colour: ' + str(self.colour) +' '
        p = self.start

        while p != self.end:
            s += str(p.state)
            p = p.right
        s += str(self.end) + '\n'
        return s


    def add_state(self, vertex):
        entry = DLLEntry(self.colour, vertex.label, vertex)
        COLOUR[vertex.label] = self.colour
        if self.start is None:
            entry.set_right(entry)
            entry.set_left(entry)

            self._start = entry
            self._end = entry

        elif self.end == self.start:
            entry.set_left(self.start)
            entry.set_right(self.start)

            self.start.set_left(entry)
            self.start.set_right(entry)

            self._end = entry
        else:
            entry.set_left(self.end)
            entry.set_right(self.start)
            self.end.set_right(entry)
            self.start.set_left(entry)
            self._end = entry
        self._size += 1


    def get_states(self):
        res = []
        p = self.start
        while p != self.end:
            res.append(p)
        res.append(self.end)
        return res

def split_on_degrees(dll, graph):
    for i in graph.vertices:
        degree = i.degree
        dll[degree].add_state(i)

def build_nx(graph):
    res = [0]*(len(graph))
    for i in graph.vertices:
        res[i.label] = i.neighbours
    return res

def buildQueue(dll, ourQueue, INQUEUE):
    aux = []
    maxsize = 0
    maxpointer = 0
    k = 0
    for l in dll:
        if l.size > 0:
            if maxsize < l.size:
                maxsize = l.size
                maxpointer = k
            k += 1
            aux.append(l.colour)
    aux.pop(maxpointer)
    INQUEUE[maxpointer] = 0
    for i in aux:
        INQUEUE[i] = 1
        ourQueue.put(i)


with open('threepaths5.gr') as f:
    G = load_graph(f)

dll = []
for i in range(len(G)):
    dll.append(DLL())
    dll[i].set_colour(i)
split_on_degrees(dll, G)
print('dll: ', dll)
nx = build_nx(G)
print('nx: ', nx)
ourQueue = Queue()
INQUEUE = [0]*(len(G))
COLOUR = [0]*(len(G))
buildQueue(dll, ourQueue, INQUEUE)


print(ourQueue)
print(INQUEUE)


with open('output.dot', 'w') as g:
    write_dot(G, g)
