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
Try `python3 mdp.py 3 2 -0.1 0.8 0.6 0.2 0.2`, with terminal cells `0,1,1`, `2,1,-5`, and obstacles `1,1`. this should run for 3 iterations.
