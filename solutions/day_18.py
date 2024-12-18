import collections

from . import base_solution as bs


class SolutionDay18(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.n = 7 if self.is_example else 71   # Grid size, is a square
        self.grid = None
        self.obstacles = None

    def read_input(self):
        """Reads the input, i.e. builds the list of obstacles

        :return:
        """
        self.obstacles = []
        input_file_path = self.get_input_file_path()
        with open(input_file_path, 'r') as of:
            while line := of.readline():
                x, y = line.split(',')
                self.obstacles.append((int(x), int(y)))

    def build_grid(self, n_obstacle):
        """Rebuilds a grid with the n_obstacle first obstacles

        :param n_obstacle: (int) number of obstacles
        :return: None (grid is a member variable)
        """
        self.grid = []
        for i in range(self.n):
            self.grid.append(['.']*(self.n))

        for i in range(n_obstacle):
            x, y = self.obstacles[i]
            self.grid[y][x] = '#'

    def print_grid(self):
        for row in self.grid:
            print(''.join(row))

    def search_path(self) -> int:
        """Searches the (shortes) path from 0, 0 to (n-1), (n-1) in bfs manner

        :return: (int) Length of shortest path. If no path can be found: -1
        """
        # Now we do a breath first search
        que = collections.deque([(0, 0)])
        steps = 0
        while que:
            l = len(que)
            for _ in range(l):
                x, y = que.popleft()
                if x == self.n-1 and y == self.n-1:
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

        # Que is empty. We can't move anymore. So, no path found
        return -1

    def _star_1(self) -> int:
        """Fill in description and code...

        :return:
        """
        self.read_input()

        # Number of obstacles
        n_obstacle = 12 if self.is_example else 1024
        self.build_grid(n_obstacle)

        return self.search_path()


    def _star_2(self) -> tuple[int, int]:
        """Fill in description and code...

        :return:
        """
        if not self.obstacles:
            self.read_input()

        # Number of initial obstacles
        n_obstacle = 12 if self.is_example else 1024

        # Try brute force which obstacle is the first one, which blocks tus from finding a path
        while n_obstacle < len(self.obstacles):
            x, y = self.obstacles[n_obstacle-1]
            # Check if the current obstacle is (potentially) on the way
            # If so, we recompute the possible (left) paths
            if self.grid[y][x] == 'x':
                self.build_grid(n_obstacle)
                if self.search_path() < 0:
                    return x, y
            # Go to next obstacle
            n_obstacle += 1


# ZKB-Ranking:
# Star 1: 11.
# Star 2: 12.