from graph import *
from queue import Queue

"""
Fast colour refinement implementation.
Based on the algorithm ideas of Lecture 2 & 3. 
"""


# ------- Start of Data structures -------
pointer = []  # List of pointers for each vertex.
dll = []  # List of DLL objects.
nx = []  # List of neighbours for each vertex.
COLOUR = []  # List of colours for each vertex.
ourQueue = Queue()  # Working queue.

# ------- End of Data structures -------


class DLLEntry(object):
    """
    A dynamic-linked-list entry object is used for building and working with the dynamic-linked-list object.
    Thus, it is required to keep track of the 'left' and 'right' elements next to this entry.
    This object is a representation of a 'state'.
    """

    def __init__(self, colour, state, vertex):
        """
        Constructor of a DLLEntry object.
        :param colour: The colour of the state.
        :param state: The integer identifier of the state.
        :param vertex: The Vertex object associated with this state.
        """

        self._colour = colour
        self._state = state
        self._vertex = vertex
        self._left = None
        self._right = None

    def set_state(self, state):
        """
        Basic setter for value of the state.
        :param state: The new state value.
        """
        self._state = state

    def set_left(self, left):
        """
        Basic setter for the pointer to the left element.
        :param left: The pointer to the left element.
        """
        self._left = left

    def set_right(self, right):
        """
        Basic setter for the pointer to the right element.
        :param right: The pointer to the right element.
        """
        self._right = right

    @property
    def vertex(self):
        """
        Vertex property.
        :return: The Vertex object associated with this entry.
        """
        return self._vertex

    @property
    def colour(self):
        """
        Colour property.
        :return: The colour of this entry.
        """
        return self._colour

    @property
    def state(self):
        """
        State property.
        :return: The integer identifier of this entry.
        """
        return self._state

    @property
    def left(self):
        """
        Left element property.
        :return: A pointer to the entry found to the left of this one.
        """
        return self._left

    @property
    def right(self):
        """
        Right element property.
        :return: A pointer to the entry found to the right of this one.
        """
        return self._right


class DLL(object):
    """
    The dynamic-linked-list object manages several DLLEntry objects.
    The DLL object is useful for faster insertion, deletion and moving of elements.
    At any point in time: start.left = end AND end.right = start.
    """

    def __init__(self):
        """
        Constructor of a DLL object.
        """
        self._start = None
        self._end = None
        self._colour = None
        self._size = 0

    @property
    def size(self):
        """
        Size property.
        :return: The number of DLLEntry objects found in this list.
        """
        return self._size

    @property
    def start(self):
        """
        Start property.
        :return: A pointer to the first element in the list.
        """
        return self._start

    @property
    def end(self):
        """
        End property.
        :return: A pointer to the last element in the list.
        """
        return self._end

    @property
    def colour(self):
        """
        Colour property.
        :return: The colour of this object. This colour is equal to the colour of all DLLEntry objects in this list.
        """
        return self._colour

    def set_colour(self, colour):
        """
        Basic setter for the colour of the object.
        :param colour: The new colour.
        """
        self._colour = colour

    def set_start(self, start):
        """
        Basic setter for the start element of the list.
        :param start: The pointer to the new starting element.
        """
        self._start = start

    def set_end(self, end):
        """
        Basic setter for the end element of the list.
        :param end: The pointer to the new ending element.
        """
        self._end = end

    def set_size(self, size):
        """
        Basic setter for the size of the object.
        :param size: The new size of the object.
        """
        self._size = size

    def __repr__(self):
        """
        String representation of this object.
        :return:
        """
        if self.start is None:
            return ''
        s = 'Colour ' + str(self.colour) +': '
        p = self.start

        while p != self.end:
            s += str(p.state) + ' '
            p = p.right
        s += str(self.end.state) + '\n'
        return s

    def remove_state(self, vertex):
        """
        Remove a DllEntry from this list.
        This is done using 3 separate cases described bellow.
        :param vertex: The Vertex to be removed.
        """
        p = pointer[vertex.label]

        if p is not None:
            if self.size == 1:  # If the size of the list is 1:
                self.set_start(None)  # Set all fields as none.
                self.set_end(None)
                self.set_size(0)  # Set size as 0

            elif self.size == 2:  # If only two elements are in the list:
                self.set_start(p.right)  # Set start and end at the element not deleted
                self.set_end(p.right)
                p.left.set_right(p.right)
                p.right.set_left(p.left)

                self.set_size(1)  # Set size to 1
            else:                 # Multiple elements
                p.left.set_right(p.right)  # Change left / right relationships
                p.right.set_left(p.left)
                if self.start == p:
                    self.set_start(self.start.right)
                if self.end == p:
                    self.set_end(self.end.left)
                self.set_size(self.size - 1)

            p = None  # Delete entry
            pointer[vertex.label] = None
            return

    def add_state(self, vertex):
        """
        Add a new state to this list.
        This is done using 3 separate cases described bellow.
        :param vertex: The Vertex to be added.
        """
        entry = DLLEntry(self.colour, vertex.label, vertex)  # Create a new DLLEntry for this Vertex.
        COLOUR[vertex.label] = self.colour  # Keep track of the vertex's colour in a separate list.

        if self.start is None:  # If the list is empty:
            entry.set_right(entry)  # Set the left most and right most entry as this new one.
            entry.set_left(entry)

            self._start = entry
            self._end = entry

        elif self.end == self.start:  # If there is only one element:
            entry.set_left(self.start)  # Set the left and right of this entry to the start.
            entry.set_right(self.start)

            self.start.set_left(entry)
            self.start.set_right(entry)

            self._end = entry  # The end is now the new entry.

        else:  # If there are multiple entries:
            entry.set_left(self.end)  # Set left to end, right to start.
            entry.set_right(self.start)
            self.end.set_right(entry)
            self.start.set_left(entry)
            self._end = entry  # The end is now the new entry.

        self._size += 1  # Increment size of DLL
        pointer[vertex.label] = entry

    def get_states(self):
        """
        Get this object's states.
        :return: A list of Vertex objects which are found in this object.
        """
        res = []
        p = self.start
        while p != self.end:
            res.append(p)
            p = p.right
        res.append(self.end)
        return res


