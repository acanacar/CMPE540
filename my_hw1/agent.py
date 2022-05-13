from my_hw1.environment import GridEnvironment
import queue


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
