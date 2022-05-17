import argparse
import queue

from my_hw2.agents import ExpectimaxAgent
from my_hw2.grid_environment import GridEnvironment

class RandomAgent:
    def __init__(self,index):
        self.index = index

class OptimalAgent:
    pass


def load_agents(env: GridEnvironment, search_type, agent_position):
    if search_type == "min-max":
        my_agent = ExpectimaxAgent(position=agent_position, environment=env)

    other_agents = []
    for i in range(env.row_number):
        for j in range(env.col_number):
            if type(env.grid_matrix[i][j]) == int: #that means agent
                agent_no = env.grid_matrix[i][j]
                if agent_no % 2 == 0:
                    agent = RandomAgent(index=agent_no)
                else:
                    agent = OptimalAgent()
                if len(other_agents) == 0:
                    other_agents[0] = (env.grid_matrix[i][j])




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
    agent_position = [(i, j) for i, r in enumerate(environment_info) for j, c in enumerate(r) if c == "c"][0]

    env = GridEnvironment(grid_matrix=environment_info)
    load_agents(env, args.search_type, agent_position)
    print('x')

if __name__ == '__main__':
    main()
