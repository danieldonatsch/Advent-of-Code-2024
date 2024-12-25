import collections

from . import base_solution as bs


class SolutionDay24(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.nodes = None
        self.connections = collections.deque()

    def read_input(self):
        input_file_path = self.get_input_file_path()

        with open(input_file_path, 'r') as of:
            # Read the given values
            self.nodes = dict()
            while line := of.readline().strip():
                name, value = line.split(':')
                self.nodes[name] = int(value)

            # Next we read the connections
            while line := of.readline().strip():
                self.connections.append(tuple(line.split()))

    def decimal_from_nodes(self, first_letter='z'):
        # Go through node names in alphabetic order
        result, bit_count = 0, 0
        for node_name in sorted(self.nodes):
            # Wait, until it starts with z
            if node_name[0] == first_letter:
                # Add it to the result
                result += self.nodes[node_name] * (2 ** bit_count)
                bit_count += 1

        return result


    def _star_1(self) -> int:
        """Solve puzzle 1

        :return:
        """
        self.read_input()
        # We process all connections, until none is left
        while self.connections:
            connection = self.connections.popleft()
            x, op, y, _, t = connection
            if x in self.nodes and y in self.nodes:
                # Process it
                if 'AND' == op:
                    self.nodes[t] = self.nodes[x] and self.nodes[y]
                elif 'OR' == op:
                    self.nodes[t] = self.nodes[x] or self.nodes[y]
                elif 'XOR' == op:
                    self.nodes[t] = self.nodes[x] ^ self.nodes[y]
                else:
                    print(f"Operation '{op}' is unknown!")
            else:
                # Not able to process it, so push it back to the stack
                self.connections.append((x, op, y, '->', t))

        return self.decimal_from_nodes(first_letter='z')



    def _star_2(self) -> str:
        """Solve puzzle 2

        Input bits of numbers x and y, then sum them, if the sum is 2 or larger, keep a one in a, for example:
            5	4	3	2	1	0
        x:	1	0	0	1	1	1
        y:	0	0	1	1	1	0
        - - - - - - - - - - - - -
        a:	0	1	1	1	0	-
        -------------------------
        z:	1	1	0	1	0	1

        First, we compute z0, which is easy:
		    z0 = x0 xor y0
		It's "overflow" is:
		    a1 = x0 and y0
		Then,
		    z1 = (x1 xor y1) xor a1
		its overflow is
		    a2 = (x1 and y1) or (x1 and a1) or (y1 and a1)
		       = (x1 and y1) or ((x1 xor y1) and a1)
		we then re-name two more variables:
		    t1 = (x1 xor y1)
		    xy1 = (x1 and y1)
		So, the formula above becomes
		    a2 = xy1 or (t1 and a1)
		Or in general, we can compute:
		    t_i = x_i xor y_1
		    xy_i = x_i AND y_i
		    a_i = xy_i-1 OR (t_i-1 AND a_i-1)
		    z_i = t_i XOR a_i

        We try to print this for every variable z_i, and find the bug...

        :return:
        """

        def check_expectation(target, left, operator, right) -> bool:
            if target[0] == 'z':
                # We expect z_i = a_i XOR t_1
                return f'a{target[1:]} XOR t{target[1:]}' == f'{left} {operator} {right}'
            if target[0] == 't' and target[1:].isdigit():
                # We expect t_i = x_i XOR y_i
                return f'x{target[1:]} XOR y{target[1:]}' == f'{left} {operator} {right}'
            if target[:2] == 'xy':
                # We expect ex_i = x_i AND y_i
                return f'x{target[2:]} AND y{target[2:]}' == f'{left} {operator} {right}'
            if target[:1] == 'a':
                # We expect a_i = anything OR xy_i or a_i = xy_i-1 OR anything
                return operator == 'OR' and f'xy{int(target[1:])-1:02d}' in (left, right)
            else:
                # We expect anything = a_i AND t_i
                return left[0] == 'a' and operator == 'AND' and right[0] == 't'

        # Tee solution!!!
        # Figured out by slowly examining the errors and running again and again...
        swaps = {
            'z08': 'cdj', 'cdj': 'z08',
            'z16': 'mrb', 'mrb': 'z16',
            'z32': 'gfm', 'gfm': 'z32',
            'qjd': 'dhm', 'dhm': 'qjd',
        }

        if self.is_example:
            # Works only with the real input.
            return ','.join(list(sorted(swaps)))

        self.read_input()
        # Make the renaming (just for display) of the t__ and the xy__
        connection_targets = dict()
        target_renaming = dict()
        for connection in self.connections:
            in1, op, in2, _, t = connection
            if t in swaps:
                t = swaps[t]
            connection_targets[t] = (in1, op, in2)
            if op == 'XOR' and ((in1[0] == 'x' and in2[0] == 'y') or (in1[0] == 'y' and in2[0] == 'x')):
                target_renaming[t] = f't{in1[1:]}'
            elif op == 'AND' and (in1[0] == 'x' and in2[0] == 'y') or (in1[0] == 'y' and in2[0] == 'x'):
                target_renaming[t] = f'xy{in1[1:]}'

        seen = set()
        for target in sorted(connection_targets):
            # Skip some, which are not of importance...
            if target[0] != 'z':
                continue
            if target in ('z00', 'z01', 'z45'):
                continue
            # Try to find the a and make the renaming (for display)
            in1, op, in2 = connection_targets[target]
            if in1 not in target_renaming:
                target_renaming[in1] = f'a{target[1:]}'
            elif in2 not in target_renaming:
                target_renaming[in2] = f'a{target[1:]}'

            # Print all related connections for this output (zXX where XX ranges from 02 to 45)
            out = ''
            que = collections.deque([target])
            while que:
                l = len(que)
                for _ in range(l):
                    t = que.popleft()
                    in1, op, in2 = connection_targets[t]
                    renamed_t = target_renaming.get(t, t)
                    renamed_1 = target_renaming.get(in1, in1)
                    renamed_2 = target_renaming.get(in2, in2)
                    if renamed_2 < renamed_1:
                        renamed_1, renamed_2 = renamed_2, renamed_1
                        in1, in2 = in2, in1
                    out += f"{renamed_t} = {renamed_1} {op} {renamed_2}, "
                    if not check_expectation(renamed_t, renamed_1, op, renamed_2) and target != 'z02':
                        print(f"!!! {renamed_t} = {renamed_1} {op} {renamed_2}, resp. {t} = {in1} {op} {in2}")

                    if in1 not in seen and in1[0] != 'x' and in1[0] != 'y':
                        que.append(in1)
                        seen.add(in1)
                    if in2 not in seen and in2[0] != 'x' and in2[0] != 'y':
                        que.append(in2)
                        seen.add(in2)
            #print(out)

        return ','.join(list(sorted(swaps)))

# ZKB-Ranking
# Star 1: 9.
# Star 2: 13.