import math
import heapq


class State:
    """
    Class to represent a state on grid-based pathfinding problems. The class contains a static variable:
    map_width containing the width of the map. Although this variable is a property of the map and not of 
    the state, the property is used to compute the hash value of the state, which is used in the CLOSED list. 

    Each state has the values of x, y, g, and cost. The cost is used as the criterion for sorting the nodes
    in the OPEN list for A*, Bi-A*, and MM. For A* and Bi-A* the cost should be the f-value of the node, while
    for MM the cost should be the p-value of the node. 
    """
    map_width = 0

    def __init__(self, x, y):
        """
        Constructor - requires the values of x and y of the state. All the other variables are
        initialized with the value of 0.
        """
        self._x = x
        self._y = y
        self._g = 0
        self._cost = 0

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
        return self._cost < other._cost

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
        return self._x == other._x and self._y == other._y

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

    def get_cost(self):
        """
        Returns the g-value of the state
        """
        return self._cost

    def set_cost(self, cost):
        """
        Sets the g-value of the state
        """
        self._cost = cost


def _get_coord(state):
    return [state.get_x(), state.get_y()]


def _un_inform(*args):
    if isinstance(args[0], State):
        args[0].set_cost(args[0].get_g())


def octile(state_1, state_2, old_child=None):
    """
    :param state_1:
    :param state_2:
    :param old_child: for reusing h-value. Floating point arithmetic are expensive,
    since h value remain the same regardless whether is from opened list or
    closed list
    :return:
    """

    if not old_child:
        dx = abs(state_1.get_x() - state_2.get_x())
        dy = abs(state_1.get_y() - state_2.get_y())
        h = state_1.get_g() + 1.5 * min(dx, dy) + abs(dx - dy)
        state_1.set_cost(h)
    else:
        state_1.set_cost(state_1.get_g() + (old_child.get_cost() - old_child.get_g()))


def mm_p(state_1, state_2, old_child=None):
    octile(state_1, state_2, old_child)
    state_1.set_cost(max(state_1.get_cost(), 2 * state_1.get_g()))


# noinspection DuplicatedCode
def _in_closed_list(parent, child, opened, closed, count=0):
    """

    :param State parent:
    :param State child:
    :param list opened:
    :param dict closed:
    :return:
    """
    g = child.get_g()
    cost = child.get_cost()
    key = child.state_hash()

    if key not in closed:
        heapq.heappush(opened, child)

        closed[key] = child

    if key in closed and g < closed[key].get_g():
        closed[key].set_cost(cost)
        closed[key].set_g(g)

        heapq.heapify(opened)


# noinspection DuplicatedCode
def dijkstra(start, goal, _map, heuristic=_un_inform):
    """
    A dijkstra that aims for modularity and more general usage. However,
    performance tends to be decreased due to generated stack if there
    are too many function calls


    :param start:
    :param goal:
    :param _map:
    :param heuristic: a callable object such as function, method, or lambda
    expression that takes in two states and return f-value. By default, it
    will be _un_inform, which set the f-value equal to g-value.
    :return:
    """
    heuristic(start, goal)

    count = 0

    opened = []

    heapq.heappush(opened, start)

    expansion = 0

    closed = {start.state_hash(): start}

    while not len(opened) == 0:
        parent = heapq.heappop(opened)

        expansion += 1

        if parent == goal:
            return parent.get_g(), expansion, \
                   {k: v for k, v in closed.items()}

        for child in _map.successors(parent):
            key = child.state_hash()

            if key in closed:
                heuristic(child, goal, closed[key])
            else:
                heuristic(child, goal)

            _in_closed_list(parent, child, opened, closed, count)

    return -1.00, expansion, {k: v for k, v in closed.items()}


# noinspection DuplicatedCode
def _bi(u, goal, opened, closed_forward, closed_backward, heuristic, _map):
    parent = heapq.heappop(opened)

    for child in _map.successors(parent):
        key = child.state_hash()
        current_g = child.get_g()

        if key in closed_forward:
            heuristic(child, goal, closed_forward[key])
        else:
            heuristic(child, goal)

        if key in closed_backward:
            u = min(u, closed_backward[key].get_g() + current_g)

        _in_closed_list(parent, child, opened, closed_forward)

    return u


def _get_bi_closed(closed_forward_list, closed_backward_list):
    closed_list = {k: v for k, v in closed_forward_list.items()}
    for k, v in closed_backward_list.items():
        closed_list[k] = v

    return closed_list


def _bi_stop_condition(u, min_f, min_b):
    return u <= min_f + min_b


def bi_astar_stop(u, min_f, min_b):
    return u <= min_f or u <= min_b


def mm_stop(u, min_f, min_b):
    return u <= min(min_f, min_b)


# noinspection DuplicatedCode
def bi(start, goal, _map, heuristic=_un_inform, stop=_bi_stop_condition):
    """
    A bidirectional search that aims for modularity and more general usage. However,
    performance tends to be decreased due to generated stack if there
    are too many function calls

    :param start:
    :param goal:
    :param _map:

    :param heuristic: a callable object such as function, method, or lambda
    expression that takes in two states and return f-value. By default, it
    will be _un_inform, which set the f-value equal to g-value (BiBs)

    :param stop: same as heuristic parameter but the signature of the callable
    objects includes first the current cost of the solution path, min values from
    both open lists. Then, it returns true or false to determine the stopping
    condition. By default, stop condition for BiBs is used.

    :return:
    """
    if not callable(heuristic) and not callable(stop):
        return

    heuristic(start, goal)
    heuristic(goal, start)

    open_f = []
    open_b = []

    closed_f = {start.state_hash(): start}
    closed_b = {goal.state_hash(): goal}

    i

    heapq.heappush(open_f, start)
    heapq.heappush(open_b, goal)

    u = math.inf

    expansion = 0

    while not len(open_f) == 0 and not len(open_b) == 0:
        min_f = open_f[0].get_cost()
        min_b = open_b[0].get_cost()

        if stop(u, min_f, min_b):
            return u, expansion, _get_bi_closed(closed_f, closed_b)

        if min_f < min_b:
            u = _bi(u, goal, open_f, closed_f, closed_b, heuristic, _map)
        else:
            u = _bi(u, start, open_b, closed_b, closed_f, heuristic, _map)

        expansion += 1

    return -1.00, expansion, _get_bi_closed(closed_f, closed_b)
