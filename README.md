# markov-decision-process
This project implements the [Markov Decision Process](https://en.wikipedia.org/wiki/Markov_decision_process) which uses the [Bellman Equation](https://en.wikipedia.org/wiki/Bellman_equation) to calculate the utility of each cell. This works on a 2-D matrix (list of lists). User needs to set the terminal cells with their location, and optional obstacle cells.

## Usage
`usage: mdp.py [-h] rows c rs g f l r`  
This command will iterate through the grid until the policies do not change anymore. It will then output the grid with its final utility values, and the final policy, where the letters `u,d,l,r` represent the directions up, down, left, and right respectively.

Here is a longer description of the command line arguments:
```
positional arguments:
  rows        Number of rows.
  c           Number of columns.
  rs          Standard reward.
  g           Gamma.
  f           Probabilty of forward.
  l           Probabilty of left.
  r           Probabilty of right.
  ```
Try `python3 mdp.py 3 2 -0.1 0.8 0.6 0.2 0.2`, with terminal cells `0,1,1`, `2,1,-5`, and obstacles `1,1`. this should run for 3 iterations. Here's a sample output during the final iteration, for calculating the final utility of index `[2,1]`:
```
[2, 1]
  Up    : (0.600000 * -1.700000) + (0.200000 * -0.100000) + (0.200000 * -1.700000) = -1.380000
  Down  : (0.600000 * -1.700000) + (0.200000 * -1.700000) + (0.200000 * -0.100000) = -1.380000
  Left  : (0.600000 * -0.100000) + (0.200000 * -1.700000) + (0.200000 * -1.700000) = -0.740000
  Right : (0.600000 * -1.700000) + (0.200000 * -1.700000) + (0.200000 * -0.100000) = -1.700000

  Utility : -0.100000 + 0.800000 * max(-1.380000, -1.380000, -0.740000, -1.700000,) = -0.692000

```

## Class MDP
### Class variables
- board: Utility values of the most recent complete iteration
- policy: Policy from most recent complete iteration 
- rows: Number of rows
- cols: Number of columns
- reward: Reward value for non-terminal states
- gamma: Gamma value
- forward: Probability of going forward
- left: Probabilty of going left
- right: Probabilty of going right
- (Probabilty of going back assumed to be 0)
- policies: List of values of all iterations so far      
- terminals: List of terminal cells' locations and values
- obstacles: List of obstacle cells' locations
- iterations: States with utility values for all iterations

### Class methods
- `set_terminals()`: Called automatically when the class object is initialized. Prompts user to set the terminal cells' locations and values. Returns a list of tuples which represent the locations and values of terminal cells.
- `set_obstacles()`: Called automatically when the class object is initialized. Prompts user to set the obstacle cells' locations. Returns a list of tuples which represent the locations of obstacles.
- `iterate()`: Performs a single iteration over the grid, updating the utilities for all non-terminal, non-obstacle cells, updates the `self.policy`, `self.board`, `self.iterations`, and `self.policies` class variables. Does not return anything.
- `converged()`: Returns true if the policy has converged over the last two complete iterations
- `bellman_equation()`: Accepts a location on board and returns new utility value for it. WARNING: This method updates the policy variable as well. If you want to calculate the utility without updating the policy, comment out the call to `self.set_policy()`, and make sure to manually call it elsewhere, after each call.
- `get_policy()`: Perform iterations till the policy converges. Prints the number of iterations, and final utilities and policy. These are also stored in the `self.board` and `self.policy` variables respectively.
