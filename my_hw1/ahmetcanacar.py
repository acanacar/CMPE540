import argparse
import queue


class Tiles:
    def __init__(self):
        self.matrix = [[None, None, None],
                       [None, "c", None],
                       [None, None, None]]

    @property
    def center(self):
        return self.matrix[1][1]

    @property
    def left(self):
        return self.matrix[1][0]

    @property
    def right(self):
        return self.matrix[1][2]

    @property
    def down(self):
        return self.matrix[2][1]

    @property
    def up(self):
        return self.matrix[0][1]


class GridEnvironment:
    def __init__(self, grid_matrix):
        # self.grid_matrix = [['x', 'x', ' ', ' ', ' '],
        #                     [' ', '1', 'x', '1', 'j'],
        #                     [' ', 'j', 'x', ' ', '2'],
        #                     ['x', 'x', 'x', ' ', ' ']]
        self.grid_matrix = grid_matrix
        self.row_number = len(grid_matrix)
        self.col_number = len(grid_matrix[0])
        self.set_dirts_as_integers()

    def get_dot_booelans(self):
        d = {}
        for i in range(self.row_number):
            for j in range(self.col_number):
                val = self.grid_matrix[i][j]
                if type(val) == int:
                    d[f"x{i}y{j}"] = val
        return d

    def get_dot_booelans_type3(self):
        d = {}
        for i in range(self.row_number):
            for j in range(self.col_number):
                val = self.grid_matrix[i][j]
                if type(val) == int:
                    d[f"{i}|{j}"] = val
        return d

    def get_dot_booelans_type2(self):
        d = []
        for i in range(self.row_number):
            for j in range(self.col_number):
                val = self.grid_matrix[i][j]
                if type(val) == int and val > 0:
                    d.append([f"x{i}_y{j}_val"])
        return '__'.join(d)

    def set_dirts_as_integers(self):
        for i in range(self.row_number):
            for j in range(self.col_number):
                try:
                    self.grid_matrix[i][j] = int(self.grid_matrix[i][j])
                except ValueError:
                    continue
                except Exception as e:
                    print(str(e))

    def get_available_grids_around_agent(self, agent) -> Tiles:
        '''

        :param agent: Agent object
        :return: grid locations around the agent.
        '''
        grids_around_agent = Tiles()
        posx, posy = agent.position_x, agent.position_y
        for x_inc in [-1, 0, 1]:

            for y_inc in [-1, 0, 1]:

                new_pos_x = posx + x_inc
                new_pos_y = posy + y_inc

                if (new_pos_x < 0) or (new_pos_x > self.row_number - 1) or \
                        (new_pos_y < 0) or (new_pos_y > self.col_number - 1) or \
                        self.grid_matrix[new_pos_x][new_pos_y] == 'x':

                    grids_around_agent.matrix[x_inc + 1][y_inc + 1] = "UNAVAILABLE"

                elif self.grid_matrix[new_pos_x][new_pos_y] == "j":

                    if x_inc * y_inc == 0:  # means that not diagonal move

                        if self.grid_matrix[new_pos_x + x_inc][new_pos_y + y_inc] == 'x':
                            grids_around_agent.matrix[x_inc + 1][y_inc + 1] = "UNAVAILABLE"

                        else:
                            grids_around_agent.matrix[x_inc + 1][y_inc + 1] = self.grid_matrix[new_pos_x][new_pos_y]  # j

                else:
                    grids_around_agent.matrix[x_inc + 1][y_inc + 1] = self.grid_matrix[new_pos_x][new_pos_y]

        return grids_around_agent

    def is_all_grids_clean(self):
        if self.dirt_number == 0:
            return True
        return False

    @property
    def dirt_number(self):
        total_dirt = 0
        for r in self.grid_matrix:
            for v in r:
                if type(v) == int:
                    total_dirt += 1
        return total_dirt


