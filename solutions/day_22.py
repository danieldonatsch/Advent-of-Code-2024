import collections

from . import base_solution as bs


class Buyer:
    def __init__(self, secret_number):
        self.sec_num = secret_number
        self.price = secret_number % 10
        self.diffs = collections.deque()
        self.best_prices = dict()

    def _mix(self, value: int):
        """To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number.
        Then, the secret number becomes the result of that operation.
        """
        self.sec_num = value ^ self.sec_num

    def _prune(self):
        """To prune the secret number, calculate the value of the secret number modulo 16777216.
        Then, the secret number becomes the result of that operation.
        """
        self.sec_num = self.sec_num % 16777216

    def calc_step_1(self):
        """Calculate the result of multiplying the secret number by 64.
        Then, mix this result into the secret number.
        Finally, prune the secret number.
        """
        result = self.sec_num * 64
        self._mix(result)
        self._prune()

    def calc_step_2(self):
        """Calculate the result of dividing the secret number by 32.
        Round the result down to the nearest integer.
        Then, mix this result into the secret number.
        Finally, prune the secret number.
        """
        result = int(self.sec_num // 32)
        self._mix(result)
        self._prune()

    def calc_step_3(self):
        """Calculate the result of multiplying the secret number by 2048.
        Then, mix this result into the secret number.
        Finally, prune the secret number.
        """
        result = self.sec_num * 2048
        self._mix(result)
        self._prune()

    def get_next_secret_number(self):
        """Computes the next secret number and returns it.

        :return: (int) secret number
        """
        self.calc_step_1()
        self.calc_step_2()
        self.calc_step_3()
        # See, if we have a new "best price"
        new_price = self.sec_num % 10
        self.diffs.append(new_price - self.price)
        # If we have already for differences...
        if len(self.diffs) == 4:
            # Make them into a tuple
            diffs = tuple(self.diffs)
            # Check, if we have seen this difference pattern before. If not, add it with the current price
            if diffs not in self.best_prices:
                self.best_prices[diffs] = new_price
            # Pop the oldest price
            self.diffs.popleft()
        # Make the new price the current price
        self.price = new_price
        # Return the secret number
        return self.sec_num


class SolutionDay22(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.best_prices = dict()

    def _star_1(self) -> int:
        """Solve puzzle 1

        :return:
        """
        input_file_path = self.get_input_file_path()

        add_secret_nums = 0
        with open(input_file_path, 'r') as of:
            while line := of.readline():
                buyer = Buyer(int(line))
                for _ in range(1999):
                    buyer.get_next_secret_number()
                add_secret_nums += buyer.get_next_secret_number()
                # Now we can also earn start 2 in the same function. :-)
                for pattern, price in buyer.best_prices.items():
                    self.best_prices[pattern] = self.best_prices.get(pattern, 0) + price

        return add_secret_nums

    def _star_2(self) -> int:
        """Solve puzzle 2

        :return:
        """
        if not self.best_prices:
            self._star_1()

        # Look for the pattern with the best price!
        pattern, max_money = None, 0
        for k, v in self.best_prices.items():
            if v > max_money:
                pattern = k
                max_money = v

        return max_money



# ZKB-Ranking
# Star 1: 19
# Star 2: 17