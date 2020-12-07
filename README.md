# markov-decision-process
This project implements the [Markov Decision Process](https://en.wikipedia.org/wiki/Markov_decision_process) which uses the [Bellman Equation](https://en.wikipedia.org/wiki/Bellman_equation) to calculate the utility of each cell. This works on a 2-D matrix (list of lists). User needs to set the terminal cells with their location, and optional obstacle cells.

## Usage
`usage: mdp.py [-h] r c r f f l r`  
This command will iterate through the grid until the policies do not change anymore. It will then output the grid with its final utility values, and the final policy, where the letters `u,d,l,r` represent the directions up, down, left, and right respectively.

Here is a longer description of the command line arguments:
```
positional arguments:
  r           Number of rows.
  c           Number of columns.
  r           Standard reward.
  g           Gamma.
  f           Probabilty of forward.
  l           Probabilty of left.
  r           Probabilty of right.
  ```
 
