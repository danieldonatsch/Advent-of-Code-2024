from . import base_solution as bs


class SolutionDay13(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)

    def get_claw_machines(self) -> list:
        def parse_line(line, sep):
            _, values = line.split(':')
            x, y = [val.split(sep)[1]for val in values.split(',')]
            return int(x), int(y)


        input_file_path = self.get_input_file_path()
        machines = []
        with open(input_file_path, 'r') as of:
            while True:
                machine = {}
                for button in ['A', 'B']:
                    line = of.readline().strip()
                    x, y = parse_line(line, '+')
                    machine[button] = {'x': x, 'y': y}
                line = of.readline().strip()
                x, y = parse_line(line, '=')
                machine['prize'] = {'x': x, 'y': y}
                machines.append(machine)
                if not of.readline():
                    break
        return machines

    def _star_1(self) -> None:
        """Fill in description and code...

        :return:
        """
        machines = self.get_claw_machines()
        cost_a = 3
        cost_b = 1
        total_cost = 0
        for machine in machines:
            # We first check the X values
            n_b = min(machine['prize']['x'] // machine['B']['x'], 100)
            while n_b >= 0:
                rest = machine['prize']['x'] - n_b * machine['B']['x']
                if rest % machine['A']['x'] == 0:
                    n_a = rest // machine['A']['x']
                    # The combination of pressing A n_a times and B n_b times leads to the correct X position
                    if machine['prize']['y'] == n_a * machine['A']['y'] + n_b * machine['B']['y']:
                        # This is the cost for the current machine! Since we go gready, we can stop:
                        total_cost += n_a * cost_a + n_b * cost_b
                        # Go to the next machine
                        break
                # Try to push the B-button once less...
                n_b -= 1

        return total_cost

    def _star_2(self) -> None:
        """Fill in description and code...

        a * Ax + b * Bx = Px
        a * Ay + b * By = Py
        Then we look for a and b:
        a * Ax = Px - b * Bx
        a * Ay = Py - b * By

        a = (Px - b * Bx) / Ax
        ((Px - b * Bx) / Ax) * Ay = Py - b * By
         (Px - b * Bx) * Ay/Ax    = Py - b * By
          Px * Ay/Ax    - Py      = b * Bx * Ay/Ax - b * By
          Px * Ay/Ax    - Py      = b * (Bx * Ay/Ax - By)
         (Px * Ay/Ax - Py) / (Bx * Ay/Ax - By) = b
        ((Px * Ay - Py * Ax) / Ax) / ((Bx * Ay - By * Ax) / Ax) = b
         (Px * Ay - Py * Ax) / (Bx * Ay - By * Ax) = b


         a * Ax * Ay =
         Ay * (Px - b * Bx) = Ax * (Py - b * By)
         Ay * Px - b * Ay * Bx = Ax * Py - b * Ax * By
         (Ax * By - Ay * Bx) * b = Ax * Py - Ay * Px
         b = (Ax * Py - Ay * Px) / (Ax * By - Ay * Bx)

        :return:
        """
        machines = self.get_claw_machines()
        cost_a = 3
        cost_b = 1
        total_cost = 0
        for machine in machines:
            machine['prize']['x'] += 10000000000000
            machine['prize']['y'] += 10000000000000
            # From
            # a * Ax + b * Bx = Px
            # a * Ay + b * By = Py
            # compute
            # b = (Ax * Py - Ay * Px) / (Ax * By - Ay * Bx)
            b = ((machine['A']['x'] * machine['prize']['y'] - machine['A']['y'] * machine['prize']['x']) /
                 (machine['A']['x'] * machine['B']['y'] - machine['A']['y'] * machine['B']['x']))
            if b != int(b):
                continue
            # Now we can compute a
            # a * Ax + b * Bx = Px -> a = (Px - b * Bx) / Ax
            a = (machine['prize']['x'] - b * machine['B']['x']) / machine['A']['x']
            if a != int(a):
                continue

            total_cost += int(a * cost_a + b * cost_b)

        return total_cost

# ZKB-Points
# 1425 -> 1498
# 1522 -> 1585
