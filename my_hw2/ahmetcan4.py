import argparse
import copy


class GridEnvironment2:

    def __init__(self, grid_matrix):
        self.grid_matrix = grid_matrix
        self.row_number = len(grid_matrix)
        self.col_number = len(grid_matrix[0])
        self.agentPositions = []
        self.process_grid_matrix()
        self.dirt_eaten_us = 0
        self.dirt_eaten_others = 0
        self.my_cleaner_move_hist = []

    def process_grid_matrix(self):

        for i in range(self.row_number):

            for j in range(self.col_number):
                self.process_grid_value(i, j, self.grid_matrix[i][j])

        self.agentPositions.sort()
        # self.agentPositions = [[i == 0, pos] for i, pos in self.agentPositions]

    def process_grid_value(self, x, y, val):
        try:
            self.agentPositions.append([int(val), [x, y]])
        except ValueError as e:
            # if val == 'x':
            #     self.walls[x][y] = True
            # elif val == '.':
            #     self.dirt[x][y] = True
            if val == 'c':
                self.agentPositions.append([0, [x, y]])
            # elif val == '.':
            #     self.dirt_positions[x][y] = True

    def get_dirt_number(self):
        count = 0
        for i in range(self.row_number):
            for j in range(self.col_number):
                if self.grid_matrix[i][j] == ".":
                    count += 1
        return count

    def is_agents_crashed(self):
        for agent_index, [agent_position_x, agent_position_y] in self.agentPositions[1:]:
            if self.agentPositions[0][0] == agent_position_x and self.agentPositions[0][1] == agent_position_y:
                return True
        return False


