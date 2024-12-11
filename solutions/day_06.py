from . import base_solution as bs


def get_step(direction) -> tuple[int, int]:
    if direction == 0:
        return -1, 0    # Up, top row has index 0...
    if direction == 1:
        return 0, 1     # to right
    if direction == 2:
        return 1, 0     # down
    if direction == 3:
        return 0, -1    # to the left


def do_step(i, j, direction) -> tuple[int, int]:
    di, dj = get_step(direction)
    return  i + di, j + dj

def do_turn(i, j, direction) -> tuple[int, int, int]:
    # Do a step back
    d = (direction + 2) % 4  # Two turns are 180 deg rot, so "backwards"
    i, j = do_step(i, j, d)
    # Now, turn right
    direction = (direction + 1) % 4
    # And do a stop
    i, j = do_step(i, j, direction)
    return i, j, direction


class SolutionDay06(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.grid = None
        self.start = None
        self.n = -1
        self.m = -1

    def build_grid(self):
        input_file_path = self.get_input_file_path()

        self.grid = []
        self.start = None
        with open(input_file_path, 'r') as of:
            i = 0
            while line := of.readline():
                line = line.strip()
                if not self.start and line.find('^') > -1:
                   self.start = (i, line.find('^'))
                self.grid.append(list(line))
                i += 1

        self.m, self.n = len(self.grid), len(self.grid[0])

    def print_grid(self):
        start_val = self.grid[self.start[0]][self.start[1]]
        self.grid[self.start[0]][self.start[1]] = '^'
        for row in self.grid:
            print(''.join([str(cell) for cell in row]))
        self.grid[self.start[0]][self.start[1]] = start_val

    def check_for_loop(self, i, j, direction) -> bool:
        # Make a deep copy of the grid, to not "pollute" the original one with this hypothetical paths
        local_grid = [row.copy() for row in self.grid]

        while True:
            if i == -1 or i == self.m or j == -1 or j == self.n:
                # We're out of the grid. No loop detected
                return False

            if local_grid[i][j] == '#':
                i, j, direction = do_turn(i, j, direction)
            else:
                cur_val = local_grid[i][j]
                if cur_val == '.':
                    # Never been here before. Mark it with the current direction
                    local_grid[i][j] = 2 ** direction
                else:
                    # We've been here before...
                    if cur_val & (2 ** direction) > 0:
                        # We detected a loop!
                        return True
                    # Update the grid cell
                    local_grid[i][j] = cur_val + (2 ** direction)
                # Do a step
                i, j = do_step(i, j, direction)

    def _star_1(self) -> None:
        """Fill in description and code...

        :return:
        """
        self.build_grid()

        path_length = 0
        direction = 0
        i, j = self.start
        while True:
            if i == -1 or i == self.m or j == -1 or j == self.n:
                # We're out of the grid
                return path_length

            if self.grid[i][j] == '#':
                i, j, direction = do_turn(i, j, direction)
            else:
                if self.grid[i][j] != 'X':
                    # We're on a new field
                    path_length += 1
                    # Mark it as visited
                    self.grid[i][j] = 'X'

                # Go to the next field
                i, j = do_step(i, j, direction)

    def _star_2(self) -> None:
        """Fill in description and code...

        :return:
        """
        self.build_grid()

        obstacle_count = 0
        # Walk along the grid, as wi did for star 1
        direction = 0
        i, j = self.start
        self.grid[i][j] = 0
        i, j = do_step(i, j, direction)
        while True:
            if i == -1 or i == self.m or j == -1 or j == self.n:
                # We're out of the grid
                return obstacle_count

            if self.grid[i][j] == '#':
                i, j, direction = do_turn(i, j, direction)
            else:
                if self.grid[i][j] == '.':
                    # Never been here before. Check, if adding a block here would make a loop!
                    self.grid[i][j] = '#'
                    # So, IF here would be an obstacle, we would do a turn
                    ni, nj, nd = do_turn(i, j, direction)
                    # Check for a loop for this hypothetical new position and direction
                    if self.check_for_loop(ni, nj, nd):
                        obstacle_count += 1
                    # Then, mark it with the real value (instead of the obstacle) and continue the original path
                    self.grid[i][j] = 2**direction
                else:
                    # We've been here. Add the current direction to the marks.
                    self.grid[i][j] = self.grid[i][j] + (2**direction)

                # Go to the next field
                i, j = do_step(i, j, direction)

# ZKB-points at start: 424
# ZKB-points with star 1: 501 (was value 77 points)
# Star 2: 1220 -> 1270 (50 points)
