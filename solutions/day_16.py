import collections

from . import base_solution as bs


class SolutionDay16(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.grid = None
        self.start = None
        self.end = None
        self.result_star_1 = None

    def read_input(self, double_grid=False) -> None:
        """Reads the input file and sets the member variables

        :param double_grid: (bool) if the grid width is doubled or not (star2 needs it double width)
        :return: None
        """
        input_file_path = self.get_input_file_path()
        self.grid = []
        with open(input_file_path, 'r') as of:
            # First part of the file is the starting grid
            while line := of.readline().strip():
                self.grid.append(list(line))

            # Get/check start and end
            self.start = len(self.grid)-2, 1
            assert self.grid[self.start[0]][self.start[1]] == 'S'
            self.end = 1, len(self.grid[1]) - 2
            assert self.grid[self.end[0]][self.end[1]] == 'E'

    def update_grid_cell(self, i, j, d, p):
        """Updates the prices for standing on this grid cell in all four directions.

        :param i: (int) vertical grid coordinate
        :param j: (int) horizontal grid coordinate
        :param d: (int) direction on which we step on the grid cell (0: N, 1: E, 2: S, 3: W)
        :param p: (int) price we pay to enter the cell
        :return:
        """
        if self.grid[i][j] == '.':
            self.grid[i][j] = [float('inf')] * 4
        became_cheaper = False
        # Compute the price for all four directions
        if p < self.grid[i][j][d]:
            self.grid[i][j][d] = p
            became_cheaper = True
        d = (d+1) % 4  # 90 Degree rotation
        p += 1000
        if p < self.grid[i][j][d]:
            self.grid[i][j][d] = p
            became_cheaper = True
        d = (d+1) % 4  # 180 Degree rotation
        p += 1000
        if p < self.grid[i][j][d]:
            self.grid[i][j][d] = p
            became_cheaper = True
        d = (d+1) % 4  # -90 Degree rotation
        p -= 1000
        if p < self.grid[i][j][d]:
            self.grid[i][j][d] = p
            became_cheaper = True
        return became_cheaper

    def _star_1(self) -> int:
        """Fill in description and code...

        We do a breath first search

        :return:
        """
        self.read_input()

        self.grid[self.end[0]][self.end[1]] = '.'

        # Add start position:
        self.grid[self.start[0]][self.start[1]] = '.'
        self.update_grid_cell(self.start[0], self.start[1], 1, 0)
        que = collections.deque([self.start])
        while que:
            l = len(que)
            for _ in range(l):
                i, j = que.popleft()
                # Check all four directions
                for d, (ni, nj) in enumerate([(i-1, j), (i, j+1), (i+1, j), (i, j-1)]):
                    if self.grid[ni][nj] == '#':
                        continue    # Wall
                    if self.update_grid_cell(ni, nj, d, self.grid[i][j][d]+1):
                        # Add to the que to check in next round
                        que.append((ni, nj))

        # Look for the minimal price we pay to reach the end
        self.result_star_1 = min(self.grid[self.end[0]][self.end[1]])
        return self.result_star_1


    def _star_2(self) -> int:
        """Fill in description and code...

        :return:
        """
        if self.result_star_1 is None:
            print("Need to run collect the first start first")
            self._star_1()

        steps = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        # We do a depth first search
        def dfs(i, j, d, p) -> bool:
            """Checks if the grid cell i, j, coming in from direction d is part of a successful path

            :param i: (int) vertical grid coordinate
            :param j: (int) horizontal grid coordinate
            :param d: (int) direction
            :param p: (int) expected price
            :return:
            """
            # Do we find the expected price?
            if p > self.result_star_1 or self.grid[i][j] == '#' or self.grid[i][j][d] != p:
                return False
            if (i, j) in good_positions and good_positions[(i,j)][d]:
                return True

            # Need to digg deeper:
            good_directions = [False] * 4
            found_way = False
            # Try to go forward:
            di, dj = steps[d]
            if dfs(i+di, j+dj, d, p+1):
                good_directions[d] = True
                found_way = True
            # Try a left turn and them moving:
            dl = (d-1) % 4
            di, dj = steps[dl]
            if dfs(i+di, j+dj, dl, p+1001):
                good_directions[dl] = True
                found_way = True
            # Try a right turn before moving:
            dr = (d+1) % 4
            di, dj = steps[dr]
            if dfs(i+di, j+dj, dr, p+1001):
                good_directions[dr] = True
                found_way = True
            if found_way:
                # Tricky: Compare with (potential previous) outcomes. Keep the good ones "True"!
                good_positions[(i, j)] = [x or y
                                          for x, y in zip(good_directions,
                                                          good_positions.get((i, j), [False, False, False, False]))]
            # Return a feedback, if we found a way or not
            return found_way


        # Add the end point, including the final direction to the good positions
        good_positions = {self.end: [False]*4}
        good_positions[self.end][self.grid[self.end[0]][self.end[1]].index(self.result_star_1)] = True

        # We start at start point, facing east...
        for direction, price in [(0, 1000), (1, 0), (2, 1000), (3, 2000)]:
            dfs(self.start[0], self.start[1], direction, price)

        '''
        # Print result visually
        for i, j in good_positions.keys():
            self.grid[i][j] = 'O'

        for row in self.grid:
            row = ['.' if isinstance(item, list) else item for item in row]
            print("".join(row))
        '''

        return len(good_positions)


    # ZKB Ranking:
# Star 1: Position 13
# Star 2: Position 16
