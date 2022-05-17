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
        # self.set_dirts_as_integers()
        self.set_opponent_cleaners_as_integers()

    def get_dot_booelans(self):
        d = {}
        for i in range(self.row_number):
            for j in range(self.col_number):
                val = self.grid_matrix[i][j]
                if type(val) == int:
                    d[f"x{i}y{j}"] = val
        return d

    def get_dot_booelans_type2(self):
        d = []
        for i in range(self.row_number):
            for j in range(self.col_number):
                val = self.grid_matrix[i][j]
                if type(val) == int and val > 0:
                    d.append([f"x{i}_y{j}_val"])
        return '__'.join(d)

    def get_dot_booelans_type3(self):
        d = {}
        for i in range(self.row_number):
            for j in range(self.col_number):
                val = self.grid_matrix[i][j]
                if type(val) == int:
                    d[f"{i}|{j}"] = val
        return d

    def get_dot_booelans_type4(self):
        d = {}
        for i in range(self.row_number):
            for j in range(self.col_number):
                val = self.grid_matrix[i][j]
                if type(val) == int:
                    d[f"MinAgent{val}"] = f"{i}|{j}"
                elif val == ".":
                    d[f"Dirt{i}|{j}"] = 1
        return d


    def set_dirts_as_integers(self):
        for i in range(self.row_number):
            for j in range(self.col_number):
                try:
                    self.grid_matrix[i][j] = int(self.grid_matrix[i][j])
                except ValueError:
                    continue
                except Exception as e:
                    print(str(e))


    def set_opponent_cleaners_as_integers(self):
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

