from . import base_solution as bs


class ChronospatialComputer:
    def __init__(self, a: int = None, b: int = None, c: int = None, instructions: list = []):
        self.registers = {'A': a, 'B': b, 'C': c}
        self.instruction_pointer = 0
        self.instructions = instructions
        self.computed_values = []

    def combo(self, operand: int) -> int:
        """The value of a combo operand can be found as follows:
        Combo operands 0 through 3 represent literal values 0 through 3.
        Combo operand 4 represents the value of register A.
        Combo operand 5 represents the value of register B.
        Combo operand 6 represents the value of register C.
        Combo operand 7 is reserved and will not appear in valid programs.

        :param operand:
        :return:
        """
        return {0: 0, 1: 1, 2: 2, 3: 3,
                4: self.registers['A'],
                5: self.registers['B'],
                6: self.registers['C'],
                7: None}[operand]

    def _dv(self, operand: int) -> int:
        """The _dv instruction performs division. The numerator is the value in the A register.
        The denominator is found by raising 2 to the power of the instruction's combo operand.
        (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)

        :param operand:
        :return:
        """
        numerator = self.registers['A']
        denominator = 2 ** self.combo(operand)
        return int(numerator / denominator)

    def adv(self, operand: int) -> None:
        """The adv instruction (opcode 0) performs division. The numerator is the value in the A register.
        The denominator is found by raising 2 to the power of the instruction's combo operand.
        (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
        The result of the division operation is truncated to an integer and then written to the A register.

        :param operand:
        :return:
        """
        #print(f"adv({operand}), {self.registers = }")
        self.registers['A'] = self._dv(operand)
        self.instruction_pointer += 2

    def bxl(self, operand: int) -> None:
        """The bxl instruction (opcode 1) calculates the bitwise XOR of register B
        and the instruction's literal operand, then stores the result in register B.

        :param operand:
        :return:
        """
        #print(f"bxl({operand}), {self.registers = }")
        self.registers['B'] = self.registers['B'] ^ operand
        self.instruction_pointer += 2

    def bst(self, operand: int) -> None:
        """The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
        (thereby keeping only its lowest 3 bits), then writes that value to the B register.

        :param operand:
        :return:
        """
        #print(f"bst({operand}), {self.registers = }")
        self.registers['B'] = self.combo(operand) % 8
        self.instruction_pointer += 2

    def jnz(self, operand: int) -> None:
        """The jnz instruction (opcode 3) does nothing if the A register is 0.
        If the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand;
        if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

        :param operand:
        :return:
        """
        #print(f"jnz({operand}), {self.registers = }")
        if self.registers['A'] == 0 or self.instruction_pointer == operand:
            self.instruction_pointer += 2
        else:
            self.instruction_pointer = operand

    def bxc(self, operand: int) -> None:
        """The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,
        then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

        :param operand:
        :return:
        """
        #print(f"bxc({operand}), {self.registers = }")
        self.registers['B'] = self.registers['B'] ^ self.registers['C']
        self.instruction_pointer += 2

    def out(self, operand: int) -> None:
        """The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value.
        (If a program outputs multiple values, they are separated by commas.)
        """
        #print(f"out({operand}), {self.registers = }")
        self.computed_values.append(str(self.combo(operand) % 8))
        self.instruction_pointer += 2

    def bdv(self, operand: int) -> None:
        """The bdv instruction (opcode 6) works exactly like the adv instruction
        except that the result is stored in the B register. (The numerator is still read from the A register.)

        :return:
        """
        #print(f"bdv({operand}), {self.registers = }")
        self.registers['B'] = self._dv(operand)
        self.instruction_pointer += 2

    def cdv(self, operand: int) -> None:
        """The cdv instruction (opcode 7) works exactly like the adv instruction
        except that the result is stored in the C register. (The numerator is still read from the A register.)
        """
        #print(f"cdv({operand}), {self.registers = }")
        self.registers['C'] = self._dv(operand)
        self.instruction_pointer += 2

    def run(self) -> str:

        opcodes = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }

        while self.instruction_pointer < len(self.instructions)-1:
            opcode = self.instructions[self.instruction_pointer]
            operator = self.instructions[self.instruction_pointer+1]
            opcodes[opcode](operator)

        return ','.join(self.computed_values)


class SolutionDay17(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.registers = {'A': None, 'B': None, 'C': None}
        self.instructions = []

    def read_input(self):
        input_file_path = self.get_input_file_path()
        with open(input_file_path, 'r') as of:
            self.registers['A'] = int(of.readline().split(':')[1].strip())
            self.registers['B'] = int(of.readline().split(':')[1].strip())
            self.registers['C'] = int(of.readline().split(':')[1].strip())
            of.readline()   # Empty line
            self.instructions = [int(instruction) for instruction in of.readline().split(':')[1].split(',')]

    def _star_1(self) -> str:
        """Fill in description and code...

        :return:
        """
        self.read_input()
        computer = ChronospatialComputer()
        computer.registers = self.registers
        computer.instructions = self.instructions
        return computer.run()

    def _star_2(self) -> int:
        """Fill in description and code...

        :return:
        """
        input_file_path = self.get_input_file_path()

# ZKB-Ranking
# Star 1, rank 16