class Agent:
    def __init__(self, position, environment: GridEnvironment):
        self.position_x = position[0]
        self.position_y = position[1]
        self.environment = environment
        self.environment.grid_matrix[self.position_x][self.position_y] = ' '
        self.observed_map = {}

    def get_successors_2(self, state):
        '''tasarimdan dolayi parametre almadan agent lokasyonundan yararlanarak node expand etmeye yariyor.'''

        self.position_x = state[0]
        self.position_y = state[1]
        dirt_dict = state[2]
        for k, v in dirt_dict.items():
            x_coord = int(k.split('|')[0])
            y_coord = int(k.split('|')[1])
            self.environment.grid_matrix[x_coord][y_coord] = v

        successors = []

        grids_around_him = self.environment.get_available_grids_around_agent(self)

        if type(grids_around_him.center) == int:

            if grids_around_him.center > 0:
                dot_booleans = state[2].copy()
                dot_booleans[f"{self.position_x}|{self.position_y}"] -= 1
                # self.environment.grid_matrix[self.position_x][self.position_y] -= 1
                successors.append(([self.position_x, self.position_y, dot_booleans], "suck", 5))

        if grids_around_him.left != "UNAVAILABLE":
            dot_booleans = state[2].copy()
            if grids_around_him.left == 'j':
                successors.append(([self.position_x, self.position_y - 2, dot_booleans], "left", 1))
            else:
                successors.append(([self.position_x, self.position_y - 1, dot_booleans], "left", 1))

        if grids_around_him.right != "UNAVAILABLE":
            dot_booleans = state[2].copy()
            if grids_around_him.right == 'j':
                successors.append(([self.position_x, self.position_y + 2, dot_booleans], "right", 1))
            else:
                successors.append(([self.position_x, self.position_y + 1, dot_booleans], "right", 1))

        if grids_around_him.down != "UNAVAILABLE":
            dot_booleans = state[2].copy()
            if grids_around_him.down == 'j':
                successors.append(([self.position_x + 2, self.position_y, dot_booleans], "down", 2))
            else:
                successors.append(([self.position_x + 1, self.position_y, dot_booleans], "down", 2))

        if grids_around_him.up != "UNAVAILABLE":
            dot_booleans = state[2].copy()
            if grids_around_him.up == 'j':
                successors.append(([self.position_x - 2, self.position_y, dot_booleans], "up", 2))
            else:
                successors.append(([self.position_x - 1, self.position_y, dot_booleans], "up", 2))

        return successors


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

        # print(f"{state} is goal state!")
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

    def find_nearest_by_manhattan_dist(self, state):
        pos_x, pos_y = state[0], state[1]
        distance = 999999
        result_kir = []
        for k, v in state[2].items():
            x_coord = int(k.split('|')[0])
            y_coord = int(k.split('|')[1])
            manhattan_d = abs(pos_x - x_coord) + abs(pos_y - y_coord)
            if manhattan_d < distance:
                result_kir = (x_coord, y_coord, v)
                distance = manhattan_d
        return result_kir

    def get_my_heuristic_value(self, state):
        nearest_dirt = self.find_nearest_by_manhattan_dist(state)
        pos_x, pos_y = state[0], state[1]
        distance = ((pos_x - nearest_dirt[0]) ** 2 + (pos_y - nearest_dirt[1]) ** 2) ** .5
        # distance = 99999
        # for k, v in state[2].items():
        #     x_coord = int(k.split('|')[0])
        #     y_coord = int(k.split('|')[1])
        #     distance = min(
        #         ((pos_x - x_coord) ** 2 + (pos_y - y_coord) ** 2) ** .5,
        #         distance)

        # manhattan_distance = self.get_manhattan_distance(state)
        # if euclidean_to_avg_point
        # euclidean_to_avg_point
        return distance

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

                # print(f"\nnew node is expanding: {node}")

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
                        # print(f"fringe ekleniyor -> {(cumulative_cost + successor_cost, len(fringe_set), successor_state, successor_path_history)}")
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

                        self.fringe_ucs.put((cumulative_cost + successor_cost + successor_distance, len(fringe_set), successor_state, successor_path_history, cumulative_cost + successor_cost))
                        # print(f"fringe ekleniyor -> {(cumulative_cost + successor_cost + successor_distance, len(fringe_set), successor_state, successor_path_history)}")
            except Exception as e:
                print(str(e))
        return []

    def run_astar_2(self):

        nodes_expanded = []

        dot_booelans = self.environment.get_dot_booelans_type3()
        start_node = (self.agent.position_x, self.agent.position_y, dot_booelans)


        self.fringe_ucs.put((0, 0, start_node, [], 0,[self.get_my_heuristic_value(start_node)]))  # f + h , slrdu ordering for tiebreaking, node, actions,total_cost,h
        fringe_set = []
        while not self.fringe_ucs.empty():

            try:
                node = self.fringe_ucs.get()

                state = node[2]
                actions = node[3]
                cumulative_cost = node[4]
                heuristic_values = node[5]

                hash_txt = self.get_hash(state)

                nodes_expanded.append(hash_txt)

                if self.goal_test(state):
                    return len(self.nodes_visited), actions, node[4],node[5]

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
                        successor_heuristic_value_history = heuristic_values.copy()
                        successor_heuristic_value_history.append(successor_distance)

                        self.fringe_ucs.put((cumulative_cost + successor_cost + successor_distance, len(fringe_set),
                                             successor_state, successor_path_history, cumulative_cost + successor_cost,successor_heuristic_value_history))
                        # print(f"fringe ekleniyor -> {(cumulative_cost + successor_cost, len(fringe_set), successor_state, successor_path_history)}")
            except Exception as e:
                print(str(e))
        return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("search_type")
    parser.add_argument("file_path")
    args = parser.parse_args()
    with open(rf"{args.file_path}") as f:
        lines = f.readlines()

    environment_info = [list(row[:-1]) for row in lines]
    agent_position = [(i, j) for i, r in enumerate(environment_info) for j, c in enumerate(r) if c == "c"][0]

    env = GridEnvironment(grid_matrix=environment_info)

    agent = Agent(environment=env, position=agent_position)

    simulator = Simulator(agent=agent, environment=env)
    heuristic_values = None
    if args.search_type == 'DFS':
        (count_of_nodes, actions, costs) = simulator.run_dfs()
    if args.search_type == 'BFS':
        (count_of_nodes, actions, costs) = simulator.run_bfs()
    if args.search_type == 'UCS':
        (count_of_nodes, actions, costs) = simulator.run_ucs()
    if args.search_type == 'GS':
        (count_of_nodes, actions, costs) = simulator.run_greedy()
    if args.search_type == 'A*1':
        (count_of_nodes, actions, costs) = simulator.run_astar()
    if args.search_type == 'A*2':
        (count_of_nodes, actions, costs,heuristic_values) = simulator.run_astar_2()

    print(f"number of expanded nodes : {count_of_nodes}")
    print(f"path : {actions}")
    print(f"cost of the solution : {costs}")
    if heuristic_values:
        print("heuristic values :", *heuristic_values)


if __name__ == '__main__':
    main()
