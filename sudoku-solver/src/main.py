import time

from grid import Grid
from math import inf
from plot_results import PlotResults


def ac3(grid, var):
    """
        This is a domain-specific implementation of AC3 for Sudoku. 

        It keeps a set of arcs to be processed (arcs) which is provided as input to the method. 
        Since this is a domain-specific implementation, we don't need to maintain a graph and a set 
        of arcs in memory. We can store in arcs the cells of the grid and, when processing a cell, 
        we ensure arc consistency of all variables related to this cell by removing the value of
        cell from all variables in its column, row, and unit. 

        For example, if the method is used as a preprocessing step, then arcs is initialized with 
        all cells that start with a number on the grid. This method ensures arc consistency by
        removing from the domain of all variables in the row, column and unit the values of 
        the cells given as input. The method adds to the set of arcs all variables that have
        their values assigned during the propagation of the constraints.
    """
    if not type(var) == list:
        arcs = [var]
    else:
        arcs = var
    checked = set()
    while len(arcs):
        cell = arcs.pop()
        checked.add(cell)

        assigned_row, failure = grid.remove_domain_row(cell[0], cell[1])
        if failure: return failure

        assigned_column, failure = grid.remove_domain_column(cell[0], cell[1])
        if failure: return failure

        assigned_unit, failure = grid.remove_domain_unit(cell[0], cell[1])
        if failure: return failure

        arcs.extend(assigned_row)
        arcs.extend(assigned_column)
        arcs.extend(assigned_unit)
    return False


def pre_process_ac3(grid):
    """
    This method enforces arc consistency for the initial grid of the puzzle.

    The method runs AC3 for the arcs involving the variables whose values are 
    already assigned in the initial grid. 
    """
    arcs_to_make_consistent = []

    for i in range(grid.get_width()):
        for j in range(grid.get_width()):
            if len(grid.get_cells()[i][j]) == 1:
                arcs_to_make_consistent.append((i, j))

    ac3(grid, arcs_to_make_consistent)


def select_variable_fa(grid):
    for i in range(grid.get_width()):
        for j in range(grid.get_width()):
            if len(grid.get_cells()[i][j]) > 1:
                return i, j

    return None


def select_variable_mrv(grid):
    var = ()
    mrv = inf

    for i in range(grid.get_width()):
        for j in range(grid.get_width()):
            domain_size = len(grid.get_cells()[i][j])

            if mrv > domain_size > 1:
                var = (i, j)
                mrv = domain_size
            elif domain_size == mrv:
                if _tie_breaker(grid, var, i, j):
                    var = (i, j)

    return var


def _tie_breaker(grid, var, x, y):
    if degree_heuristic(grid, x, y) > degree_heuristic(grid, var[0], var[1]):
        return True
    return False


def degree_heuristic(grid, x, y):
    degree = 0

    bag = set()

    # Fix row, find the number of variables that is already assigned.
    for i in range(grid.get_width()):
        if len(grid.get_cells()[x][i]) == 1 and i != y:
            degree += 1
            bag.add((x, i))

    # Fix column, find the number of variables that is already assigned.
    for i in range(grid.get_width()):
        if len(grid.get_cells()[i][y]) == 1 and i != x:
            degree += 1
            bag.add((i, y))

    row_init = (x // 3) * 3
    col_init = (y // 3) * 3

    for i in range(row_init, row_init + 3):
        for j in range(col_init, col_init + 3):
            if len(grid.get_cells()[i][j]) == 1 and (i, j) != (x, y) and (i, j) not in bag:
                degree += 1

                bag.add((i, j))

    return degree


def search(grid, var_selector):

    if grid.is_solved_deep():
        return grid, True

    var = var_selector(grid)

    for d in grid.get_cells()[var[0]][var[1]]:
        if grid.is_value_consistent(d, var[0], var[1]):
            copy_grid = grid.copy()

            copy_grid.get_cells()[var[0]][var[1]] = f'{d}'

            failure = ac3(copy_grid, var)
            if not failure:
                result, solved = search(copy_grid, var_selector)
                if solved:
                    return result, solved

    return None, False


def solve(grid, var_selector):
    pre_process_ac3(grid)

    start = time.time()

    result, solved = search(grid, var_selector)

    end = time.time()

    return end - start


if __name__ == "__main__":

    file = open('tutorial_problem.txt', 'r')
    problems = file.readlines()
    for p in problems:
        g = Grid()
        g.read_file(p)

        pre_process_ac3(g)

        result, solved = search(g, select_variable_mrv)

    file = open('top95.txt', 'r')
    problems = file.readlines()

    runtime_mrv = []
    runtime_fa = []

    for p in problems:
        g = Grid()
        g.read_file(p)

        fa_runtime = solve(g.copy(), select_variable_fa)
        mrv_runtime = solve(g.copy(), select_variable_mrv)

        runtime_mrv.append(mrv_runtime)
        runtime_fa.append(fa_runtime)
    
    
    plotter = PlotResults()
    plotter.plot_results(
        runtime_mrv,
        runtime_fa,
        "Running Time Backtracking (MRV)",
        "Running Time Backtracking (FA)",
        "running_time",
    )
