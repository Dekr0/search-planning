import cProfile
import time
import getopt
import io
import pstats
import sys

from search.algorithms import State
from search.algorithms import dijkstra, bi, mm_p
from search.algorithms import octile, bi_astar_stop, mm_stop
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
    Function for testing your implementation. Run it with a -help option
    to see the options available.
    """
    optlist, _ = getopt.getopt(sys.argv[1:], 'h:m:r:', ['testinstances',
                                                        'plots', 'help'])

    plots = False
    for o, _ in optlist:
        if o in "-help":
            print("Examples of Usage:")
            print("Solve set of test instances: main.py --testinstances")
            print("Solve set of test instances and generate plots: main.py "
                  "--testinstances --plots")
            exit()
        elif o in "--plots":
            plots = True

    test_instances = "test-instances/testinstances.txt"
    gridded_map = Map("dao-map/brc000d.map")

    nodes_expanded_bi_astar = []
    nodes_expanded_astar = []
    nodes_expanded_mm = []

    start_states = []
    goal_states = []
    solution_costs = []

    with open(test_instances, "r") as file:
        for instance_string in file:
            list_instance = instance_string.split(",")
            start_states.append(State(int(list_instance[0]), int(list_instance[1])))
            goal_states.append(State(int(list_instance[2]), int(list_instance[3])))

            solution_costs.append(float(list_instance[4]))

    start_t = time.time()

    stream = io.StringIO()
    # dijkstra_Profiler = cProfile.Profile()
    # bi_bs_Profiler = cProfile.Profile()
    astar_Profiler = cProfile.Profile()
    bi_hs_Profiler = cProfile.Profile()
    mm_Profiler = cProfile.Profile()

    with open("expansion_stat.csv", "w") as file, open("profile.txt", "w") as report:
        # with uninformed searches
        # file.write("Instance #,Solution Cost,Dijkstra,BiBs,A*,MM,Bi-A*\n")

        # without uninformed searches
        file.write("Instance #,Solution Cost,A*,MM,Bi-A*\n")

        for i in range(0, len(start_states)):
            start = start_states[i]
            goal = goal_states[i]

            # For testing and obtain statistical data
            # dijkstra_Profiler.enable()
            # cost, expanded_dijkstra, closed = dijkstra(start, goal, gridded_map)
            # dijkstra_Profiler.disable()
            # verify_cost(start, goal, cost, solution_costs[i], "Dijkstra")

            astar_Profiler.enable()
            cost, expanded_astar, closed = dijkstra(start, goal, gridded_map, octile)
            astar_Profiler.disable()
            nodes_expanded_astar.append(expanded_astar)
            gridded_map.plot_map(closed, start, goal, f"astar/astar-{i}.png")
            verify_cost(start, goal, cost, solution_costs[i], "A*")

            # For testing purpose and obtain statistical data
            # bi_bs_Profiler.enable()
            # cost, expanded_bi_bs, closed = bi(start, goal, gridded_map)
            # bi_bs_Profiler.disable()
            # verify_cost(start, goal, cost, solution_costs[i], "BiBs")

            mm_Profiler.enable()
            cost, expanded_mm, closed = bi(start, goal, gridded_map, mm_p, mm_stop)
            mm_Profiler.disable()
            nodes_expanded_mm.append(expanded_mm)
            gridded_map.plot_map(closed, start, goal, f"mm/mm-{i}.png")
            verify_cost(start, goal, cost, solution_costs[i], "MM")

            bi_hs_Profiler.enable()
            cost, expanded_bi_astar, closed = bi(start, goal, gridded_map,
                                                 octile, bi_astar_stop)
            bi_hs_Profiler.disable()
            nodes_expanded_bi_astar.append(expanded_bi_astar)
            gridded_map.plot_map(closed, start, goal, f"bi-astar/bi-astar-{i}.png")
            verify_cost(start, goal, cost, solution_costs[i], "Bi-A*")

            # file.write(f"{i+1},{cost},{expanded_dijkstra},{expanded_bi_bs},"
            #            f"{expanded_astar},{expanded_mm},{expanded_bi_astar}\n")
            file.write(f"{i+1},{cost},{expanded_astar},{expanded_mm},"
                       f"{expanded_bi_astar}\n")

        end = time.time()

        print(end - start_t)

        # pstats.Stats(dijkstra_Profiler, stream=stream).strip_dirs().print_stats()
        pstats.Stats(astar_Profiler, stream=stream).strip_dirs().print_stats()
        # pstats.Stats(bi_bs_Profiler, stream=stream).strip_dirs().print_stats()
        pstats.Stats(mm_Profiler, stream=stream).strip_dirs().print_stats()
        pstats.Stats(bi_hs_Profiler, stream=stream).strip_dirs().print_stats()

        report.write(stream.getvalue())

    print('Finished running all tests. The implementation of an algorithm is likely'
          ' correct if you do not see mismatch messages for it.')

    if plots:
        from search.plot_results import PlotResults
        plotter = PlotResults()
        plotter.plot_results(nodes_expanded_mm, nodes_expanded_astar,
                             "Nodes Expanded (MM)", "Nodes Expanded (A*)",
                             "nodes_expanded_mm_astar")
        plotter.plot_results(nodes_expanded_mm, nodes_expanded_bi_astar,
                             "Nodes Expanded (MM)", "Nodes Expanded (Bi-A*)",
                             "nodes_expanded_mm_bi_astar")


if __name__ == "__main__":
    main()
