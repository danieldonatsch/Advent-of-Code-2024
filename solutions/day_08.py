from . import base_solution as bs

from collections import defaultdict


class SolutionDay08(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.n_rows = 0
        self.n_cols = 0
        self.antenna_locations = None

    def compute_antenna_locations(self):
        """Reads the file and computes all antenna locations. Saves them in a dict, ordered by antenna frequency.

        :return: None
        """
        input_file_path = self.get_input_file_path()

        self.antenna_locations = defaultdict(list)
        with open(input_file_path, 'r') as of:
            row = 0
            while line := of.readline().strip():
                width = len(line)
                for col, antenna in enumerate(line):
                    if antenna != '.':
                        self.antenna_locations [antenna].append((row, col))
                row += 1
        # City size
        self.n_rows = row
        self.n_cols = width

    def _star_1(self) -> None:
        """Computes anti nodes which are one "hop" away from the antennas

        :return: (int) anti nodes which are one "hop" away from the antennas
        """
        def compute_anti_nodes(locations) -> list:
            anti_nodes = list()
            # Compute the difference of every pair
            for i in range(len(locations) - 1):
                for j in range(i + 1, len(locations)):
                    dx = locations[i][0] - locations[j][0]
                    dy = locations[i][1] - locations[j][1]
                    # Compute the anti-nodes and see if they are still on the grid
                    anti_node = locations[i][0] + dx, locations[i][1] + dy
                    if 0 <= anti_node[0] < self.n_rows and 0 <= anti_node[1] < self.n_cols:
                        anti_nodes.append(anti_node)
                    anti_node = locations[j][0] - dx, locations[j][1] - dy
                    if 0 <= anti_node[0] < self.n_rows and 0 <= anti_node[1] < self.n_cols:
                        anti_nodes.append(anti_node)

            return anti_nodes

        if self.antenna_locations is None:
            self.compute_antenna_locations()

        # Use a set to make sure, all found anti-nodes are unique
        all_anti_nodes = set()
        for locations in self.antenna_locations.values():
            all_anti_nodes.update(compute_anti_nodes(locations))
        return len(all_anti_nodes)

    def _star_2(self) -> None:
        """Computes all anti nodes which are in the city. Also, each antenna location is an anti-node!

        :return:
        """

        def compute_anti_nodes(nodes) -> list:
            anti_nodes = list()
            # Compute the difference of every pair
            for i in range(len(nodes) - 1):
                for j in range(i + 1, len(nodes)):
                    dx = nodes[i][0] - nodes[j][0]
                    dy = nodes[i][1] - nodes[j][1]
                    x, y = nodes[i]
                    # One direction
                    hops = 1
                    while 0 <= (nx := x + hops * dx) < self.n_rows and 0 <= (ny := y + hops * dy) < self.n_cols:
                        anti_nodes.append((nx, ny))
                        hops += 1
                    # The other direction
                    hops = -2  # Start with -2, since the hop -1 would be to nodes[j]
                    while 0 <= (nx := x + hops * dx) < self.n_rows and 0 <= (ny := y + hops * dy) < self.n_cols:
                        anti_nodes.append((nx, ny))
                        hops -= 1
            return nodes + anti_nodes

        if self.antenna_locations is None:
            self.compute_antenna_locations()

        # Use a set to make sure, all found anti-nodes are unique
        all_anti_nodes = set()
        for locations in self.antenna_locations.values():
            all_anti_nodes.update(compute_anti_nodes(locations))
        return len(all_anti_nodes)

# Star1: 652 -> 716
# Star2: 716 -> 758