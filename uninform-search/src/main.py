import cProfile
import getopt
import io
import pstats
import sys

from search.algorithms import State
from search.algorithms import dijkstra
from search.algorithms import bibs
from search.map import Map


def verify_cost(start, goal, encounter, expected, name):
    if encounter != expected:
        print(f"There is a mismatch in the solution cost found by {name} and what "
              "was expected for the problem:")
        print("Start state: ", start)
        print("Goal state: ", goal)
        print("Solution cost encountered: ", encounter)
        print("Solution cost expected: ", expected)
        print()


# noinspection DuplicatedCode
def main():
    """
    Function for testing your A* and Dijkstra's implementation. There is no need to edit this file.
    Run it with a -help option to see the options available. 
    """
    optlist, _ = getopt.getopt(sys.argv[1:], 'h:m:r:', ['testinstances', 'plots', 'help'])

    test_instances = None

    plots = False
    for o, a in optlist:
        if o in "-help":
            print("Examples of Usage:")
            print("Solve set of test instances: main.py --testinstances")
            print("Solve set of test instances and generate plots: main.py --testinstances --plots")
            exit()
        elif o in "--plots":
            plots = True
        elif o in "--testinstances":
            test_instances = "test-instances/testinstances.txt"

    gridded_map = Map("dao-map/brc000d.map")

    nodes_expanded_dijkstra = []
    nodes_expanded_bibs = []

    start_states = []
    goal_states = []
    solution_costs = []

    if not test_instances:
        exit(0)

    with open(test_instances, "r") as file:
        for instance_string in file:
            list_instance = instance_string.split(",")
            start_states.append(State(int(list_instance[0]), int(list_instance[1])))
            goal_states.append(State(int(list_instance[2]), int(list_instance[3])))

            solution_costs.append(float(list_instance[4]))

    with open("stats.csv", "w") as file, cProfile.Profile() as dij, cProfile.Profile() as bi:
        file.write("Dijkstra,Bi-Bs,Cost\n")

        for i in range(0, len(start_states)):
            start = start_states[i]
            goal = goal_states[i]

            dij.enable()
            cost, expanded_dijkstra, closed = dijkstra(start, goal, gridded_map)
            dij.disable()

            nodes_expanded_dijkstra.append(expanded_dijkstra)

            # gridded_map.plot_map(closed, start, goal, f"dij/dij-{i}.png")

            verify_cost(start, goal, cost, solution_costs[i], "Dijkstra")

            bi.enable()
            cost, expanded_bibs, closed = bibs(start, goal, gridded_map)
            bi.disable()

            nodes_expanded_bibs.append(expanded_bibs)

            # gridded_map.plot_map(closed, start, goal, f"bibs/bibs-{i}.png")

            verify_cost(start, goal, cost, solution_costs[i], "Bi-Bs")

            file.write(f"{expanded_dijkstra},{expanded_bibs},{cost}\n")

        with open("report.txt", "w") as report:
            stream = io.StringIO()
            pstats.Stats(dij, stream=stream).print_stats()
            pstats.Stats(bi, stream=stream).print_stats()
            report.write(stream.getvalue())

    if plots:
        from search.plot_results import PlotResults
        plotter = PlotResults()
        plotter.plot_results(nodes_expanded_bibs, nodes_expanded_dijkstra, "Nodes Expanded (Bi-HS)",
                             "Nodes Expanded (Dijkstra)", "nodes_expanded")

    print('Finished running all experiments.')


if __name__ == "__main__":
    main()
