from my_hw1.agent import Agent
from my_hw1.environment import GridEnvironment
from my_hw1.simulator import Simulator

with open(r'C:\Users\a.acar\PycharmProjects\CMPE540_HW1\my_hw1\test_cases\init1.txt') as f:
    lines = f.readlines()

environment_info = [list(row[:-1]) for row in lines]
agent_position = [(i, j) for i, r in enumerate(environment_info) for j, c in enumerate(r) if c == "c"][0]

env = GridEnvironment(grid_matrix=environment_info)

agent = Agent(environment=env, position=agent_position)

simulator = Simulator(agent=agent, environment=env)

# (count_of_nodes, actions, costs) = simulator.run_bfs()
# (count_of_nodes, actions, costs) = simulator.run_dfs()
# (count_of_nodes, actions, costs) = simulator.run_ucs()
# (count_of_nodes, actions, costs) = simulator.run_greedy()
(count_of_nodes, actions, costs) = simulator.run_astar()
print(f"path : {actions}")
print(f"costs : {costs}")
print(f"number of expanded nodes : {count_of_nodes}")
print('done')

"""
down right up right right down right up right down suck up left down suck suck
['down', 'right', 'right', 'up', 'right', 'right', 'down', 'right', 'suck', 'left', 'suck', 'right', 'suck']

"""
