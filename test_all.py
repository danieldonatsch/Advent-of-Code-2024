import time

import solutions
from run import get_advent_of_code_solution

from pydoc import locate

# Solution for samples.
# Dict key is the day, first solution for star 1, second for star 2
sample_solutions = {
    1: (11, 31),
    2: (2,4),
    3: (161, 48),
    4: (18, 9),
    5: (143, 123),
    6: (41, )
}

# Solution for samples.
# Dict key is the day, first solution for star 1, second for star 2
puzzle_solutions = {
    1: (2742123, 21328497),
    2: (479, 531),
    3: (183788984, 62098619),
    4: (2370, 1908),
    5: (7024, 4151),
    6: (5208,)
}


def run_all_tests(example=True) -> None:
    target_values = sample_solutions if example else puzzle_solutions

    for day, values in sorted(target_values.items()):
        solution = get_advent_of_code_solution(day=day, is_example=example)
        val = values[0]
        out = ''
        if val == solution._star_1():
            out += '*'
        else:
            out += 'x'
        if len(values) == 1:
            out += '-'
        else:
            val = values[1]
            if val == solution._star_2():
                out += '*'
            else:
                out += 'x'
        print(f"{day: 2d}", out)


if __name__ == '__main__':
    t0 = time.time()
    run_all_tests(example=True)

    print("\nRunning all Advent of Code 2024 puzzles took", round(time.time() - t0, 4), "seconds")
