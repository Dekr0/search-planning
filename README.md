This repository contains all four projects required to finish in Search and Planning in Artificial Intelligence (CMPUT 366). Each folder contains the source code (located in `src` folder) for each project and analysis on the algorithms implemented per project.

## Searching

### Uninform and Inform Serach

---

- Dijkstra, Bidirectional Search, A*, Bidirection A* and MM algorithm were implemented to solved each path finding problems on the video game data provided by [movingai.com](movingai.com).
- Annoated maps were provided to visualize how each algorithm expanded during the searching process
  - The black region (most outter) surrounded the grey region indicated the boundary of a map
  - The small portion within grey region indicated the region of which a algorithm could not travel through
  - The black region in the grey out version of the original maps indicated the area algorithms expanded during the search

![](https://github.com/Dekr0/search-planning/blob/main/inform-search/src/mm/mm-16.png)

- The characteristic between algorithms was compared for each path finding problems in terms of total numbers of expansions

![](https://github.com/Dekr0/search-planning/blob/main/inform-search/src/nodes_expanded_mm_astar.png)

![](https://github.com/Dekr0/search-planning/blob/main/inform-search/src/nodes_expanded_mm_bi_astar.png)

---

## Minimax Connect 4

- Minimax algorithm and Minimax with Alpha-Beta Pruning were implemented to solved each Connect 4 configuration to determine which player will win in a given number of round as well as the most optimal move that player should play in order to win the game

- The characteristic between Minimax and Minimax with Alpha-Beta Pruning were compared in terms of number of expansions in the decision trees

---

## Suduku Solver

- A set of backtracking algorithms were implemented to solve a given sudoku problem. Each backtracking algorithm was difference from each other since they chose in between two types of variables (first variable with no assignment and MRV) selection to determine which variable to expand during, and chose whether use AC3 algorithm and forward checking or not.

- The charactersitc between each backtracking algorithms were compared in terms of number of expansions.
