import heapq
import math


class State:
    """
    Class to represent a state on grid-based pathfinding problems. The class contains one static variable:
    map_width containing the width of the map. Although this is a property of the map and not of the state, 
    the width is used to compute the hash value of the state, which is used in the CLOSED list. 

    Each state has the values of x, y, g.  
    """
    map_width = 0
    map_height = 0

    def __init__(self, x, y):
        """
        Constructor - requires the values of x and y of the state. All the other variables are
        initialized with the value of 0.
        """
        self._x = x
        self._y = y
        self._g = 0

    def __repr__(self):
        """
        This method is invoked when we call a print instruction with a state. It will print [x, y],
        where x and y are the coordinates of the state on the map. 
        """
        state_str = "[" + str(self._x) + ", " + str(self._y) + "]"
        return state_str

    def __lt__(self, other):
        """
        Less-than operator; used to sort the nodes in the OPEN list
        """
        return self._g < other.get_g()

    def state_hash(self):
        """
        Given a state (x, y), this method returns the value of x * map_width + y. This is a perfect 
        hash function for the problem (i.e., no two states will have the same hash value). This function
        is used to implement the CLOSED list of the algorithms. 
        """
        return self._y * State.map_width + self._x

    def __eq__(self, other):
        """
        Method that is invoked if we use the operator == for states. It returns True if self and other
        represent the same state; it returns False otherwise. 
        """
        return self._x == other.get_x() and self._y == other.get_y()

    def get_x(self):
        """
        Returns the x coordinate of the state
        """
        return self._x

    def get_y(self):
        """
        Returns the y coordinate of the state
        """
        return self._y

    def get_g(self):
        """
        Returns the g-value of the state
        """
        return self._g

    def set_g(self, cost):
        """
        Sets the g-value of the state
        """
        self._g = cost


class Node:

    def __init__(self, parent, state):
        self._parent = parent
        self._state = state

    def get_g(self):
        return self._state.get_g()

    def get_parent(self):
        return self._parent

    def get_state(self):
        return self._state

    def set_parent(self, parent):
        self._parent = parent

    def set_g(self, g):
        self._state.set_g(g)


def _get_bibs_closed_list(closed_forward_list, closed_backward_list):
    closed_list = {k: v.get_state() for k, v in closed_forward_list.items()}
    for k, v in closed_backward_list.items():
        closed_list[k] = v.get_state()

    return closed_list


def _in_closed_list(parent, child, hash_key, current_g, open_list, closed_list):
    if hash_key not in closed_list:
        heapq.heappush(open_list, child)

        closed_list[hash_key] = Node(parent, child)

    if hash_key in closed_list and current_g < closed_list[hash_key].get_g():
        closed_list[hash_key].set_g(current_g)
        closed_list[hash_key].set_parent(parent)

        heapq.heapify(open_list)


def _bibs_helper(u, num_expansion, open_list, closed_forward_list, closed_backward_list, gridded_map):
    parent = heapq.heappop(open_list)
    num_expansion += 1

    for child in gridded_map.successors(parent):
        hash_key = child.state_hash()
        current_g = child.get_g()

        if hash_key in closed_backward_list:
            u = min(u, closed_backward_list[hash_key].get_g() + current_g)

        _in_closed_list(parent, child, hash_key, current_g, open_list, closed_forward_list)

    return u, num_expansion


def bibs(start, goal, gridded_map):
    open_forward_list = []
    open_backward_list = []

    closed_forward_list = {start.state_hash(): Node(None, start)}
    closed_backward_list = {goal.state_hash(): Node(None, goal)}

    heapq.heappush(open_forward_list, start)
    heapq.heappush(open_backward_list, goal)

    u = math.inf  # cost of the best solution seen so far

    num_expansion = 0

    while not len(open_forward_list) == 0 and not len(open_backward_list) == 0:
        min_forward = open_forward_list[0].get_g()
        min_backward = open_backward_list[0].get_g()

        if u <= min_forward + min_backward:
            return u, num_expansion, \
                   _get_bibs_closed_list(closed_forward_list, closed_backward_list)

        if min_forward < min_backward:
            u, num_expansion = _bibs_helper(u, num_expansion, open_forward_list,
                                            closed_forward_list,
                                            closed_backward_list, gridded_map)
        else:
            u, num_expansion = _bibs_helper(u, num_expansion, open_backward_list,
                                            closed_backward_list,
                                            closed_forward_list, gridded_map)

    return -1.00, num_expansion, _get_bibs_closed_list(closed_forward_list, closed_backward_list)


def dijkstra(start, goal, gridded_map):
    open_list = []

    heapq.heappush(open_list, start)

    hash_key = start.state_hash()
    node = Node(None, start)

    num_expansion = 0

    closed_list = {hash_key: node}

    while not len(open_list) == 0:
        parent = heapq.heappop(open_list)
        num_expansion += 1

        if parent == goal:
            return parent.get_g(), num_expansion, \
                   {k: v.get_state() for k, v in closed_list.items()}

        for child in gridded_map.successors(parent):
            hash_key = child.state_hash()
            current_g = child.get_g()

            _in_closed_list(parent, child, hash_key, current_g, open_list, closed_list)

    return -1.00, num_expansion, {k: v.get_state() for k, v in closed_list.items()}
