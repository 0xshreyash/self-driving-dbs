# Multi-armed bandits

## Explore first

Just explore at the start. Allocating N exploration steps for each of the K arms and then pick the best one on average.

## Epsilon-greedy

for each round do:
  toss a coin with success probability epsilon
  if success then
    explore arms with uniform probability
  else
    exploit the arm with the highest average answer

The above two strategies do not adapt themselves to the awards observed by the algorithm. 