def split_on_initial_colouring(dll, graph, initial_colouring):
    """
    Arbitrarily split the vertices in different colour classes.
    If no initial colouring is provided, the vertices will be split based on their degrees.
    :param dll: An array of differently coloured DLL objects.
    :param graph: The given graph.
    :param initial_colouring: An array of colour such that the 'i-th' vertex has colour initial_colouring[i].
    """
    if initial_colouring == []:  # Check if any initial colouring was provided.
        for i in graph.vertices:  # Split the nodes on their degree.
            degree = i.degree
            dll[degree].add_state(i)  # Add this vertex to the DLL with colour 'degree'.
    else:  # Split the nodes on initial colouring.
        for i in range(len(initial_colouring)):
            dll[initial_colouring[i]].add_state(graph.vertices[i])


def build_nx(graph):
    """
    Build the neighbour list for each vertex.
    :param graph: The given graph.
    """
    for i in graph.vertices:
        nx[i.label] = i.neighbours


def buildQueue(dll, ourQueue):
    """
    Build the working queue.
    :param dll: An array of differently coloured DLL objects.
    :param ourQueue: An empty Queue object.
    """
    aux = []
    maxsize = 0
    maxpointer = 0
    k = 0
    diffColours = 0
    for l in dll:
        if l.size > 0:
            if maxsize < l.size:
                maxsize = l.size
                maxpointer = k  # Keep track of the position of the dll with largest number of elements
            k += 1
            diffColours += 1
            aux.append(l.colour)  # Add each list to the queue
    if diffColours > 1:
        aux.pop(maxpointer)  # Remove the list with largest number of elements.
    for i in aux:
        ourQueue.put(i)


def nicePrinting(dll):
    """
    An attempt to print the list of DLL objects in a nice manner.
    :param dll: An array of differently coloured DLL objects.
    """
    for d in dll:
        if d.size > 0:
            print(d)


def colourGraph(dll, G):
    """
    Colour the vertex of the graph by setting their 'colour' property.
    This is intended for testing purposes only.
    :param dll: An array of differently coloured DLL objects.
    :param G: The given graph.
    :return: The coloured graph.
    """
    for d in dll:
        if d.size > 0:
            p = d.start
            while p != d.end:
                G.vertices[p.state].colornum = d.colour
                p = p.right
            G.vertices[d.end.state].colornum = d.colour
    return G


def smallest_free_colour():
    """
    Find the smallest free colour available.
    :return: Such a colour if it was found. If not, create a new colour and return that one.
    """
    for d in dll:
        if d.size == 0 and d.colour != 0:
            return d.colour
    dll.append(DLL())
    length = len(dll)
    dll[length - 1].set_colour(length - 1)
    return length - 1


def refine(C, G):
    """
    Refine a colour class.
    :param C: A DLL object representing a colour class.
    :param G: The given graph.
    """
    states = C.get_states()  # Retrieve the states of this colour class.
    L = []
    visited = []
    A = [0]*(len(G) + 1)
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
                    A[COLOUR[n.label]] += 1

    for colour in L:
        if A[colour] < dll[colour].size:  # Split up the colour class.
             l = smallest_free_colour()  # Get the smallest free colour.
             for v in visited:  # Iterate over found neighbours.
                 if COLOUR[v.label] == colour:  # Check that they belong to the respective colour class.
                     dll[colour].remove_state(v)  # Remove the vertex from the old colour class.
                     dll[l].add_state(v)  # Add vertex to the new colour class.
             if dll[colour].size < dll[l].size:
                 ourQueue.put(colour)
             else:
                 ourQueue.put(l)


def dllToList(dll, G):
    """
    Transform the list of DLL objects to a an array of colours.
    This is intended for testing purposes only.
    :param dll: An array of differently coloured DLL objects.
    :param G: The given graph.
    :return: An array of colours representing the list of DLL objects.
    """
    colors = [0] * (len(G.vertices))
    for i in dll:
        p = i.start
        # print(p)
        if i.size > 1:
            while p != i.end:
                colors[p.vertex.label] = i.colour
                p = p.right
            colors[p.vertex.label] = i.colour
        elif i.size == 1:
            colors[p.vertex.label] = i.colour

    return colors


def refine_colour(G, initial_colouring):
    global dll
    global COLOUR
    global pointer
    global nx

    dll = []
    COLOUR = []
    pointer = []
    nx = []

    for i in range(len(G)):
        dll.append(DLL())  # Build the empty list of DLL objects.
        dll[i].set_colour(i)  # Set the colour of each DLL object.
        COLOUR.append(-1)  # Initialise the list of colours.
        pointer.append(None)  # Initialise the list of pointers.
        nx.append(None)   # Initialise the list of neighbours.

    split_on_initial_colouring(dll, G, initial_colouring)

    build_nx(G)

    buildQueue(dll, ourQueue)

    while not ourQueue.empty():
        currentColour = ourQueue.get()
        refine(dll[currentColour], G)

    # colourGraph(dll, G)

    return COLOUR, dll
