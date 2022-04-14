# Missionaries-and-Cannibal-Problem using A* (Star) algorithm
There are two islands. One left and one right.
The Missionaries and Cannibal problem's main goal is the movement of N cannibals
and N missionaries from one island to the other using a boat of M people capacity.

Despite how easy it sounds there is one condition to this problem:

The number of cannibals on both islands must be lower than the number of missionaries, otherwise 
the cannibals will "eat" the missionaries and we don't want that.

The algorithm we'll be using is called A*(Star) algorithm which uses techniques for path finding and graph traversals.
All we have to do is give as inputs the number of both missionaries and cannibals(N), the capacity of people for the boat(M) and
how many moves we wish the boat to transfer. 
