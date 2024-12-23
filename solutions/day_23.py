from collections import defaultdict

from . import base_solution as bs


class SolutionDay23(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)
        self.graph = defaultdict(set)
        self.three_cliques = None

    def build_graph(self):
        input_file_path = self.get_input_file_path()
        with open(input_file_path, 'r') as of:
            while line := of.readline().strip():
                node1, node2 = line.split('-')
                self.graph[node1].add(node2)
                self.graph[node2].add(node1)



    def _star_1(self) -> int:
        """Solve puzzle 1

        :return:
        """
        self.build_graph()
        self.three_cliques = set()

        # Count 3-node-circles which have a t-named node.
        count_cycles, cycles_with_t = 0, 0
        for start_node, neighbours in self.graph.items():
            for neighbour in neighbours:
                if neighbour in self.graph:
                    for nn in self.graph[neighbour]:
                        if nn in self.graph and start_node in self.graph[nn]:
                            self.three_cliques.add(tuple(sorted([start_node, neighbour, nn])))
                            count_cycles += 1
                            if start_node[0] == 't' or neighbour[0] == 't' or nn[0] == 't':
                                cycles_with_t += 1

        # We counted each cycle 6 times:
        # A, B, C and A, C, B
        # B, A, C and B, C, A
        # C, A, B and C, B, A
        return cycles_with_t // 6


    def _star_2(self) -> int:
        """Solve puzzle 2

        :return:
        """
        if not self.three_cliques or not self.graph:
            self._star_1()


        def can_add_vertex_to_clique(clique, vertex) -> bool:
            """Check, if we can add it to the clique"""
            for v in clique:
                if v not in self.graph[vertex]:
                    return False
            # All vertices of teh current clique are neighbours of the new vertex
            return True

        cliques = self.three_cliques
        # Assume, we have only one solution...
        while len(cliques) > 1:
            larger_cliques = set()
            for clique in cliques:
                root_node = clique[0]
                for neighbour in self.graph[root_node]:
                    if neighbour in clique:
                        continue
                    # Check, if we can add it to the clique
                    if can_add_vertex_to_clique(clique, neighbour):
                        larger_cliques.add(tuple(sorted(list(clique) + [neighbour])))
            cliques = larger_cliques

        for clique in cliques:
            return ','.join(list(clique))







# ZKB-Ranking
# Star 1: 8.
# Star 2: 16.