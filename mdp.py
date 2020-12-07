#!/usr/bin/env python
import argparse

class MDP:
    def __init__(self, rows, cols, rs, g, f, l, r):
        # Values on board from most recent complete iteration
        self.board = [[0 for n in range(cols)] for m in range(rows)]
        # Policy from most recent complete iteration
        self.policy = [['-' for n in range(cols)] for m in range(rows)]
        # Number of rows
        self.rows = rows
        # Number of columns
        self.cols = cols
        # Reward value for non-terminal states
        self.reward = rs
        # Gamma
        self.gamma = g
        # Probability of going forward
        self.forward = f
        # Probabilty of going left
        self.left = l
        # Probabilty of going right
        self.right = r
        # Probabilty of going back assumed to be 0

        # List of values of all iterations so far
        self.policies = []
        # Get user input for terminal states locations and values
        self.terminals = self.set_terminals()
        # Get user input for obstacle states locations and values
        self.obstacles = self.set_obstacles()

        # Set inital state as iterations list for now.
        # Newer states will be added as required
        self.iterations = [self.board]

    def __str__(self):
        output = []
        for row in self.board:
            output.append(' '.join(list(str(el).rjust(6) for el in row)))
        output = '\n'.join(output)
        output2 = []
        for row in self.policy:
            output2.append(' '.join(list(str(el).rjust(6) for el in row)))
        output2 = '\n'.join(output2)
        return 'Values:\n'+output+'\n\n---------------\n\nPolicy:\n'+output2+'\n'

    # Prompt user to set the terminal states' locations and values
    def set_obstacles(self):
        obstacles = []
        print("Set the obstacle cells:\n")
        while True:
            val = input("Enter r,c or enter 'fin' when done\n")
            if val == 'fin':
                break
            try:
                r,c = val.split(',')
            except ValueError:
                print("\nWrong format\n")
                continue
            else:
                try:
                    self.board[int(r)][int(c)] = '-'
                except IndexError:
                    print("\nRow, column values out of bounds\n")
                    continue
                obstacles.append((int(r),int(c)))
        print()
        return obstacles

    # Prompt user to set the terminal states' locations and values
    def set_terminals(self):
        terminals = []
        print("Set the terminal cells:\n")
        while True:
            val = input("Enter r,c,val, or enter 'fin' when done\n")
            if val == 'fin':
                if len(terminals) == 1:
                    print("\nYou need at least two terminal cells\n")
                    continue
                else:
                    break
            try:
                r,c,val = val.split(',')
            except ValueError:
                print("\nWrong format\n")
                continue
            else:
                try:
                    self.board[int(r)][int(c)] = int(val)
                except IndexError:
                    print("\nRow, column values out of bounds\n")
                    continue
                terminals.append((int(r),int(c)))
        print()
        return terminals

    # Set policy for a cell given its options
    def set_policy(self, i, j, direction_values):
        policy = max(direction_values, key = lambda x: x[1])
        self.policy[i][j] = policy[0]

    # Calculate the utility for a given cell
    def bellman_equation(self, i, j):

        # If that direction is in bounds and not an obstacle, take that value, else,
        # take the current cell's value
        move_up    = self.board[i-1][ j ] if (((i-1) >= 0        ) and ((i-1,j) not in self.obstacles)) else self.board[i][j]
        move_down  = self.board[i+1][ j ] if (((i+1) <  self.rows) and ((i+1,j) not in self.obstacles)) else self.board[i][j]
        move_left  = self.board[ i ][j-1] if (((j-1) >= 0        ) and ((i,j-1) not in self.obstacles)) else self.board[i][j]
        move_right = self.board[ i ][j+1] if (((j+1) <  self.cols) and ((i,j+1) not in self.obstacles)) else self.board[i][j]

        # (Calculate Probabilty of each move * Utility of that move) for each direction
        u = (self.forward * move_up) + (self.left * move_left) + (self.right * move_right)

        l = (self.forward * move_left) + (self.left * move_down) + (self.right * move_up)

        r = (self.forward * move_right) + (self.left * move_up) + (self.right * move_down)

        d = (self.forward * move_down) + (self.left * move_right) + (self.right * move_left)

        # Bellman Equation with the max of the above four values
        utility = self.reward + self.gamma * max(u, d, l, r)

        # Set the policy using the four directions and their values
        self.set_policy(i, j, [('u', u), ('d', d), ('l', l), ('r',r)])

        # Round for pretty numbers
        return round(utility, 5)

    # Calculate new utilities for all non-terminal cells in the grid, based on old values
    def iterate(self):
        new_iter = [x[:] for x in self.board]
        for i in range(self.rows):
            for j in range(self.cols):

                if (i,j) not in self.terminals and (i,j) not in self.obstacles:
                    utility = self.bellman_equation(i,j)
                    new_iter[i][j] = utility
                else:
                    if (i,j) in self.terminals:
                        self.policy[i][j] = self.board[i][j]
        self.iterations.append(new_iter)
        self.policies.append(self.policy)
        self.board = new_iter

    # Check if 2-d lists are equal
    def two_d_equal(self, a, b):
        for i in range(len(a)):
            for j in range(len(a[0])):
                if a[i][j] != b[i][j]:
                    return False
        return True

    # Check if the last two policies are equal, meaning that the policy has converged
    def converged(self):
        if len(self.policies) >= 2:
            if self.two_d_equal(self.policies[-1], self.policies[-2]):
                return True
        return False

    # Run the iteration till the policy converges
    def get_policy(self):
        i = 1
        while not self.converged():
            self.iterate()
            i += 1
        print()
        print("Number of iterations:", i)
        print()
        print(self)

# Accept user input
def main():
    parser = argparse.ArgumentParser(description='Markov Decision Process')

    parser.add_argument('rows', type = int,
                        help ='Number of rows.',
                        metavar = 'r')
    parser.add_argument('cols', type = int,
                        help ='Number of columns.',
                        metavar = 'c')
    parser.add_argument('rs', type = float,
                        help ='Standard reward.',
                        metavar = 'r')
    parser.add_argument('g', type = float,
                        help ='Gamma.',
                        metavar = 'g')
    parser.add_argument('f', type = float,
                        help ='Probabilty of forward.',
                        metavar = 'f')
    parser.add_argument('l', type = float,
                        help ='Probabilty of left.',
                        metavar = 'l')
    parser.add_argument('r', type = float,
                        help ='Probabilty of right.',
                        metavar = 'r')
    args = parser.parse_args()

    gridworld = MDP(args.rows, args.cols, args.rs, args.g, args.f, args.l, args.r)
    print(gridworld)
    gridworld.get_policy()

if __name__ ==  "__main__":
    main()
