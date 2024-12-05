from . import base_solution as bs

from functools import cmp_to_key


class SolutionDay05(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.later_pages = None
        self.unsorted_pages = []

    def compare(self, item1, item2):
        if item1 in self.later_pages and item2 in self.later_pages[item1]:
            return -1
        if item2 in self.later_pages and item1 in self.later_pages[item2]:
            return 1
        return 0

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
                n = len(pages)
                order_is_valid = True
                for i in range(n):
                    if pages[i] not in self.later_pages:
                        # Page i has no rule, can be anywhere
                        continue
                    for j in range(0, i):
                        if pages[j] in self.later_pages[pages[i]]:
                            order_is_valid = False
                            break
                    if not order_is_valid:
                        self.unsorted_pages.append(pages)
                        break
                if order_is_valid:
                    mid = n//2
                    sum_of_middle_pages += int(pages[mid])

        return sum_of_middle_pages

    def _star_2(self) -> None:
        """Fill in description and code...

        :return:
        """
        # Today, we need to run the two in consecutive order
        if self.later_pages is None:
            print("Please run star_1() first.")
            return

        sum_of_middle_pages = 0
        for pages in self.unsorted_pages:
            n = len(pages)
            #print("Unsorted pages:", pages)
            pages.sort(key=cmp_to_key(self.compare))
            #print("Sorted pages:", pages)
            mid = n // 2
            sum_of_middle_pages += int(pages[mid])
            #print('+', int(pages[mid]), '=', sum_of_middle_pages)

        # 4157 was too high
        return sum_of_middle_pages

