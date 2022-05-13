import queue
from my_hw1.agent import Agent
from my_hw1.environment import GridEnvironment


class Simulator:
    def __init__(self, agent: Agent, environment: GridEnvironment):
        self.agent = agent
        self.environment = environment
        self.fringe_lifo = queue.LifoQueue()
        self.fringe_fifo = queue.Queue()
        self.fringe_ucs = queue.PriorityQueue()
        self.nodes_visited = {}

    # def handle_action(self, action):
    #     if action == "SUCK":
    #         self.environment.grid_matrix[self.agent.position_x][self.agent.position_y] = ' '

    def goal_test(self, state):

        for i in state[2].values():
            if i != 0:
                return False

        print(f"{state} is goal state!")
        return True

    def get_hash(self, state):
        mytext = []
        for k, v in state[2].items():
            mytext.append(f"{k}|{v}")
        dirt_txt = "__".join(mytext)
        return f"X{state[0]}Y{state[1]}|{dirt_txt}"

    def get_manhattan_distance(self, state):

        pos_x, pos_y = state[0], state[1]

        distance = 999999
        for k, v in state[2].items():
            x_coord = int(k.split('|')[0])
            y_coord = int(k.split('|')[1])
            distance = min(abs(pos_x - x_coord) + abs(pos_y - y_coord), distance)
        return distance

    # def get_jumper_amount_to_the_dirt(self,cleaner_pos_x,cleaner_pos_y,dirt_pos_x,dirt_pos_y):
    #     pos_x_min = min(dirt_pos_x,cleaner_pos_x)
    #     pos_y_max = max(dirt_pos_y,cleaner_pos_y)
    #
    #     for i in range(dirt_pos_x-cleaner_pos_x):

    # for row in self.environment.grid_matrix:

    def get_my_heuristic_value(self, state):
        pos_x, pos_y = state[0], state[1]
        distances = []
        x_coord_sum = 0
        y_coord_sum = 0
        count_of_dirt = 0
        for k, v in state[2].items():
            x_coord = int(k.split('|')[0])
            y_coord = int(k.split('|')[1])
            x_coord_sum += v * x_coord
            y_coord_sum += v * y_coord
            count_of_dirt += v

        average_position_of_dirts_x = int(x_coord_sum / count_of_dirt)
        average_position_of_dirts_y = int(y_coord_sum / count_of_dirt)
        euclidean_to_avg_point = ((average_position_of_dirts_x - pos_x) ** 2 + (average_position_of_dirts_y - pos_y) ** 2) ** .5
        # manhattan_distance = self.get_manhattan_distance(state)
        # if euclidean_to_avg_point
        # euclidean_to_avg_point
        return euclidean_to_avg_point

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

            print(f"new node is expanding: {node}")
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

    def run_bfs(self):

        nodes_expanded = []

        dot_booelans = self.environment.get_dot_booelans_type3()

        start_node = (self.agent.position_x, self.agent.position_y, dot_booelans)

        self.fringe_fifo.put((start_node, [], []))

        while not self.fringe_fifo.empty():

            node = self.fringe_fifo.get()

            state = node[0]
            actions = node[1]
            costs = node[2]

            hash_txt = self.get_hash(state)

            nodes_expanded.append(hash_txt)

            if self.goal_test(state):
                return len(self.nodes_visited), actions, sum(node[2])

            print(f"new node is expanding: {node}")
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
                    self.fringe_fifo.put((successor_state, successor_path_history, successor_cost_history))

        return []

    def run_ucs(self):

        nodes_expanded = []

        dot_booelans = self.environment.get_dot_booelans_type3()

        start_node = (self.agent.position_x, self.agent.position_y, dot_booelans)

        self.fringe_ucs.put((0, 0, start_node, []))  # cumulative cost, slrdu ordering for tiebreaking, node, actions
        fringe_set = []
        while not self.fringe_ucs.empty():

            try:
                node = self.fringe_ucs.get()

                state = node[2]
                actions = node[3]
                cumulative_cost = node[0]

                hash_txt = self.get_hash(state)

                nodes_expanded.append(hash_txt)

                if self.goal_test(state):
                    return len(self.nodes_visited), actions, node[0]

                print(f"\nnew node is expanding: {node}")

                self.nodes_visited[hash_txt] = 1

                successors = self.agent.get_successors_2(state=state)
                # reversed(successors)
                for successor in successors:

                    successor_state = successor[0]
                    successor_action = successor[1]
                    successor_cost = successor[2]

                    successor_state_hash = self.get_hash(successor_state)

                    if successor_state_hash not in nodes_expanded:
                        fringe_set.append(successor_state_hash)
                        successor_path_history = actions.copy()
                        successor_path_history.append(successor_action)

                        self.fringe_ucs.put((cumulative_cost + successor_cost, len(fringe_set), successor_state, successor_path_history))
                        print(f"fringe ekleniyor -> {(cumulative_cost + successor_cost, len(fringe_set), successor_state, successor_path_history)}")
            except Exception as e:
                print(str(e))
        return []

    def run_greedy(self):

        nodes_expanded = []

        dot_booelans = self.environment.get_dot_booelans_type3()

        start_node = (self.agent.position_x, self.agent.position_y, dot_booelans)

        self.fringe_ucs.put((0, 0, start_node, [], 0))  # manhattan distance, slrdu ordering for tiebreaking, node, actions,total_cost
        fringe_set = []
        while not self.fringe_ucs.empty():

            try:
                node = self.fringe_ucs.get()

                state = node[2]
                actions = node[3]
                cumulative_cost = node[4]

                hash_txt = self.get_hash(state)

                nodes_expanded.append(hash_txt)

                if self.goal_test(state):
                    return len(self.nodes_visited), actions, node[4]

                # print(f"\nnew node is expanding: {node}")

                self.nodes_visited[hash_txt] = 1

                successors = self.agent.get_successors_2(state=state)
                # reversed(successors)

                for successor in successors:

                    successor_state = successor[0]
                    successor_action = successor[1]
                    successor_cost = successor[2]
                    successor_distance = self.get_manhattan_distance(successor_state)
                    successor_state_hash = self.get_hash(successor_state)

                    if successor_state_hash not in nodes_expanded:
                        fringe_set.append(successor_state_hash)
                        successor_path_history = actions.copy()
                        successor_path_history.append(successor_action)

                        self.fringe_ucs.put((successor_distance, len(fringe_set), successor_state, successor_path_history, cumulative_cost + successor_cost))
                        # print(f"fringe ekleniyor -> {(cumulative_cost + successor_cost, len(fringe_set), successor_state, successor_path_history)}")
            except Exception as e:
                print(str(e))
        return []

    def run_astar(self):

        nodes_expanded = []

        dot_booelans = self.environment.get_dot_booelans_type3()

        start_node = (self.agent.position_x, self.agent.position_y, dot_booelans)

        self.fringe_ucs.put((0, 0, start_node, [], 0))  # f + h , slrdu ordering for tiebreaking, node, actions,total_cost
        fringe_set = []
        while not self.fringe_ucs.empty():

            try:
                node = self.fringe_ucs.get()

                state = node[2]
                actions = node[3]
                cumulative_cost = node[4]

                hash_txt = self.get_hash(state)

                nodes_expanded.append(hash_txt)

                if self.goal_test(state):
                    return len(self.nodes_visited), actions, node[4]

                print(f"\nnew node is expanding: {node}")

                self.nodes_visited[hash_txt] = 1

                successors = self.agent.get_successors_2(state=state)
                # reversed(successors)

                for successor in successors:

                    successor_state = successor[0]
                    successor_action = successor[1]
                    successor_cost = successor[2]
                    successor_distance = self.get_manhattan_distance(successor_state)
                    successor_state_hash = self.get_hash(successor_state)

                    if successor_state_hash not in nodes_expanded:
                        fringe_set.append(successor_state_hash)
                        successor_path_history = actions.copy()
                        successor_path_history.append(successor_action)

                        self.fringe_ucs.put((cumulative_cost + successor_cost + successor_distance, len(fringe_set), successor_state, successor_path_history, cumulative_cost + successor_cost))
                        print(f"fringe ekleniyor -> {(cumulative_cost + successor_cost + successor_distance, len(fringe_set), successor_state, successor_path_history)}")
            except Exception as e:
                print(str(e))
        return []

    def run_astar_2(self):

        nodes_expanded = []

        dot_booelans = self.environment.get_dot_booelans_type3()

        start_node = (self.agent.position_x, self.agent.position_y, dot_booelans)

        self.fringe_ucs.put((0, 0, start_node, [], 0))  # f + h , slrdu ordering for tiebreaking, node, actions,total_cost
        fringe_set = []
        while not self.fringe_ucs.empty():

            try:
                node = self.fringe_ucs.get()

                state = node[2]
                actions = node[3]
                cumulative_cost = node[4]

                hash_txt = self.get_hash(state)

                nodes_expanded.append(hash_txt)

                if self.goal_test(state):
                    return len(self.nodes_visited), actions, node[4]

                # print(f"\nnew node is expanding: {node}")

                self.nodes_visited[hash_txt] = 1

                successors = self.agent.get_successors_2(state=state)
                # reversed(successors)

                for successor in successors:

                    successor_state = successor[0]
                    successor_action = successor[1]
                    successor_cost = successor[2]
                    successor_distance = self.get_my_heuristic_value(successor_state)
                    successor_state_hash = self.get_hash(successor_state)

                    if successor_state_hash not in nodes_expanded:
                        fringe_set.append(successor_state_hash)
                        successor_path_history = actions.copy()
                        successor_path_history.append(successor_action)

                        self.fringe_ucs.put((cumulative_cost + successor_cost + successor_distance, len(fringe_set), successor_state, successor_path_history, cumulative_cost + successor_cost))
                        # print(f"fringe ekleniyor -> {(cumulative_cost + successor_cost, len(fringe_set), successor_state, successor_path_history)}")
            except Exception as e:
                print(str(e))
        return []
