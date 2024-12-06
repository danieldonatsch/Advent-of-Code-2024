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
                # We're on an obstacle. Shouldn't be. Do a step back
                d = (direction + 2) % 4     # Two turns are 180 deg rot, so "backwards"
                i, j = do_step(i, j, d)
                # Now, turn right
                direction = (direction + 1) % 4
                # And do a stop
                i, j = do_step(i, j, direction)
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
        input_file_path = self.get_input_file_path()

# ZKB-points at start: 424
# ZKB-points with star 1: 501 (was value 77 points)
