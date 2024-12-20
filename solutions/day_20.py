import collections
from collections import defaultdict

from . import base_solution as bs


class SolutionDay20(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.start = None
        self.end = None
        self.grid = []
        self.n = None
        self.m = None

    def read_input(self) -> None:
        """Reads the input file, builds the grid with the walls and the racetrack, finds start and end position.

        :return:
        """
        input_file_path = self.get_input_file_path()
        with open(input_file_path, 'r') as of:
            while line := of.readline().strip():
                if (x := line.find('S')) > 0:
                    self.start = (len(self.grid), x)
                if (x := line.find('E')) > 0:
                    self.end = (len(self.grid), x)
                self.grid.append(list(line))

        self.n = len(self.grid)
        self.m = len(self.grid[0])


    def find_shortest_path(self):
        """Looks for the shortest path and add the number of steps needed to reach each position on the racetrack

        :return:
        """
        # Get start point and convert it into a usual point
        i, j = self.start
        self.grid[i][j] = '.'
        # The que of positions we need to check next. At first, it wasn't clear, that only one track exists.
        que = collections.deque([(i, j)])
        steps = 0
        while que:
            l = len(que)
            if l > 1:
                print(f"Case with more than one option at {i=}, {j=}")
            for _ in range(l):
                i, j = que.popleft()
                self.grid[i][j] = steps
                for ni, nj in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
                    if self.grid[ni][nj] == '.':
                        que.append((ni, nj))
                    elif self.grid[ni][nj] == 'E':
                        self.grid[ni][nj] = steps+1
                        return
            # Do one step
            steps += 1

    def print_grid(self):
        for row in self.grid:
            print(''.join(str(x) for x in row))

    def check_cheat(self, i, j) -> tuple[int, int]:
        """Checks a position on the grid: if it is part of a wall figure out if going through it would be a shortcut.

        :param i: (int) vertical grid position
        :param j: (int) horizontal grid position
        :return:
        """
        if self.grid[i][j] != '#':
            # It's not a wall. No shortcut possible
            return 0, 0

        # Compute horizontal and vertical shortcut (possibilities)
        short_cuts = []
        for di, dj in [(1, 0), (0, 1)]:
            if self.grid[i-di][j-dj] == '#' or self.grid[i+di][j+dj] == '#':
                short_cuts.append(0)
            else:
                short_cuts.append(max(0, abs(self.grid[i-di][j-dj] - self.grid[i+di][j+dj]) - 2))
        return short_cuts[0], short_cuts[1]

    def get_all_cheats(self, i: int, j: int, cheats: dict) -> dict:
        """Computes all possible cheats under the assumption we're currently on grid cell i, j,

        :param i: (int) vertical grid position
        :param j: (int) horizontal grid position
        :param cheats: (dict) key: length of the shortcut, value: number of shortcuts found.
        :return: (dict) the updated cheats dict
        """
        # Compute the "field": All possible cells which can be reached within max_step steps if there would be no wall.
        max_step = 20
        for di in range(-max_step, max_step+1):
            for dj in range(-max_step+abs(di), max_step-abs(di)+1):
                cheat_i, cheat_j = i + di, j + dj
                if 0 <= cheat_i < self.n and 0 <= cheat_j < self.m and type(self.grid[cheat_i][cheat_j]) == int:
                    # Going from (i,j) to (cheat_i, cheat_j) is possible withing max_step cheating steps.
                    # Compute the gain we would get when doing so (compared to follow the official track)
                    win = self.grid[cheat_i][cheat_j] - self.grid[i][j] - abs(di) - abs(dj)
                    win = max(0, win)
                    cheats[win] = cheats.get(win, 0) + 1
        return cheats

    def _star_1(self) -> int:
        """Solve puzzle 1

        :return:
        """
        self.read_input()
        self.find_shortest_path()

        # Check every grid cell if it could be a single (small) shortcut
        # Count the "win"
        counter = dict()
        for i in range(1, len(self.grid)-1):
            for j in range(1, len(self.grid[0])-1):
                x, y = self.check_cheat(i, j)
                counter[x] = counter.get(x, 0) + 1
                counter[y] = counter.get(y, 0) + 1

        #for k, v in sorted(counter.items()):
        #    print(f"{v} cheats save {k} picoseconds")

        # Sum up all shortcuts, which save at least 100 steps
        good_cheats = 0
        for saving, cheats in counter.items():
            if saving >= 100:
                good_cheats += cheats

        return good_cheats


    def _star_2(self) -> int:
        """Solve puzzle 2

        :return:
        """
        if not self.grid:
            self.read_input()
            self.find_shortest_path()

        def get_next_field(i, j) -> tuple:
            for ni, nj in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                if type(self.grid[ni][nj]) == int and self.grid[ni][nj] > self.grid[i][j]:
                    return ni, nj
            return None

        # Follow along the track and figure out for each field, which cheating possibility it has.
        cheats = dict()
        pos = self.start
        while pos:
            i, j = pos
            cheats = self.get_all_cheats(i, j, cheats)

            pos = get_next_field(i, j)

        #for k, v in sorted(cheats.items()):
        #    print(f"{v} cheats save {k} picoseconds")

        # Sum up the cheating possibilities which have at least saving of min_saving steps
        min_saving = 50 if self.is_example else 100
        good_cheats = 0
        for saving, cheats in cheats.items():
            if saving >= min_saving:
                good_cheats += cheats

        return good_cheats


# ZKB-Ranking
# Star 1: 12
# Star 2: 8