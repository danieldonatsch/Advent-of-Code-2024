#import solutions
from pydoc import locate


def get_advent_of_code_solution(day: int, is_example, verbose=False):
    """Gets the object which computes the solution on that specific day

    :param day: (int) 1 to 25
    :param is_example: (bool) True if the example data (with known solution) should be used, False otherwise
    :return: solution class
    """
    solution_class = locate(f"solutions.day_{day:02d}.SolutionDay{day:02d}")
    return solution_class(day, is_example, verbose)


def main(day: int, is_example=False) -> None:
    """Runs the solution for the given day, either with the example input or the "real" one

    :param day: (int) 1 to 25
    :param is_example: bool
    :return: None
    """

    solution = get_advent_of_code_solution(day=day, is_example=is_example, verbose=True)
    print(" ")
    solution.star_1()
    print(" ")
    solution.star_2()


if __name__ == '__main__':
    print("Hello Advent of Code 2024!")
    main(
        day=3,
        is_example=True
    )
