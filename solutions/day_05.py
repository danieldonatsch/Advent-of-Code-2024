from . import base_solution as bs

from functools import cmp_to_key
from collections import deque


class SolutionDay05(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.later_pages = None
        self.unsorted_pages = []
        self.return_zero = False

    def compare(self, item1, item2):
        """Comparison function to use the Pyton sort() or sorted(). But didn't work in all cases!

        In cases, where this function returns 0 (i.e. undefined pairs exist), the sort might not anymore be correct.

        :param item1:
        :param item2:
        :return: -1 if item1 before item2, 0 if relation undefined, 1 if item1 is after item2
        """
        if item1 in self.later_pages and item2 in self.later_pages[item1]:
            return -1
        if item2 in self.later_pages and item1 in self.later_pages[item2]:
            return 1

        self.return_zero = True
        return 0

    def sort_pages(self, pages) -> list:
        """Sorts unsorted pages based on the pair-wise orderings

        :param pages: list of unsorted pages
        :return: list with the sorted pages
        """
        count_right = []
        for p in pages:
            count = 0
            for x in pages:
                if x in self.later_pages[p]:
                    count += 1
            count_right.append((count, p))
        # Sort according to the number of "pages to the right".
        # The page, which has the most pages right of it, is the first one.
        count_right.sort(reverse=True)

        # Check, if we never had the same amount of "pages to the right". If so, make sure, these have the right order
        n = len(count_right)
        flipped = True
        while flipped:
            flipped = False
            for i in range(1, n):
                if (count_right[i-1][0] == count_right[i][0]) and \
                    (count_right[i-1][1] in self.later_pages[count_right[i][1]]):
                    # We need to flip this!
                    count_right[i-1], count_right[i] = count_right[i], count_right[i-1]
                    flipped = True

        return [page for (_, page) in count_right]

    def check_order(self, pages) -> bool:
        n = len(pages)
        order_is_valid = True
        for i in range(n):
            if pages[i] not in self.later_pages:
                # Page i has no rule, can be anywhere
                continue
            for j in range(0, i):
                if pages[j] in self.later_pages[pages[i]]:
                    order_is_valid = False
                    return False
        # No bug found...
        return True

    def _star_1(self) -> None:
        """Fill in description and code...

        :return:
        """
        input_file_path = self.get_input_file_path()

        sum_of_middle_pages = 0
        with open(input_file_path, 'r') as of:
            self.later_pages = dict()
            while line := of.readline():
                line = line.strip()
                if not line:
                    # Move to second part
                    break
                before, after = line.split("|")
                if before in self.later_pages:
                    self.later_pages[before].add(after)
                else:
                    self.later_pages[before] = {after}

            # Now we check the orderings.
            while line := of.readline():
                line = line.strip()
                pages = line.split(',')
                if self.check_order(pages):
                    mid = len(pages)//2
                    sum_of_middle_pages += int(pages[mid])
                else:
                    self.unsorted_pages.append(pages)

        return sum_of_middle_pages

    def _star_2(self) -> None:
        """Sorts the unsorted pages. Depends on _star_1()

        :return: Sum of middle page after sorting the unsorted ones.
        """
        # Today, we need to run the two in consecutive order
        if self.later_pages is None:
            print("Please run star_1() first.")
            return

        sum_of_middle_pages = 0
        i = 0
        for pages in self.unsorted_pages:
            pages = self.sort_pages(pages)
            mid = len(pages) // 2
            sum_of_middle_pages += int(pages[mid])

            '''
            self.return_zero = False
            pages.sort(key=cmp_to_key(self.compare))
            if self.return_zero:
                print(i, "Issue with sorting. Using mid:", m)
            mid = len(pages) // 2
            sum_of_middle_pages += int(pages[mid])
            '''
            i += 1

        return sum_of_middle_pages
