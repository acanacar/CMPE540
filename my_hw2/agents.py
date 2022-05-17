class ExpectimaxAgent:
    def __init__(self, position, environment):
        self.position_x = position[0]
        self.position_y = position[1]
        self.environment = environment
        # self.environment.grid_matrix[self.position_x][self.position_y] = ' '

    def do_expectimax(self, game_state, action, current_depth, current_agent_index, isMax):
        pass

    def get_action(self, game_state):
        self.do_expectimax(game_state)
