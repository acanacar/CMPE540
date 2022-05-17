import argparse

from my_hw2.grid2 import Grid


class GridEnvironment2:

    def __init__(self, grid_matrix):
        self.grid_matrix = grid_matrix
        self.row_number = len(grid_matrix)
        self.col_number = len(grid_matrix[0])
        self.walls = Grid(self.col_number, self.row_number, False)
        self.dirt = Grid(self.col_number, self.row_number, False)
        self.numOpponentCleaner = 0
        self.agentPositions = []
        self.process_grid_matrix()

    def process_grid_matrix(self):

        for i in range(self.row_number):

            for j in range(self.col_number):
                self.process_grid_value(i, j, self.grid_matrix[i][j])

        self.agentPositions.sort()
        self.agentPositions = [(i == 0, pos) for i, pos in self.agentPositions]

    def process_grid_value(self, x, y, val):

        try:

            int(val)

        except ValueError as e:
            self.agentPositions.append((int(val), (x, y)))
            self.numOpponentCleaner += 1

        if val == 'x':
            self.walls[x][y] = True
        elif val == '.':
            self.dirt[x][y] = True
        elif val == 'c':
            self.agentPositions.append((0, (x, y)))


class Simulator:
    def __init__(self, agents, start_indice,env):
        self.start_indice = start_indice
        self.moveHistory = []
        self.agents = agents
        self.env = env


def run(env,n_actions):
    pass


def main():
    args = argparse.Namespace()
    # parser = argparse.ArgumentParser()
    # parser.add_argument("search_type")
    # parser.add_argument("file_path")
    # args = parser.parse_args()

    args.file_path = r"C:\home\acanacar\PycharmProjects\CMPE540\my_hw2\test_cases\init1.txt"
    args.search_type = "min-max"
    args.n_actions = 5

    with open(rf"{args.file_path}") as f:
        lines = f.readlines()

    environment_info = [list(row[:-1]) for row in lines]
    # agent_position = [(i, j) for i, r in enumerate(environment_info) for j, c in enumerate(r) if c == "c"][0]

    env = GridEnvironment2(grid_matrix=environment_info)
    run(env,args.n_actions)

if __name__ == '__main__':
    main()
