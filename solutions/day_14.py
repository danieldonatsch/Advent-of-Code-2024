from collections import defaultdict

from . import base_solution as bs


class SolutionDay14(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.w = 11 if self.is_example else 101
        self.h = 7 if self.is_example else 103
        self.robots = []
        self.robot_pos = []

    def print_grid(self, marks=None, out_file=None) -> None:
        if out_file:
            of = open(out_file, 'w')

        for i in range(self.h):
            out = ['.'] * self.w
            for j in self.robot_pos[i]:
                out[j] = '1' if out[j] == '.' else str(int(out[j]) + 1)
            if marks and i in marks:
                out.append('M')
            else:
                out.append(' ')
            out.append(str(i))
            print(''.join(out))
            if out_file:
                of.write(''.join(out))
                of.write('\n')

        if out_file:
            of.close()

    def read_input(self):
        self.robots = []
        input_file_path = self.get_input_file_path()
        with open(input_file_path, 'r') as of:
            while line := of.readline().strip():
                p, v = line.split(' ')
                p = (p.split('=')[1]).split(',')
                v = (v.split('=')[1]).split(',')
                self.robots.append({'p': (int(p[0]), int(p[1])),
                                    'v': (int(v[0]), int(v[1]))})

    def move_robot(self, p, v, steps) -> tuple[int, int]:
        x = p[0] + steps * v[0]
        y = p[1] + steps * v[1]
        x = x % self.w
        y = y % self.h
        return x, y

    def _star_1(self) -> int:
        """Fill in description and code...

        :return:
        """
        steps = 100

        self.read_input()
        mx, my = int(self.w//2), int(self.h//2)

        self.robot_pos = defaultdict(list)
        quadrants = [[0, 0], [0, 0]]

        for robot in self.robots:
            # Compute the move
            x, y = self.move_robot(robot['p'], robot['v'], steps)
            self.robot_pos[y].append(x)

            if x == mx or y == my:
                continue

            qx = 0 if x < mx else 1
            qy = 0 if y < my else 1

            quadrants[qy][qx] += 1

        return quadrants[0][0] * quadrants[0][1] * quadrants[1][0] * quadrants[1][1]



    def _star_2(self) -> int:
        """Fill in description and code...

        :return:
        """
        self.read_input()

        n_robots = len(self.robots)

        steps = 0
        while True:
            self.robot_pos = defaultdict(list)
            for robot in self.robots:
                # Compute the move
                x, y = self.move_robot(robot['p'], robot['v'], steps)
                self.robot_pos[y].append(x)

            # Look for the two rows with the most robots (assuming there will be a bounding box!)
            row1, row2, mx1, mx2 = 0, 0, 0, 0
            for row, robots in self.robot_pos.items():
                if len(robots) > mx1:
                    # row 1 becomes second largest
                    row2, mx2 = row1, mx1
                    row1 = row
                    mx1 = len(robots)
                    continue
                if len(robots) > mx2:
                    row2 = row
                    mx2 = len(robots)

            self.robot_pos[row2].sort()
            l, r = 0, len(self.robot_pos[row2]) - 1
            l_not_found, r_not_found = True, True
            while l < r and l_not_found and r_not_found:
                if l_not_found and self.robot_pos[row2][l] not in self.robot_pos[row1]:
                    l += 1
                else:
                    l_not_found = False
                if r_not_found and self.robot_pos[row2][r] not in self.robot_pos[row1]:
                    r -= 1
                else:
                    r_not_found = False

            if l_not_found or r_not_found:
                steps += 1
                continue

            l_pos, r_pos = self.robot_pos[row2][l], self.robot_pos[row2][r]

            if row2 < row1:
                row1, row2 = row2, row1
            # Build a triangle and see, how many of the "higher" rows supports it!
            support_row_indices = set()
            support_robots = 0
            for row, robots in self.robot_pos.items():
                # Check how many robots are in the bounding box
                if row1 <= row <= row2:
                    support_row_indices.add(row)
                    for pos in robots:
                        if l_pos <= pos <= r_pos:
                            support_robots += 1

            if support_robots >= 0.7 * n_robots:
                print(steps)
                self.print_grid(support_row_indices, out_file=f"output/{steps}.txt")

                ans = input("Press 'c' to continue. Or 's' to stopp  ")

                if ans.strip().lower() == 's':
                    return steps

            steps += 1

            if steps > 103 * 101:
                print("No Christmas Tree found")
                return -1

        return -1



# ZKB-Points
# 1585(?) -> 1653 (20 have been faster)
# 1653 -> 1714 (20 have been faster)
