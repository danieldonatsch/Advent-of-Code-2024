import time

from run import get_advent_of_code_solution


# Solution for samples.
# Dict key is the day, first solution for star 1, second for star 2
sample_solutions = {
    1: (11, 31),
    2: (2,4),
    3: (161, 48),
    4: (18, 9),
    5: (143, 123),
    6: (41, 6),
    7: (3749, 11387),
    8: (14, 34),
    9: (1928, 2858),
    10: (36, 81),
    11: (55312, 65601038650482),
    12: (1930, 1206),
    13: (480, 875318608908),
    14: (12,),
    15: (10092, 9021),
    16: (11048, 64),
    17: ('4,6,3,5,6,3,5,2,1,0', 117440),
    18: (22, (6, 1)),
    19: (6, 16),
    20: (0, 285),
    21: (126384, 154115708116294),
    22: (37327623, 24),
    23: (7, 'co,de,ka,ta'),
    24: (2024, 'cdj,dhm,gfm,mrb,qjd,z08,z16,z32'),
    25: (3, )
}

# Solution for samples.
# Dict key is the day, first solution for star 1, second for star 2
puzzle_solutions = {
    1: (2742123, 21328497),
    2: (479, 531),
    3: (183788984, 62098619),
    4: (2370, 1908),
    5: (7024, 4151),
    6: (5208, 1972),
    7: (1611660863222, 945341732469724),
    8: (369, 1169),
    9: (6307275788409, 6327174563252),
    10: (535, 1186),
    11: (212655, 253582809724830),
    12: (1533024, 910066),
    13: (28262, 101406661266314),
    14: (225521010, ), # (225521010, 7774),
    15: (1465152, 1511259),
    16: (99488, 516),
    17: ('2,7,2,5,1,2,7,3,7', 247839002892474),
    18: (340, (34, 32)),
    19: (369, 761826581538190),
    20: (1404, 1010981),
    21: (242484, 294209504640384),
    22: (12759339434, 1405),
    23: (1423, 'gt,ha,ir,jn,jq,kb,lr,lt,nl,oj,pp,qh,vy'),
    24: (55114892239566, 'cdj,dhm,gfm,mrb,qjd,z08,z16,z32'),
    25: (3508, )
}


def run_all_tests(example=True) -> None:
    target_values = sample_solutions if example else puzzle_solutions

    if example:
        print("Results with small examples")
    else:
        print("Real Input Results:")
    print("Day Stars")
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
        print(f"{day: 3d}", out)


if __name__ == '__main__':
    t0 = time.time()
    run_all_tests(example=True)

    print("\nRunning all Advent of Code 2024 puzzles took", round(time.time() - t0, 4), "seconds")
