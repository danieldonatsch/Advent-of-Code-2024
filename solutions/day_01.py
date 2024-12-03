import collections

from . import base_solution as bs


class SolutionDay01(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)

    def fill_lists(self, list_1, list_2) -> None:
        """Reads input file and fills data into the two lists

        :param list_1:
        :param list_2:
        """
        input_file = self.get_input_file_path()
        with open(input_file, 'r') as of:
            while line := of.readline():
                l, r = line.strip().split('   ')
                list_1.append(int(l))
                list_2.append(int(r))

    def _star_1(self) -> int:
        """Read the file into two lists. Sort them, and compute the differences.
        This is done in O(n log n) time.

        :return: (int) difference between the two lists
        """
        list_1, list_2 = [], []
        self.fill_lists(list_1, list_2)

        diff = 0
        for item1, item2 in zip(sorted(list_1), sorted(list_2)):
            diff += abs(item1 - item2)
        return diff


    def _star_2(self):
        """Read the file into two lists.
        Count in second the appearance of each entry.
        Walk over first one and multiply each entry with the count from the second list

        :return: (int) similarity score
        """
        list_1, list_2 = [], []
        self.fill_lists(list_1, list_2)

        # Count the appearance in list 2:
        counter = collections.Counter(list_2)

        similarity_score = 0
        for item in list_1:
            similarity_score += item * counter.get(item, 0)

        return similarity_score
