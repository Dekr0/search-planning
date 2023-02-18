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

```
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | |X| | | | |
|O|O|X|O|X| | |
|X|X|O|X|O| |O|
---------------
 0 1 2 3 4 5 6

optimal move to play: 3
```

---

## Suduku Solver

- A set of backtracking algorithms were implemented to solve a given sudoku problem. Each backtracking algorithm was difference from each other since they chose in between two types of variables (first variable with no assignment and MRV) selection to determine which variable to expand during, and chose whether use AC3 algorithm and forward checking or not.

```
- - - - - - - - - - - - -
| 5 2 . | . . 6 | . . . |
| . . . | . . . | 7 . 1 |
| 3 . . | . . . | . . . |
- - - - - - - - - - - - -
| . . . | 4 . . | 8 . . |
| 6 . . | . . . | . 5 . |
| . . . | . . . | . . . |
- - - - - - - - - - - - -
| . 4 1 | 8 . . | . . . |
| . . . | . 3 . | . 2 . |
| . . 8 | 7 . . | . . . |
- - - - - - - - - - - - -

- - - - - - - - - - - - -
| 5 2 7 | 3 1 6 | 4 8 9 |
| 8 9 6 | 5 4 2 | 7 3 1 |
| 3 1 4 | 9 8 7 | 5 6 2 |
- - - - - - - - - - - - -
| 1 7 2 | 4 5 3 | 8 9 6 |
| 6 8 9 | 2 7 1 | 3 5 4 |
| 4 5 3 | 6 9 8 | 2 1 7 |
- - - - - - - - - - - - -
| 9 4 1 | 8 2 5 | 6 7 3 |
| 7 6 5 | 1 3 4 | 9 2 8 |
| 2 3 8 | 7 6 9 | 1 4 5 |
- - - - - - - - - - - - -

```

- The charactersitc between each backtracking algorithms were compared in terms of number of expansions.

![](https://github.com/Dekr0/search-planning/blob/main/sudoku-solver/src/running_time.png)
