from graph_io import load_graph, save_graph, write_dot
from graph import *
from queue import Queue
import time


# TODO LIST:
# * Change deletion of DLLEntry in a DLL object (use a data structure pointer where pointer[vertex] = DLLEntry which has that vertex) -- done :)
# * Optimize methods in "graph.py" (eg. change lists to heaps)
# * Check for redundant code
# * Change split_on_degrees to split_on_initial_colouring (andrei's code) -- done
# * Add a main refine_colour(G) method so it can be called outside this file ?? done (hopefully)


# with open('colorref_smallexample_4_7.grl') as f:
# with open('colorref_smallexample_2_49.grl') as f:
# with open('threepaths10240.gr') as f:
# # with open('test.gr') as f:
#     Glist = load_graph(f, read_list = True)

# ------- Start of Data structures -------
pointer = []
dll = [] # List of DLL objects
nx = [] # List of neighbours
INQUEUE = [] # Keep track of elements in queue
COLOUR = [] # Keep track of the colour of each vertex
ourQueue = Queue() # Working queue

# ------- End of Data structures -------


# G = Glist[0][0]
#
# with open('output.dot', 'w') as g:
#     write_dot(G, g)

# startTime = time.time()






class DLLEntry(object):

    # Constructor for a DLL entry
    # Params:
    # colour: colour of the DLLEntry
    # state: state of the DLLEntry
    # vertex: number of the DLLEntry vertex
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

    # Return the number of states
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

    # Constructor for the Dynamic-Linked-List object
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

    def set_start(self, start):
        self._start = start

    def set_end(self, end):
        self._end = end

    def set_size(self, size):
        self._size = size

    # String representation of the DLL
    def __repr__(self):
        if self.start is None:
            return ''
        s = 'Colour ' + str(self.colour) +': '
        p = self.start

        while p != self.end:
            s += str(p.state) + ' '
            p = p.right
        s += str(self.end.state) + '\n'
        return s

    # Removes a state from this DLL
    def remove_state(self, vertex):
        p = pointer[vertex.label]
        if p is not None:
            if self.size == 1: # If the size of the list is 1
                self.set_start(None) # Set all fields as none
                self.set_end(None)
                self.set_size(0) # Set size as 0

            elif self.size == 2: # If only two elements are in the list
                self.set_start(p.right) # Set start and end at the element not deleted
                self.set_end(p.right)
                p.left.set_right(p.right)
                p.right.set_left(p.left)

                self.set_size(1) # Set size to 1
            else: # Multiple elements
                p.left.set_right(p.right) # Change left / right relationships
                p.right.set_left(p.left)
                if self.start == p:
                    self.set_start(self.start.right)
                if self.end == p:
                    self.set_end(self.end.left)
                self.set_size(self.size - 1)

            p = None # Delete entry
            pointer[vertex.label] = None
            return


    # Adds a state to the DLL
    def add_state(self, vertex):
        entry = DLLEntry(self.colour, vertex.label, vertex) # Create a new entry
        COLOUR[vertex.label] = self.colour # Keep track of the vertex's colour in a separate list

        if self.start is None: # If the list is empty
            entry.set_right(entry) # Set the left most and right most entry as this new one.
            entry.set_left(entry)

            self._start = entry
            self._end = entry

        elif self.end == self.start: # If there is only one element
            entry.set_left(self.start) # Set the left and right of this entry to the start
            entry.set_right(self.start)

            self.start.set_left(entry)
            self.start.set_right(entry)

            self._end = entry # The end is now the new entry

        else: # If there are multiple entries
            entry.set_left(self.end) # Set left to end, right to start
            entry.set_right(self.start)
            self.end.set_right(entry)
            self.start.set_left(entry)
            self._end = entry # The end is now the new entry.

        self._size += 1 # Increment size of DLL
        pointer[vertex.label] = entry

    # Return the states of this list
    def get_states(self):
        res = []
        p = self.start
        while p != self.end:
            res.append(p)
            p = p.right
        res.append(self.end)
        return res

