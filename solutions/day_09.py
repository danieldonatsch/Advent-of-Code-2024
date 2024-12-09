from . import base_solution as bs


class SolutionDay09(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)

    def _star_1(self) -> None:
        """Moves the memory bit by bit in front and fill empty spaces

        :return:
        """
        input_file_path = self.get_input_file_path()
        with open(input_file_path, 'r') as of:
            line = of.readline().strip()

        if not line:
            print(f"{self.__class__.__name__}._star_1(): File Reading failed")
            return

        memory = []
        for i in range(0, len(line), 2):
            file_id = i // 2
            file_len = int(line[i])
            space_len = int(line[i+1]) if i+1 < len(line) else 0
            memory += file_len * [file_id] + space_len * [None]

        l, r = 0, len(memory)-1
        while l < r:
            if memory[l] is not None:
                l += 1
            elif memory[r] is None:
                r -= 1
            else:
                # Left is None, right is not None. So, we move the value from left to right
                memory[l] = memory[r]
                memory[r] = None
                # Move both pointers
                l += 1
                r -= 1

        check_sum = 0
        # Compute check-sum
        for pos in range(len(memory)):
            file_id = memory[pos]
            if file_id is None:
                break
            check_sum += pos * file_id

        return check_sum

    def _star_2(self) -> None:
        """Moves the memory block-wise from back to front (if possible)

        :return:
        """
        input_file_path = self.get_input_file_path()
        with open(input_file_path, 'r') as of:
            line = of.readline().strip()

        if not line:
            print(f"{self.__class__.__name__}._star_1(): File Reading failed")
            return

        used_memory = []
        empty_memory = []
        mem_pos = 0
        for i in range(0, len(line), 2):
            file_id = i // 2
            file_len = int(line[i])
            # Add to used memory
            used_memory.append([mem_pos, file_len, file_id])
            # Move position in memory
            mem_pos += file_len
            # Add empty space, if there is some:
            space_len = int(line[i + 1]) if i + 1 < len(line) else 0
            empty_memory.append([mem_pos, space_len])
            mem_pos += space_len

        # Now we try to move the last memory as much in front as possible
        # Two nested for loops is quadratic, but it seems to be sufficient fast.
        for i in range(len(used_memory)-1, -1, -1):
            j = 0
            while j < len(empty_memory):
                if used_memory[i][0] < empty_memory[j][0]:
                    # The empty space we look at is behind the used memory. Stop searching!
                    break
                if used_memory[i][1] <= empty_memory[j][1]:
                    orig_mem_pos, orig_mem_size, _ = used_memory[i]
                    # We can move the memory to this empty space
                    used_memory[i][0] = empty_memory[j][0]
                    # Shrink the empty space
                    empty_memory[j][1] -= used_memory[i][1]
                    # And move it accordingly
                    empty_memory[j][0] += used_memory[i][1]
                    # Add the newly emptied memory to the empty memory set
                    # The memory just before the moved one, so this is i-1, can be extended
                    empty_memory[i-1][1] += orig_mem_size
                    if i < len(empty_memory):
                        # Further, also the following memory space can be concatenated!
                        empty_memory[i-1][1] += empty_memory[i][1]
                        del empty_memory[i]
                    # This memory can't be moved again.
                    break
                j += 1

        # Compute the check-sum
        check_sum = 0
        for mem_pos, file_len, file_id  in used_memory:
            for i in range(file_len):
                check_sum += (mem_pos + i) * file_id

        return check_sum


# ZKB-Points: 791 -> 855 -> 917
# 64pts, 62 pts (out of 83 points)