class Simulator:
    def __init__(self, env, n_actions, start_indice=0):
        self.start_indice = start_indice
        self.env = env
        self.n_actions = n_actions
        self.util_calls = 0
        self.first_move = None
        self.last_util_for_my_cleaner = -999999

    def is_valid_action(self, grid_matrix, action, agent_position):
        agent_x = agent_position[0]
        agent_y = agent_position[1]
        new_position = None
        if action == 'left':
            new_position = (agent_x, agent_y - 1)
        elif action == 'right':
            new_position = (agent_x, agent_y + 1)
        elif action == 'down':
            new_position = (agent_x + 1, agent_y)
        elif action == 'up':
            new_position = (agent_x - 1, agent_y)

        if new_position:
            new_position_x = new_position[0]
            new_position_y = new_position[1]
            if (new_position_x > self.env.row_number) or new_position_x < 0:
                return False
            elif (new_position_y > self.env.col_number) or new_position_y < 0:
                return False
            elif grid_matrix[new_position_x][new_position_y] == 'x':
                return False
        else:

            if action == 'stop':
                pass
            elif action == 'suck':
                if grid_matrix[agent_x][agent_y] != ".":
                    return False

        return True

    def is_game_over(self, env):
        return (not env.get_dirt_number()) or env.is_agents_crashed()

    def get_new_state(self, action, env, agent_position, agent_index):

        new_env = copy.deepcopy(env)
        agent = new_env.agentPositions[agent_index]
        agent_x = agent[1][0]
        agent_y = agent[1][1]

        if action == 'suck':
            new_env.grid_matrix[agent_x][agent_y] = ' '
            if agent_index == 0:
                new_env.dirt_eaten_us += 1
            else:
                new_env.dirt_eaten_others += 1
        elif action == 'left':
            agent[1] = [agent_x, agent_y - 1]
            # agent[1][1] -= 1
        elif action == 'right':
            agent[1] = [agent_x, agent_y + 1]
        elif action == 'down':
            agent[1] = [agent_x + 1, agent_y]
        elif action == 'up':
            agent[1] = [agent_x - 1, agent_y]

        return new_env

    def get_successor_states(self, agent_index, env):
        agent_position = env.agentPositions[agent_index][1]
        successor_states = []
        for action in ['left', 'right', 'down', 'up', 'stop', 'suck']:
            if self.is_valid_action(env.grid_matrix, action, agent_position):
                new_env = self.get_new_state(action, env, agent_position, agent_index)
                if agent_index == 0:
                    new_env.my_cleaner_move_hist.append(action)
                successor_states.append(new_env)

        return successor_states

    def static_evaluation(self, game_env):
        if game_env.is_agents_crashed():
            return -100
        return game_env.dirt_eaten_us - game_env.dirt_eaten_others

    def minimax(self, env, agent_index, current_depth, max_player):
        self.util_calls += 1
        print(f"agent_index:{agent_index} , current_depth: {current_depth}")

        if self.is_game_over(env):
            self.first_move = env.my_cleaner_move_hist[0]
            score = self.static_evaluation(env)
            print(f"BITTII")
            return score
        if current_depth == 0:
            return self.last_util_for_my_cleaner
        next_agent_index = (agent_index + 1) % len(env.agentPositions)
        max_player_f = not bool(next_agent_index)
        if max_player:
            max_util = float('-inf')
            for successor_state in self.get_successor_states(agent_index, env):
                util = self.minimax(env=successor_state, agent_index=next_agent_index, current_depth=current_depth - 1,
                                    max_player=max_player_f)
                max_util = max(max_util, util)
            self.last_util_for_my_cleaner = max_util
            return max_util
        elif agent_index % 2 == 0:
            utils = []
            for successor_state in self.get_successor_states(agent_index, env):
                util = self.minimax(env=successor_state, agent_index=next_agent_index, current_depth=current_depth - 1,
                                    max_player=max_player_f)
                utils.append(util)
            if len(utils) > 0:
                util_mean = sum([u for u in utils]) / len(utils)
                return util_mean
        else:
            min_util = float('inf')
            for successor_state in self.get_successor_states(agent_index, env):
                util = self.minimax(env=successor_state, agent_index=next_agent_index, current_depth=current_depth - 1,
                                    max_player=max_player_f)
                min_util = min(min_util, util)
            return min_util

    def minimax_alpha_beta(self, env, agent_index, current_depth, max_player, alpha, beta):
        self.util_calls += 1
        print(f"agent_index:{agent_index} , current_depth: {current_depth}")

        if self.is_game_over(env):
            self.first_move = env.my_cleaner_move_hist[0]
            score = self.static_evaluation(env)
            print(f"BITTII")
            return score
        if current_depth == 0:
            return self.last_util_for_my_cleaner
        next_agent_index = (agent_index + 1) % len(env.agentPositions)
        max_player_f = not bool(next_agent_index)
        if max_player:
            max_util = -9999999
            for successor_state in self.get_successor_states(agent_index, env):
                util = self.minimax_alpha_beta(env=successor_state,
                                               agent_index=next_agent_index,
                                               current_depth=current_depth - 1,
                                               max_player=max_player_f, alpha=alpha, beta=beta)
                max_util = max(max_util, util)
                alpha = max(alpha, util)
                if beta <= alpha:
                    break
            self.last_util_for_my_cleaner = max_util
            return max_util

        elif agent_index % 2 == 0:
            utils = []
            for successor_state in self.get_successor_states(agent_index, env):
                util = self.minimax_alpha_beta(env=successor_state, agent_index=next_agent_index,
                                               current_depth=current_depth - 1,
                                               max_player=max_player_f, alpha=alpha, beta=beta)
                utils.append(util)
            if len(utils) > 0:
                util_mean = sum([u for u in utils]) / len(utils)
                return util_mean

        else:
            min_util = +9999999
            for successor_state in self.get_successor_states(agent_index, env):
                util = self.minimax_alpha_beta(env=successor_state, agent_index=next_agent_index,
                                               current_depth=current_depth - 1,
                                               max_player=max_player_f, alpha=alpha, beta=beta)
                min_util = min(min_util, util)
                beta = min(beta, util)
                if beta <= alpha:
                    break
            return min_util

    def run_minimax(self):
        score = self.minimax(self.env, agent_index=0, current_depth=self.n_actions, max_player=True)
        return score

    def run_minimax_alpha_beta(self):
        score = self.minimax_alpha_beta(self.env, agent_index=0, current_depth=self.n_actions, max_player=True,alpha=float('-inf'),beta=float('inf'))
        return score

    # def run_minimax_(self):
    #     action_no = 0
    #     agentPositions = self.env.agentPositions.copy()
    #     agent_index = 0
    #
    #     agent = agentPositions[agent_index]
    #     agentPosition = agent[1]
    #     env_matrix = self.env.grid_matrix.copy()
    #     action = self.get_action(agentPosition,agent_index,env_matrix)
    #
    #     for action in ['left', 'right', 'down', 'up', 'stop', 'suck']:
    #         if self.is_valid_action(env_matrix,action,agentPosition):
    #             pass
    #         self.minimax(action=action, currentDepth=0, currentAgentIndex=0, max_player=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("search_type")
    parser.add_argument("file_path")
    parser.add_argument("n_actions")
    args = parser.parse_args()

    # args = argparse.Namespace()
    # args.file_path = r"/Users/acanacar/PycharmProjects/CMPE540/my_hw2/test_cases/init1.txt"
    # args.search_type = "min-max"
    # args.n_actions = 5

    with open(rf"{args.file_path}") as f:
        lines = f.readlines()

    environment_info = [list(row[:-1]) for row in lines]
    # agent_position = [(i, j) for i, r in enumerate(environment_info) for j, c in enumerate(r) if c == "c"][0]

    env = GridEnvironment2(grid_matrix=environment_info)
    simulator = Simulator(env=env, n_actions=args.n_actions)
    if args.search_type == "min-max":
        utility_score = simulator.run_minimax()
        print(f"Action: {simulator.first_move} ")
        print(f"Value: {utility_score}")
        print(f"Util calls: {simulator.util_calls}")
    if args.search_type == "alpha-beta":
        utility_score = simulator.run_minimax_alpha_beta()
        print(f"Action: {simulator.first_move} ")
        print(f"Value: {utility_score}")
        print(f"Util calls: {simulator.util_calls}")

    # run(env,args.n_actions)
    print('finito')


if __name__ == '__main__':
    main()
