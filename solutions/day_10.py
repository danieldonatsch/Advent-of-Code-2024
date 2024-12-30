from . import base_solution as bs


class SolutionDay10(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.map = None
        self.height = 0
        self.width = 0

    def build_map(self):
        self.map = []
        input_file_path = self.get_input_file_path()
        with open(input_file_path, 'r') as of:
            while line := of.readline().strip():
                self.map.append([int(x) for x in line])
        self.height = len(self.map)
        self.width = len(self.map[0])

    def find_peaks(self, positions, h) -> int:
        """Looks for all peaks that can be found from the current positions (breadth-first approach)

        :param positions: set of all
        :param h: (int) current height
        :return: score
        """
        if not positions:
            return 0

        if h == 9:
            return len(positions)

        next_positions = set()
        h = h+1
        for i, j in positions:
            # Look at all four neighbours:
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i+di, j+dj
                if 0 <= ni < self.height and 0 <= nj < self.width:
                    if self.map[ni][nj] == h:
                        # If the neighbour reaches the next level, add it
                        next_positions.add((ni, nj))

        return self.find_peaks(next_positions, h)

    def find_all_paths(self, path_counts, h) -> int:
        """Counts all path to the current positions.

        :param path_counts: dict with positions as key and all path leading to it as value
        :param h: (int) current height
        :return: score
        """
        if not path_counts:
            return 0

        if h == 9:
            return sum(path_counts.values())

        next_level = dict()
        h = h+1
        for (i, j), count in path_counts.items():
            # Look at all four neighbours:
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i+di, j+dj
                if 0 <= ni < self.height and 0 <= nj < self.width:
                    if self.map[ni][nj] == h:
                        # If the neighbour reaches the next level, add it
                        next_level[(ni, nj)] = count + next_level.get((ni, nj), 0)

        return self.find_all_paths(next_level, h)

    def _star_1(self) -> None:
        """Fill in description and code...

        :return:
        """
        self.build_map()

        total_score = 0
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 0:
                    # Trail head found, follow its path
                    score = self.find_peaks([(i, j)], 0)
                    total_score += score

        return total_score

    def _star_2(self) -> None:
        """Fill in description and code...

        :return:
        """
        if self.map is None:
            self.build_map()

        path_count = 0
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 0:
                    # Trail head found, follow its path
                    count = self.find_all_paths({(i, j): 1}, 0)
                    path_count += count

        return path_count


# ZKB Points:
# star 1: 917 -> 985 (68)
# star 1: 985 -> 1053 (68)