# Split the vertices on initial colouring (based on Andrei's code)
def split_on_initial_colouring(dll, graph, initial_colouring):
    if initial_colouring == []:
        for i in graph.vertices: # Split the nodes on their degree.
            degree = i.degree
            dll[degree].add_state(i) # Add this vertix to the dll with colour "degree"
    else: # Split the nodes on initial colouring
        for i in range(len(initial_colouring)):
            dll[initial_colouring[i]].add_state(graph.vertices[i])


# Build the "nx" list - keep track of the list of neighbours for each vertix
def build_nx(graph):
    for i in graph.vertices:
        nx[i.label] = i.neighbours

# Build our working queue
def buildQueue(dll, ourQueue, INQUEUE):
    aux = []
    maxsize = 0
    maxpointer = 0
    k = 0
    diffColours = 0
    for l in dll:
        if l.size > 0:
            if maxsize < l.size:
                maxsize = l.size
                maxpointer = k # Keep track of the position of the dll with largest number of elements
            k += 1
            diffColours += 1
            aux.append(l.colour) # Add each list to the queue
    if diffColours > 1:
        aux.pop(maxpointer) # Remove the list with largest number of elements.
    INQUEUE[maxpointer] = 0
    for i in aux:
        INQUEUE[i] = 1 # Keep track of elements in queue
        ourQueue.put(i)

# Print the DLL objects in a nice way :)
def nicePrinting(dll):
    for d in dll:
        if d.size > 0:
            print(d)

def colourGraph(dll, G):
    for d in dll:
        if d.size > 0:
            p = d.start
            while p != d.end:
                G.vertices[p.state].colornum = d.colour
                # print(G.vertices[p.state-1].colornum)
                p = p.right
            G.vertices[d.end.state].colornum = d.colour
    return G

def smallest_free_colour():
    for d in dll:
        if d.size == 0 and d.colour != 0:
            return d.colour
    dll.append(DLL())
    length = len(dll)
    dll[length - 1].set_colour(length - 1)
    return length - 1


def refine(C, G): # C is a DLL
    states = C.get_states()
    L = []
    visited = []
    A = [0]*(len(G))
    for q in states:
        neighbours = nx[q.vertex.label]
        for n in neighbours:
            if COLOUR[n.label] != C.colour:
                if COLOUR[n.label] not in L:
                    L.append(COLOUR[n.label])
                    visited.append(n)
                    A[COLOUR[n.label]] += 1
                if n not in visited:
                    visited.append(n)
                    A[COLOUR[n.label]] += 1 # !!! Check to not count duplicates

    for colour in L:
        if A[colour] < dll[colour].size: # Split up "colour"
             l = smallest_free_colour() # Get the smallest free colour
             for v in visited: # Iterate over found neighbours
                 if COLOUR[v.label] == colour: # Check that they belong to the respective colour class
                     dll[colour].remove_state(v)
                     dll[l].add_state(v) # Add vertex to the DLL object
             if dll[colour].size < dll[l].size:
                 ourQueue.put(colour)
             else:
                 ourQueue.put(l)


            # If this happens, then split up dll[colour] by adding the vertices with colour "colour" to a new DLL

def refine_colour(G, initial_colouring):
    global dll
    global INQUEUE
    global COLOUR
    global pointer
    global nx

    dll = []
    INQUEUE = []
    COLOUR = []
    pointer = []
    nx = []

    for i in range(len(G)):
        dll.append(DLL()) # Populate the empty list with DLL objects
        dll[i].set_colour(i) # Set the colour of each DLL object
        INQUEUE.append(0)
        COLOUR.append(-1)
        pointer.append(None)
        nx.append(None)

    split_on_initial_colouring(dll, G, initial_colouring) # Add vertices based on degrees

    build_nx(G) # Construct the list of neighbours for each vertix

    buildQueue(dll, ourQueue, INQUEUE)

    i = 1
    while not ourQueue.empty():
        currentColour = ourQueue.get()
        # print('Refining with current colour: ', currentColour)
        refine(dll[currentColour], G)
        i = i + 1

    return dll
