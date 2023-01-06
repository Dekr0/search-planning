## Discuss Results

---

- From the given runtime plot between Backtracking using MRV and First Available, there are noticeable number of 
problems that are solved in approximately the same time by using either of the two heuristics. This potentially caused 
by the fact that majority of the available non-assigned variables have very similar domain size or no difference between 
each other. There are no considerable amount of non-assigned variables with small domain size stand out among the others 
to improve the backtracking performance. Despite MRV also utilizes degree heuristic to act as tie-breaker, it does not 
create a large difference for a problem that with large numbers of non-assigned variables (i.e., less binary constraints
). In order to utilize MRV, the problem space should consist of a good degree of number of variables with noticeably small 
domain sizes compare to other variables. This allows MRV can quickly distinguish those variables among others as well as 
improve the backtracking performance due to their small domain sizes.

- There are also number of problems where MRV can solve in less than nearly at 0 sec while First Available need to spend 
more than that. In these problems, MRV is able to improve the backtracking performance significantly through variables 
with small domain size. 

- There are few exceptions where MRV spend slightly more times than First Available because MRV needs additional time 
to iterate through all variables for locate the one with minimum domain size for every search call where First Available 
only need to pick where its domain size is greater than one. 