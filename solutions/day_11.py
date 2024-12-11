import collections
from functools import lru_cache

from . import base_solution as bs


class SolutionDay11(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)

    def _star_1(self) -> int:
        """Brute-force approach, works for 25 steps.

        :return: number of numbers after 25 step.
        """
        @lru_cache
        def track_splits(number: int, split: int) -> int:
            if split == 25:
                return 1
            if number == 0:
                return track_splits(1, split+1)
            if (l := len(num_str := str(number))) % 2 == 0:
                num1, num2 = num_str[:l//2], num_str[l//2:]
                return track_splits(int(num1), split+1) + track_splits(int(num2), split+1)
            return track_splits(2024 * number, split+1)


        input_file_path = self.get_input_file_path()
        with open(input_file_path, 'r') as of:
            numbers = [int(item) for item in of.read().strip().split()]
        count = 0
        for num in numbers:
            count += track_splits(num, 0)
        return count

    def _star_2(self) -> None:
        """More efficient approach,
        where we count the numbers in each step and group the same numbers together to save compute.

        :return: number of numbers after 75 steps
        """
        @lru_cache
        def compute_split(number) -> tuple:
            if number == 0:
                return 1, None
            if (l := len(num_str := str(number))) % 2 == 0:
                return int(num_str[:l//2]), int(num_str[l//2:])
            return 2024 * number, None

        input_file_path = self.get_input_file_path()
        with open(input_file_path, 'r') as of:
            # Count the appearance of every number
            counter = collections.Counter([int(item) for item in of.read().strip().split()])

        for i in range(75):
            new_counter = dict()
            for num, count in counter.items():
                # Do one step for num
                num1, num2 = compute_split(num)
                # Update the appearance for num1 and (if exists) num2.
                new_counter[num1] = new_counter.get(num1, 0) + count
                if num2 is not None:
                    new_counter[num2] = new_counter.get(num2, 0) + count
            # Make the next step the current one
            counter = new_counter

        # Sum up the counts of each number which appears in the list after 75 steps
        return sum(counter.values())


# ZKB Points:
# 1055 -> 1117 (62 points out of 83)
# 1117 -> 1220 (103 Pooints? Hm...)