import queue

from my_hw2.grid_environment import GridEnvironment


class Simulator:
    def __init__(self, agents, environment: GridEnvironment):
        self.agents = agents
        self.environment = environment
        self.fringe_lifo = queue.LifoQueue()
        self.fringe_fifo = queue.Queue()
        self.fringe_ucs = queue.PriorityQueue()
        self.nodes_visited = {}

    def goal_test(self, state):

        for i in state[2].values():
            if i != 0:
                return False

        # print(f"{state} is goal state!")
        return True

    def get_hash(self, state):
        mytext = []
        for k, v in state[2].items():
            mytext.append(f"{k}|{v}")
        dirt_txt = "__".join(mytext)
        return f"X{state[0]}Y{state[1]}|{dirt_txt}"

    def run(self):
        pass

    def run_dfs(self):

        nodes_expanded = []

        dot_booelans = self.environment.get_dot_booelans_type3()

        start_node = (self.agent.position_x, self.agent.position_y, dot_booelans)

        self.fringe_lifo.put((start_node, [], []))

        while not self.fringe_lifo.empty():

            node = self.fringe_lifo.get()

            state = node[0]
            actions = node[1]
            costs = node[2]

            hash_txt = self.get_hash(state)

            nodes_expanded.append(hash_txt)

            if self.goal_test(state):
                return len(self.nodes_visited), actions, sum(node[2])

            # print(f"new node is expanding: {node}")
            # if ([2, 5, {'x2y5': 1, 'x2y6': 0}]
            # if state[0] == 2 and state[1] == 5 and state[2]['x2y5'] == 1 and state[2]['x2y6'] == 0:
            #     print('xx')
            # if (node[0][0] == 1) and (node[0][1] == 5):
            #     print('x2')

            self.nodes_visited[hash_txt] = 1

            successors = self.agent.get_successors_2(state=state)

            for successor in successors:

                successor_state = successor[0]
                successor_action = successor[1]
                successor_cost = successor[2]

                successor_state_hash = self.get_hash(successor_state)

                if successor_state_hash not in nodes_expanded:
                    successor_path_history = actions.copy()
                    successor_path_history.append(successor_action)

                    successor_cost_history = costs.copy()
                    successor_cost_history.append(successor_cost)

                    tempPath = list(actions)
                    tempCost = list(costs)
                    tempPath.append(successor_action)
                    tempCost.append(successor_cost)

                    # self.fringe_lifo.put((successor_state, tempPath, tempCost))
                    self.fringe_lifo.put((successor_state, successor_path_history, successor_cost_history))

        return []
