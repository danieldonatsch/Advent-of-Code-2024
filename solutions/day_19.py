import collections

from . import base_solution as bs


class SolutionDay19(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.trie = dict()

    def build_try(self, words):
        """Builds a trie form the given list of words

        :param words: (list) list of words
        :return:
        """
        for word in words:
            curr = self.trie
            for char in word:
                if not char in curr:
                    curr[char] = dict()
                curr = curr[char]

    def find_possible_words(self, string, start_idx) -> list:
        """Computes all positions within the string which can be reached from start_index with the given set of words.

        :param string: (str) string to be searched/built
        :param start_idx: (int) start index
        :return: (list) list of possible end indices
        """
        i = start_idx
        char = string[start_idx]
        curr = self.trie
        out = []
        while char in curr:
            i += 1
            curr = curr[char]
            if ',' in curr:
                out.append(i)
            if i < len(string):
                char = string[i]
            else:
                break

        return out

    def can_build_string(self, string) -> bool:
        """Figures out, if we can build the input string with the given set of words.

        We keep a list reachable, which has the same length as the input string and stores booleans.
        We compute for each reachable position all (forward) positions, which we can reach with the given set of words.
        That way, we go through the whole string/list. If we and with a True value on the last entry,
        we can reach the end and therefore the string can be built with the given set of words.

        :param string:
        :return:
        """
        n = len(string)
        # Do a breadth first search
        reachable = [False] * (n+1)
        reachable[0] = True
        for i in range(n):
            if not reachable[i]:
                continue
            ends = self.find_possible_words(string, i)
            for j in ends:
                reachable[j] = True

        return reachable[n]

    def count_ways_to_build_string(self, string) -> int:
        """Counts all possible ways to build the string with the given words.

        It does the (almost) the same as can_build_string(),
        except that we count the ways we have to reach a specific position within the input-string.
        So, we replace the reachable list with a ways list, which stores integers instead of booleans.

        :param string: (str) String which needs to be built
        :return: (int) count of ways
        """
        n = len(string)
        # Do a breadth first search, similar to can build string.
        ways = [0] * (n+1)
        ways[0] = 1
        for i in range(n):
            if ways[i] == 0:
                continue
            ends = self.find_possible_words(string, i)
            for j in ends:
                # Add all the possibilities to go form i to j
                ways[j] += ways[i]

        return ways[n]

    def _star_1(self) -> int:
        """Solves puzzle part 1

        :return:
        """
        input_file_path = self.get_input_file_path()
        with open(input_file_path, 'r') as of:
            line = of.readline().strip()
            line += ','
            self.build_try(line.split())

            of.readline()   # Empty line
            count = 0
            while line := of.readline().strip():
                # Do a breadth first search
                if self.can_build_string(line):
                    count += 1

            return count


    def _star_2(self) -> int:
        """Solves puzzle part 2

        :return:
        """
        input_file_path = self.get_input_file_path()
        with open(input_file_path, 'r') as of:
            line = of.readline().strip()
            line += ','
            self.build_try(line.split())

            of.readline()   # Empty line
            count = 0
            while line := of.readline().strip():
                # Do a breadth first search
                count += self.count_ways_to_build_string(line)

            return count


# ZKB-Ranking:
# Star 1: 13
# Star 2: 10
