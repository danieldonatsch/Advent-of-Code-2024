from . import base_solution as bs


class SolutionDay25(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.locks = set()
        self.keys = set()

    def read_input(self):
        input_file_path = self.get_input_file_path()

        count = 0
        with open(input_file_path, 'r') as of:
            while line := of.readline():
                is_key = False
                counter = [0] * 5
                for i in range(6):
                    if i == 0:
                        is_key = (line[0] == '.')
                    else:
                        for j in range(5):
                            counter[j] += int(line[j] == '#')

                    line = of.readline()
                if is_key:
                    self.keys.add(tuple(counter))
                else:
                    self.locks.add(tuple(counter))
                # Read the potentially empty line
                of.readline()
                count += 1

    def _star_1(self) -> int:
        """Solve puzzle 1

        :return:
        """
        self.read_input()

        # Do it stupid and straight forward
        pair_count = 0
        for lock in self.locks:
            for key in self.keys:
                matches = 1
                for i in range(5):
                    if lock[i] + key[i] > 5:
                        matches = 0
                        break
                pair_count += matches
        return pair_count

    def _star_2(self) -> int:
        """Solve puzzle 2

        :return:
        """
        input_file_path = self.get_input_file_path()

# ZKB-Ranking:
# Star 1: 18
# Star 2: