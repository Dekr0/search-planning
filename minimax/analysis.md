1. Minimax without Alpha Beta pruning expanded 17606 states in the starting position.
Minimax with Alpha Beta pruning expanded 1413 states in the starting position.

2. 
    - Assuming player 'X' is playing the optimal move given by the Minimax and Alpha Beta
algorithms, and player 'X' place the next move in column 3 (the 4th column from left to 
right), it is impossible for player 'O' to win the game regardless the fact that player 'O' 
is playing optimally and chooses the optimal move. Player 'X' can force a win within 3 moves 
if player 'X' continue to play optimally (regardless whether if player 'O' play optimally).
Player 'O' can only win a game if player 'O' play optimally and player 'X' does not play 
optimally in a few turns. 
    - Look at the board closely, player 'X' has a better setup for winning the game while 
player 'O' is more difficult to construct a setup to win the game (less alignment to make 
a connect 4).

3. It is possible for Minimax and Alpha Beta to expand the same number of nodes under only
 one condition. That condition is that the max nodes are ordered with increasing value and 
the min nodes are ordered in the decreasing values. In such a condition, Alpha Beta cannot 
prune any node since it will always discover a better score and a better move after expanding 
the next nodes. This is also the worst case for Alpha Beta pruning.