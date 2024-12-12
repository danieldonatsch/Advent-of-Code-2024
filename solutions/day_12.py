from collections import defaultdict

from . import base_solution as bs


class SolutionDay12(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.grid = None
        self.m = -1
        self.n = -1

    def build_grid(self):
        input_file_path = self.get_input_file_path()

        self.grid = []
        with open(input_file_path, 'r') as of:
            i = 0
            while line := of.readline():
                line = line.strip()
                self.grid.append(list(line))
                i += 1

        self.m, self.n = len(self.grid), len(self.grid[0])

    def get_connected_area(self, i: int, j: int, exp_val) -> list:
        """Searches neighbours recursively to find a connected area, i.e. neighboring grid cells with the expected value.

        :param i: (int) vertical grid position
        :param j: (int) horizontal grid position
        :param exp_val: expected grid value
        :return: list of tuples with grid positions belonging to the connected area
        """
        if not (0 <= i < self.m and 0 <= j < self.n) or self.grid[i][j] != exp_val:
            # Out of grid or on a different value
            return []
        # Mark this cell as visited
        self.grid[i][j] = '#'
        connected_area = [(i, j)]
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            connected_area += self.get_connected_area(i+di, j+dj, exp_val)
        return connected_area

    def compute_area_x_perimeter(self, i, j) -> int:
        """Computes connected area and its perimeter and returns the multiplication of the two values.

        Grid area: number of connected cells:
        Perimeter: number of edges (cell sides).
        Example:
                  A
                 AAAA
        Area: 5
        Perimeter: 12

        :param i: (int) vertical grid position
        :param j: (int) horizontal grid position
        :return: area * perimeter (int)
        """
        connected_area = self.get_connected_area(i, j, self.grid[i][j])
        area = len(connected_area)
        connected_area = set(connected_area)

        perimeter = 0
        # Check all neighbours
        for i, j in connected_area:
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if (i+di, j+dj) not in connected_area:
                    perimeter += 1
        # Compute the fence
        return area * perimeter

    def compute_area_x_sides(self, i, j) -> tuple[int, int]:
        """Computes connected area and its sides and returns the multiplication of the two values.

        Grid area: number of connected cells:
        Sides: as one side count all cell edges which are neighbours and in-line.
        Example:
                  A
                 AAAA
        Area: 5
        Sides: 8

        :param i: (int) vertical grid position
        :param j: (int) horizontal grid position
        :return: area * perimeter (int)
        """
        connected_area = self.get_connected_area(i, j, self.grid[i][j])
        area = len(connected_area)
        connected_area = set(connected_area)

        sides = defaultdict(list)
        # Check all neighbours
        for i, j in connected_area:
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if (i+di, j+dj) not in connected_area:
                    # Build a "side id" consisting ot fhe direction (vertical/horizontal)
                    # and the cell indices before and after it. Further, we keep store also it's "position"
                    # to (later) figure out, if the side is all connected or not.
                    if di == 0:
                        side = f"h-{j}-{j+dj}"      # horizontal edge
                        sides[side].append(i)
                    else:
                        side = f"v-{i}-{i+di}"      # Vertical edge
                        sides[side].append(j)

        # Count the sides
        side_count = 0
        for edges in sides.values():
            # Sort all cell edges which (potentially) belong to the same side
            edges.sort()
            n = len(edges)
            edges += [None]
            # Check if they are connected. If not, increase the count by 1.
            for l in range(n):
                if edges[l]+1 != edges[l+1]:
                    side_count += 1
        # Compute the fence
        return area * side_count

    def _star_1(self) -> None:
        """Fill in description and code...

        :return:
        """
        self.build_grid()

        total_fence = 0
        for i in range(self.m):
            for j in range(self.n):
                if self.grid[i][j] == '#':
                    continue
                total_fence += self.compute_area_x_perimeter(i, j)

        return total_fence

    def _star_2(self) -> None:
        """Fill in description and code...

        :return:
        """
        self.build_grid()

        total_fence = 0
        for i in range(self.m):
            for j in range(self.n):
                if self.grid[i][j] == '#':
                    continue
                total_fence += self.compute_area_x_sides(i, j)

        return total_fence


# ZKB-Points:
# 1270 -> 1341
# 1341 -> 1425
