from . import base_solution as bs


class SolutionDay15(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.grid = None
        self.directions = None
        self.robot_pos = None

    def print_grid(self):
        # Mark robot
        if self.robot_pos:
            self.grid[self.robot_pos[0]][self.robot_pos[1]] = '@'
        # Print grid
        for row in self.grid:
            print(''.join(row))
        # Remove robot mark
        if self.robot_pos:
            self.grid[self.robot_pos[0]][self.robot_pos[1]] = '.'

    def read_input(self, double_grid=False) -> None:
        """Reads the input file and sets the member variables

        :param double_grid: (bool) if the grid width is doubled or not (star2 needs it double width)
        :return: None
        """
        input_file_path = self.get_input_file_path()
        self.grid = []
        with open(input_file_path, 'r') as of:
            # First part of the file is the starting grid
            while line := of.readline().strip():
                self.grid.append(list(line))
                if (x := line.find('@')) > 0:
                    self.robot_pos = (len(self.grid)-1, x)

            if double_grid:
                # For the second question, the grid becomes twice as wide (but keeps its height)
                for i in range(len(self.grid)):
                    new_row = []
                    for item in self.grid[i]:
                        if item == 'O':
                            new_row.extend(['[', ']'])
                        else:
                            new_row.extend([item] * 2)
                    self.grid[i] = new_row
                self.robot_pos = (self.robot_pos[0], 2*self.robot_pos[1])

            #self.print_grid()
            #print(self.robot_pos)

            # Second part are the robot moves
            self.directions = []
            while line := of.readline().strip():
                self.directions += list(line)

    @staticmethod
    def get_new_coordinates(i, j, d) -> tuple[int, int]:
        if d == '^':
            return i-1, j
        if d == 'v':
            return i+1, j
        if d == '<':
            return i, j-1
        if d == '>':
            return i, j+1
        print("Unknown direction", d)
        return i, j

    def can_object_move(self, i, j, d) -> bool:
        """Computes, if an object (robot or box) can move to this coordinate.

        :param i: (int) vertical coordinate
        :param j: (int) vertical coordinate
        :param d: (int) direction in which we try to push the box, if there is one on (i, j)
        :return: True if the field is free or can be made free. False otherwise.
        """
        if self.grid[i][j] == '#':
            # Nope, we're on a wall
            return False
        if self.grid[i][j] == '.':
            # Yes, we're on a free space!
            return True

        # Unclear, we're on a box. Let's see, if we can move the box!
        ni, nj = self.get_new_coordinates(i, j, d)
        if self.can_object_move(ni, nj, d):
            # The box can be moved. Move it to the new position ni, nj and make i, j free.
            self.grid[ni][nj] = self.grid[i][j]
            self.grid[i][j] = '.'
            return True
        else:
            # No, the box can't be moved. So, nothing can be moved to here.
            return False

    def can_objects_move_vertical(self, i: int, j_pos: set, di: int) -> bool:
        """Checks if the fields j_pos are free or if it has boxes, if they can be moved to row+di

        :param i: (int) row coordinate
        :param j_pos: (set) column coordinates of the fields we should check
        :param di: (int) direction in which we try to push boxes which are on the fields
        :return: (bool) True if all fields can be made free, false otherwise
        """
        # Check each object:
        need_to_check = set()
        for j in j_pos:
            if self.grid[i][j] == '#':
                return False    # We hit the wall
            if self.grid[i][j] == '[':
                # Need more investigation for this and its neighbor!
                need_to_check.add(j)
                need_to_check.add(j+1)
            elif self.grid[i][j] == ']':
                # Need more investigation for this and its neighbor!
                need_to_check.add(j)
                need_to_check.add(j-1)

        if not need_to_check:
            # Everything is well, nothing more to check
            return True

        # More to check, go to next level:
        if self.can_objects_move_vertical(i+di, need_to_check, di):
            objects_to_move = j_pos.union(need_to_check)
            # We can move the objects, so we do move the objects!
            for j in need_to_check:
                self.grid[i+di][j] = self.grid[i][j]
                self.grid[i][j] = '.'
            # After moving all, we return True
            return True
        else:
            # We can't move the objects, so:
            return False


    def get_gps_sum(self, box_tye='O') -> int:
        """Looks for all boxes in the grid and compute its gps location (100*i, j) and sums all of it

        :param box_tye: (str) the character which defines the box, either 'O' or '['
        :return: (int) sum of coordinates
        """
        # Finally, compute the GPS locations and its sum
        gps_sum = 0
        m, n = len(self.grid), len(self.grid[0])
        for i in range(1, m - 1):
            for j in range(1, n - 1):
                if self.grid[i][j] == box_tye:
                    gps_sum += (100 * i) + j

        return gps_sum

    def _star_1(self) -> int:
        """Fill in description and code...

        :return:
        """
        self.read_input()

        i, j = self.robot_pos
        # Mark position as empty
        self.grid[i][j] = '.'
        for d in self.directions:
            # Compute the preferred new robot position
            ni, nj = self.get_new_coordinates(i, j, d)
            # Check if the robot can be placed here
            if self.can_object_move(ni, nj, d):
                i, j = ni, nj

        #self.print_grid()
        return self.get_gps_sum(box_tye='O')


    def _star_2(self) -> int:
        """Fill in description and code...

        :return:
        """
        self.read_input(double_grid=True)

        i, j = self.robot_pos
        # Mark position as empty
        self.grid[i][j] = '.'
        self.grid[i][j+1] = '.'
        for d in self.directions:
            # Compute the preferred new robot position
            ni, nj = self.get_new_coordinates(i, j, d)
            di, dj = ni-i, nj-j
            # Check if the robot can be placed here
            if di == 0:
                # Horizontal works as before
                if self.can_object_move(ni, nj, d):
                    j = nj
            else:
                if self.can_objects_move_vertical(ni, {nj}, di):
                    i = ni

        #print("Final grid:")
        #self.robot_pos = (i, j)
        #self.print_grid()

        return self.get_gps_sum(box_tye='[')


# ZKB-Ranking:
# Star 1: 21 who reaches it before me
# Star 2: 19 who reached it before me
