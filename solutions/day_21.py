from . import base_solution as bs


class SolutionDay21(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)

        # The paths from one directional keypad position to every other
        self.dir_pad_paths = dict()
        self.dir_pad_paths['A'] = {'A': [''], '^': ['<'], '>': ['v'], 'v': ['<v', 'v<'], '<': ['<v<', 'v<<']}
        self.dir_pad_paths['^'] = {'A': ['>'], '^': [''], '>': ['>v', 'v>'], 'v': ['v'], '<': ['v<']}
        self.dir_pad_paths['>'] = {'A': ['^'], '^': ['<^', '^<'], '>': [''], 'v': ['<'], '<': ['<<']}
        self.dir_pad_paths['v'] = {'A': ['^>', '>^'], '^': ['^'], '>': ['>'], 'v': [''], '<': ['<']}
        self.dir_pad_paths['<'] = {'A': ['>>^', '>^>'], '^': ['>^'], '>': ['>>'], 'v': ['>'], '<': ['']}

        # The shortest path lengths between two directional keypad positions:
        self.dir_pad_path_len = dict()
        self.dir_pad_path_len['A'] = {'A': 0, '^': 1, '>': 1, 'v': 2, '<': 3}
        self.dir_pad_path_len['^'] = {'A': 1, '^': 0, '>': 2, 'v': 1, '<': 2}
        self.dir_pad_path_len['>'] = {'A': 1, '^': 2, '>': 0, 'v': 1, '<': 2}
        self.dir_pad_path_len['v'] = {'A': 2, '^': 1, '>': 1, 'v': 0, '<': 1}
        self.dir_pad_path_len['<'] = {'A': 3, '^': 2, '>': 2, 'v': 1, '<': 0}

        # But we actually need the next-level path length, so a robot which "clicks" on the buttons of the robot...
        self.dir_pad2_path_len = self.compute_shortest_path_lengths(self.dir_pad_paths, self.dir_pad_path_len)
        # To get the full length, we need to add a button press. Each time the robot arm reaches the correct position,
        # we need to press once "A". Therefore, we need to extend each path with the number of buttons plus one:
        for start in self.dir_pad2_path_len.keys():
            for end in self.dir_pad2_path_len[start].keys():
                self.dir_pad2_path_len[start][end] += len(self.dir_pad_paths[start][end][0]) + 1

        # To earn the second star, we have to operate not just through two but 25 robots.
        # So, we compute the path length iteratively for 25 robots.
        self.dir_pad25_path_len = dict()
        for key, value in self.dir_pad2_path_len.items():
            self.dir_pad25_path_len[key] = value.copy()
        robot_count = 2
        while robot_count < 25:
            robot_count += 1
            self.dir_pad25_path_len = self.compute_shortest_path_lengths(self.dir_pad_paths, self.dir_pad25_path_len)

        # So, the same game with the numpad: First, we manually define all paths from lower to larger numbers.
        self.num_pad_paths = dict()
        self.num_pad_paths['A'] = {'A': [''],
                                   '0': ['<'],
                                   '1': ['^<<', '<^<'],
                                   '2': ['<^', '^<'],
                                   '3': ['^'],
                                   '4': ['^<<^', '^<^<', '^^<<', '<^<^', '<^^<'] ,
                                   '5': ['<^^', '^<^', '^^<'],
                                   '6': ['^^'],
                                   '7': ['^^<^<', '^^<<^', '^<^<^', '^<<^^', '^^^<<', '^<^^<', '<^<^^', '<^^^<', '<^^<^'],
                                   '8': ['<^^^', '^<^^', '^^<^', '^^^<'],
                                   '9': ['^^^']}
        self.num_pad_paths['0'] = {'0': [''],
                                   '1': ['^<'],
                                   '2': ['^'],
                                   '3': ['^>', '>^'],
                                   '4': ['^<^', '^^<'] ,
                                   '5': ['^^'],
                                   '6': ['^^>', '^>^', '>^^'],
                                   '7': ['^^^<', '^^<^', '^<^^'],
                                   '8': ['^^^'],
                                   '9': ['>^^^', '^>^^', '^^>^', '^^^>']}
        self.num_pad_paths['1'] = {'1': [''],
                                   '2': ['>'],
                                   '3': ['>>'],
                                   '4': ['^'] ,
                                   '5': ['^>', '>^'],
                                   '6': ['^>>', '>^>', '>>^'],
                                   '7': ['^^'],
                                   '8': ['^^>', '^>^', '>^^'],
                                   '9': ['>>^^', '>^>^', '>^^>', '^>>^', '^>^>', '^^>>']}
        self.num_pad_paths['2'] = {'2': [''],
                                   '3': ['>'],
                                   '4': ['<^', '^<'] ,
                                   '5': ['^'],
                                   '6': ['^>', '>^'],
                                   '7': ['^^<', '^<^', '<^^'],
                                   '8': ['^^'],
                                   '9': ['>^^', '^>^', '^^>']}
        self.num_pad_paths['3'] = {'3': [''],
                                   '4': ['<<^', '<^<', '^<<'],
                                   '5': ['<^', '^<'],
                                   '6': ['^'],
                                   '7': ['^<^<', '^<<^', '<^<^', '<<^^', '^^<<', '<^^<'],
                                   '8': ['<^^', '^<^', '^^<'],
                                   '9': ['^^']}
        self.num_pad_paths['4'] = {'4': [''] ,
                                   '5': ['>'],
                                   '6': ['>>'],
                                   '7': ['^'],
                                   '8': ['^>', '>^'],
                                   '9': ['>>^', '>^>', '^>>']}
        self.num_pad_paths['5'] = {'5': [''],
                                   '6': ['>'],
                                   '7': ['^<', '<^'],
                                   '8': ['^'],
                                   '9': ['>^', '^>']}
        self.num_pad_paths['6'] = {'6': [''],
                                   '7': ['<^<', '<<^', '^<<'],
                                   '8': ['<^', '^<'],
                                   '9': ['^']}
        self.num_pad_paths['7'] = {'7': [''],
                                   '8': ['>'],
                                   '9': ['>>']}
        self.num_pad_paths['8'] = {'8': [''],
                                   '9': ['>']}
        self.num_pad_paths['9'] = {'9': ['']}

        def change_direction(path) -> str:
            swaps = {'<': '>', '>': '<', '^': 'v', 'v': '^'}
            return ''.join([swaps[char] for char in path[::-1]])

        # Then, compute the backwards path (larger to smaller numbers) by reversing the forward paths
        for start in self.num_pad_paths.keys():
            for end in self.num_pad_paths[start].keys():
                if start not in self.num_pad_paths[end]:
                    self.num_pad_paths[end][start] = [change_direction(x) for x in self.num_pad_paths[start][end]]

        # Finally, we can compute the shortest path between any two numpad keys
        self.num_pad_path_len = self.compute_shortest_path_lengths(self.num_pad_paths, self.dir_pad2_path_len)


    @staticmethod
    def compute_shortest_path_lengths(pad_paths, step_lengths):
        # Finally, we can compute the shortest path between any two numpad keys
        pad_path_len = dict()
        # Compute dir_pad_paths:
        for start in pad_paths.keys():
            pad_path_len[start] = dict()
            for end in pad_paths[start].keys():
                path_len = []
                for path in pad_paths[start][end]:
                    path = 'A' + path + 'A'
                    path_len.append(0)
                    # Compute the pad path length by...
                    for i in range(1, len(path)):
                        x, y = path[i - 1], path[i]
                        # summing up all position changes from x to y.
                        path_len[-1] += step_lengths[x][y]

                pad_path_len[start][end] = min(path_len)

        return pad_path_len

    def _test(self):
        """Some tests used to develop the super-complicated pre-processing in the _init_() function...

        :return:
        """
        bla = 'Av<<A>>^A<A>AvA<^AA>A<vAAA>^A'
        total_length = 0
        for i in range(1, len(bla)):
            x, y = bla[i-1], bla[i]
            # Compute the dir_pad_path_len from the previous position x to the current position y. Plus pressing the button
            total_length += self.dir_pad_path_len[x][y] + 1
        assert total_length == len('<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'), \
            "dir_pad_path_len test failed"

        bla = 'A<A^A>^^AvvvA'
        total_length = 0
        for i in range(1, len(bla)):
            x, y = bla[i-1], bla[i]
            # Compute the dir_pad_path_len from the previous position x to the current position y.
            total_length += self.dir_pad2_path_len[x][y]

        assert total_length == len('<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'), \
            "dir_pad2_path_len test failed"

        bla = 'A029A'
        total_length = 0
        for i in range(1, len(bla)):
            x, y = bla[i - 1], bla[i]
            # Compute the dir_pad_path_len from the previous position x to the current position y.
            total_length += self.num_pad_path_len[x][y]

        assert total_length == len('<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'), \
            "num_pad_path_len test failed"

        total_length = self.compute_path_length('029A')

        assert total_length == len('<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'), \
            "compute_shortest_path() test failed"

        print("Test completed successful")

    def compute_path_length(self, num_input):
        path = 'A' + num_input
        total_length = 0
        for i in range(1, len(path)):
            x, y = path[i - 1], path[i]
            # Compute the path length from the previous position x to the current position y.
            total_length += self.num_pad_path_len[x][y]

        return total_length

    def _star_1(self) -> int:
        """Solve puzzle 1

        :return:
        """
        #self._test()

        input_file_path = self.get_input_file_path()
        complexity_sum = 0
        with open(input_file_path, 'r') as of:
            while line := of.readline().strip():
                length = self.compute_path_length(line)
                complexity = int(line[:3]) * length
                complexity_sum += complexity

        return complexity_sum

    def _star_2(self) -> int:
        """Solve puzzle 2

        :return:
        """
        # Finally, we can compute the shortest path between any two numpad keys
        self.num_pad_path_len = self.compute_shortest_path_lengths(self.num_pad_paths, self.dir_pad25_path_len)

        input_file_path = self.get_input_file_path()
        complexity_sum = 0
        with open(input_file_path, 'r') as of:
            while line := of.readline().strip():
                length = self.compute_path_length(line)
                complexity = int(line[:3]) * length
                complexity_sum += complexity

        return complexity_sum

# ZKB-Ranking
# Star 1: 17.
# Star 2: 17.