#!/usr/bin/env python
import argparse

class MDP:
    def __init__(self, rows, cols, rs, g, f, l, r):

        self.board = [[0 for n in range(cols)] for m in range(rows)]
        self.policy = [['-' for n in range(cols)] for m in range(rows)]
        self.rows = rows
        self.cols = cols
        self.reward = rs
        self.gamma = g
        self.forward = f
        self.left = l
        self.right = r

        # List of change of value for each cell, after each iteration
        self.policies = []

        # Test Code
        self.board[0][1] = 1
        self.board[2][1] = -5
        self.terminals = [(0,1),(2,1), (1,1)]

        # self.set_terminals()
        # List of terminal positions
        self.iterations = [self.board]
    def reset_policy(self):
        self.policy = [['-' for n in range(cols)] for m in range(rows)]

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

    def set_terminals(self):
        terminals = []
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
        self.terminals = terminals

    def set_policy(self, i, j, direction_values):
        policy = max(direction_values, key = lambda x: x[1])
        self.policy[i][j] = policy[0]


    def bellman_equation(self, i, j):
        move_up    = self.board[i-1][ j ] if (i-1) >= 0         else self.board[i][j]
        move_down  = self.board[i+1][ j ] if (i+1) <  self.rows else self.board[i][j]
        move_left  = self.board[ i ][j-1] if (j-1) >= 0         else self.board[i][j]
        move_right = self.board[ i ][j+1] if (j+1) <  self.cols else self.board[i][j]

        u = (self.forward * move_up) + (self.left * move_left) + (self.right * move_right)

        l = (self.forward * move_left) + (self.left * move_down) + (self.right * move_up)

        r = (self.forward * move_right) + (self.left * move_up) + (self.right * move_down)

        d = (self.forward * move_down) + (self.left * move_right) + (self.right * move_left)

        utility = self.reward + self.gamma * max(u, d, l, r)
        self.set_policy(i, j, [('u', u), ('d', d), ('l', l), ('r',r)])
        return round(utility, 5)

    def iterate(self):
        new_iter = [x[:] for x in self.board]
        for i in range(self.rows):
            for j in range(self.cols):

                if (i,j) not in self.terminals:
                    utility = self.bellman_equation(i,j)
                    new_iter[i][j] = utility
        self.iterations.append(new_iter)
        self.policies.append(self.policy)
        self.board = new_iter

    def two_d_equal(self, a, b):
        for i in range(len(a)):
            for j in range(len(a[0])):
                if a[i][j] != b[i][j]:
                    return False
        return True

    def converged(self):
        if len(self.policies) >= 2:
            if self.two_d_equal(self.policies[-1], self.policies[-2]):
                return True
        return False

    def get_policy(self):
        i = 1
        while not self.converged():
            self.iterate()
            i += 1
        print()
        print("Number of iterations:", i)
        print()
        print(self)


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
                        metavar = 'f')
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
    gridworld.get_policy()

if __name__ ==  "__main__":
    main()
