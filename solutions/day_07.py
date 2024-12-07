from . import base_solution as bs





class SolutionDay07(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.num_ops = 2

    def dfs(self, res, nums) -> bool:
        if len(nums) == 1:
            return res == nums[0]

        # Try both operators
        n0, n1 = nums[0], nums[1]
        mult = n0 * n1
        if mult <= res and self.dfs(res, [mult] + nums[2:]):
            return True
        add = n0 + n1
        if add <= res and self.dfs(res, [add] + nums[2:]):
            return True
        if self.num_ops == 3:
            # If a third operator is allowed, use also concatenation
            con = int(str(n0) + str(n1))
            if con <= res and self.dfs(res, [con] + nums[2:]):
                return True

        return False


    def solve_puzzle(self):
        input_file_path = self.get_input_file_path()

        possible_true_equation_counter = 0
        with open(input_file_path, 'r') as of:
            while line := of.readline().strip():
                result, numbers = line.split(':')
                result = int(result)
                numbers = [int(num) for num in numbers.split()]
                if self.dfs(result, numbers):
                    possible_true_equation_counter += result

        return possible_true_equation_counter


    def _star_1(self) -> None:
        """Fill in description and code...

        :return:
        """
        self.num_ops = 2
        return self.solve_puzzle()


    def _star_2(self) -> None:
        """Fill in description and code...

        :return:
        """
        self.num_ops = 3
        return self.solve_puzzle()


# ZKB-points:
# Initially: 506
# With star1: 579 (worth 73)
# With star2: 652 (worth 73)