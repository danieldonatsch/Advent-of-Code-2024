from . import base_solution as bs


class SolutionDay04(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.grid = None

    def count_for_MAS(self, i, j) -> int:
        m, n = len(self.grid), len(self.grid[0])
        count = 0
        # Check all 8 directions...
        # Vertical
        if i >= 3:
            count += (self.grid[i-1][j] == 'M' and self.grid[i-2][j] == 'A' and self.grid[i-3][j] == 'S')
        if i < m-3:
            count += (self.grid[i+1][j] == 'M' and self.grid[i+2][j] == 'A' and self.grid[i+3][j] == 'S')
        # Horizontal
        if j >= 3:
            count += (self.grid[i][j-1] == 'M' and self.grid[i][j-2] == 'A' and self.grid[i][j-3] == 'S')
        if j < n-3:
            count += (self.grid[i][j+1] == 'M' and self.grid[i][j+2] == 'A' and self.grid[i][j+3] == 'S')
        # Diagonal
        if i >= 3 and j >= 3:
            count += (self.grid[i-1][j-1] == 'M' and self.grid[i-2][j-2] == 'A' and self.grid[i-3][j-3] == 'S')
        if i >= 3 and j < n-3:
            count += (self.grid[i-1][j+1] == 'M' and self.grid[i-2][j+2] == 'A' and self.grid[i-3][j+3] == 'S')
        if i < m-3 and j >= 3:
            count += (self.grid[i+1][j-1] == 'M' and self.grid[i+2][j-2] == 'A' and self.grid[i+3][j-3] == 'S')
        if i < m-3 and j < n-3:
            count += (self.grid[i+1][j+1] == 'M' and self.grid[i+2][j+2] == 'A' and self.grid[i+3][j+3] == 'S')
        # Return the count
        return count

    def check_diag_for_MaS(self, i, j, diag=1):
        if diag == 1:
            i1, j1 = i-1, j-1
            i2, j2 = i+1, j+1
        else:
            i1, j1 = i-1, j+1
            i2, j2 = i+1, j-1

        # Check for MaS
        if self.grid[i1][j1] == 'M' and self.grid[i2][j2] == 'S':
            return True
        # Check for SaM
        if self.grid[i1][j1] == 'S' and self.grid[i2][j2] == 'M':
            return True
        # Diag is not part of an X-MAS
        return False


    def _star_1(self) -> None:
        """Fill in description and code...

        :return:
        """
        input_file_path = self.get_input_file_path()

        count = 0
        with open(input_file_path, 'r') as of:
            self.grid = [line.strip() for line in of.readlines()]

            m, n = len(self.grid), len(self.grid[0])
            for i in range(n):
                for j in range(m):
                    if self.grid[i][j] == 'X':
                        count += self.count_for_MAS(i, j)

        return count



    def _star_2(self) -> None:
        """Fill in description and code...

        :return:
        """
        if self.grid is None:
            input_file_path = self.get_input_file_path()

            with open(input_file_path, 'r') as of:
                self.grid = [line.strip() for line in of.readlines()]

        count = 0
        m, n = len(self.grid), len(self.grid[0])
        for i in range(1, n-1):
            for j in range(1, m-1):
                if self.grid[i][j] == 'A':
                    count += int(self.check_diag_for_MaS(i, j, 1) and self.check_diag_for_MaS(i, j, 2))

        return count
