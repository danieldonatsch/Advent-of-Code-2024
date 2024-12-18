import collections

from . import base_solution as bs


class SolutionDay18(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.n = None       # Grid size, is a square
        self.grid = None
        self.obstacles = None

    def read_input(self):
        self.n = 7 if self.is_example else 71

        self.grid = []
        for i in range(self.n):
            self.grid.append(['.']*(self.n))

        self.obstacles = []
        input_file_path = self.get_input_file_path()
        with open(input_file_path, 'r') as of:
            while line := of.readline():
                x, y = line.split(',')
                self.obstacles.append((int(x), int(y)))

    def print_grid(self):
        for row in self.grid:
            print(''.join(row))

    def _star_1(self) -> int:
        """Fill in description and code...

        :return:
        """
        self.read_input()

        # Number of obstacles
        n_obstacle = 12 if self.is_example else 1024

        for i in range(n_obstacle):
            x, y = self.obstacles[i]
            self.grid[y][x] = '#'

        self.print_grid()

        # Now we do a breath first search
        que = collections.deque([(0, 0)])
        steps = 0
        while que:
            l = len(que)
            for _ in range(l):
                x, y = que.popleft()
                if x == self.n-1 and y == self.n-1:
                    self.print_grid()
                    return steps
                # Check if we're still on the grid
                if 0 <= x < self.n and 0 <= y < self.n:
                    if self.grid[y][x] != '.':
                        continue
                    # Mark as visited
                    self.grid[y][x] = 'x'
                    # Add neighbours to the que:
                    for neighbour in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                        que.append(neighbour)
            steps += 1

        print("que is empty!")
        self.print_grid()

    def _star_2(self) -> int:
        """Fill in description and code...

        :return:
        """
        input_file_path = self.get_input_file_path()


# ZKB-Ranking:
# Star 1: 11.