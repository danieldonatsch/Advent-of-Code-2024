import os.path
import time


class BaseSolution:

    def __init__(self, day_num: int, example=False, verbose=False):
        self.solution_day = day_num
        self.is_example = example
        self.verbose = verbose
        if self.verbose:
            print(f"{self.__class__.__name__} initialized")

    def get_input_file_path(self, star=1):
        if star == 2 and self.is_example:
            # Check, if there is a special example for star 2
            if os.path.exists(f"input/day{self.solution_day:02d}_example2.txt"):
                return f"input/day{self.solution_day:02d}_example2.txt"

        return f"input/day{self.solution_day:02d}_example.txt" if self.is_example \
            else f"input/day{self.solution_day:02d}.txt"

    def star_1(self):
        start_time = time.time()
        print(f"*  Collect first star on December {self.solution_day}, 2025...")

        res = self._star_1()
        print(f"*  The solution is:\n*  \t > {repr(res)} <")

        print("*  Run time:", time.time()-start_time, "seconds")

    def star_2(self):
        start_time = time.time()
        print(f"** Collect second star on December {self.solution_day}, 2025...")

        res = self._star_2()
        print(f"** The solution is:\n** \t > {repr(res)} <")

        print("** Run time:", time.time()-start_time, "seconds")

    def _star_1(self):
        print("Needs to be implemented on each day!")

    def _star_2(self):
        print("Needs to be implemented on each day!")
