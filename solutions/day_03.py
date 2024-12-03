import re

from . import base_solution as bs


def compute_mult(string) -> int:
    """Takes a string that looks like 'mul(2,4)' and computes the multiplication, e.g. 2 * 4 -> returns 8

    :param string: String of form mul(x,y)
    :return: (int) result of x*y
    """
    # Strip mul( and ) at the beginning and ending. Then split by the comma
    num1, num2 = string[4:-1].split(',')
    return int(num1) * int(num2)


class SolutionDay03(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)

    def _star_1(self) -> int:
        """Search for all multiplications, execute them and sum them

        :return:
        """
        input_file = self.get_input_file_path()
        total = 0
        with open(input_file, 'r') as of:
            while line := of.readline():
                multiplications = re.findall("mul\(\d+,\d+\)", line)
                for multiplication in multiplications:
                    total += compute_mult(multiplication)

        return total


    def _star_2(self) -> int:
        """Search for all multiplications, execute them and sum them if we have a do() seen last.
        After a don't() skip the multiplications

        :return:
        """
        input_file = self.get_input_file_path(star=2)
        res = 0
        do = True
        with open(input_file, 'r') as of:
            input_string = of.read()
            n = len(input_string)
            # We start with "do" and at pos 0
            do = True
            pos = 0
            # Compute for each of the three possibilities its first appearance
            mul = re.search("mul\(\d+,\d+\)", input_string[pos:])
            pos_mul = mul.span()[0]
            pos_do = input_string.find("do()", pos)
            pos_dont = input_string.find("don't()", pos)

            while pos < n:
                # What do we do next? The one with the smallest position
                if pos_mul < pos_do and pos_mul < pos_dont:
                    # Multiplication is next. Apply it and update the position
                    if do:
                        res += compute_mult(mul.group())
                    pos = pos_mul + 8   # mul(x,y) has at least length 8, we can skip that
                    mul = re.search("mul\(\d+,\d+\)", input_string[pos:])
                    # if mul is None, end of string is reached. Set it to n to keep the inequalities in the ifs valid
                    pos_mul = pos + mul.start() if mul else n
                elif pos_do < pos_mul and pos_do < pos_dont:
                    # do() is next. Apply it and update the positions
                    do = True
                    pos = pos_do + 4  # do() has 4 characters, skip these
                    pos_do = input_string.find("do()", pos)
                    # if pos_do is -1, end of string is reached. Set it to n to keep the inequalities in the ifs valid
                    pos_do = n if pos_do < 0 else pos_do
                elif pos_dont < pos_mul and pos_dont < pos_do:
                    # don't() is next. Apply it and update the positions
                    do = False
                    pos = pos_dont + 7  # don't() has 7 characters, skip these
                    pos_dont = input_string.find("don't()", pos)
                    # if pos_do is -1, end of string is reached. Set it to n to keep the inequalities in the ifs valid
                    pos_dont = n if pos_dont < 0 else pos_dont
                else:
                    if self.verbose:
                        print(f"{pos_mul=} {pos_do=} {pos_dont}")
                    break

        return res
