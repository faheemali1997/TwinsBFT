from stringling import stirling2
from itertools import product
from json import dumps
from collections import defaultdict
from os.path import join
import os


class TestGenerator:

    def __init__(self, nodes: list, rounds: int):
        """
        0 1 2 3 4.....n -> Nodes
        0 1 2 3 4.....f -> byzentine nodes
        n + f -> Twin

        For example, if n = 7, we have 2 byzentine nodes

        byzentine   normal       twins of byzentine nodes
        0 1       | 2 3 4 5 6  | 7 8

        """
        self.total_nodes = nodes
        self.rounds = rounds
        self.number_of_byzentine_nodes = (len(nodes) - 1) // 3
        self.byzentine_nodes = [w for w in range(self.number_of_byzentine_nodes)]
        self.nodes = [w for w in range(len(self.total_nodes) + len(self.byzentine_nodes))]

    def get_twin(self, node):

        assert node in self.byzentine_nodes
        return self.nodes[len(self.total_nodes) - 1 + node]

    def make_partitions(self, limit: int, partitions: int):
        
        return stirling2(len(self.total_nodes), min(limit, partitions))

    def combine_partitions_leaders(self, partitions):

        """:ivar

        We need generators here to limit. Generators are like iterators in Java/C++.

        """

        all_leaders = self.byzentine_nodes[::]

        for partition in partitions:
            for leader in all_leaders:
                yield (leader, partition)

    def combine_scenarios_with_rounds(self, cases):

        return product(cases, repeat=self.rounds)

    @staticmethod
    def empty_list():
        return []

    def get_json_dump(self, testcases):

        json_dump = []

        """
        
        If we have only one node in round_leaders, it is non-byzentine
        else, it is byzentine.
             
        """

        
        for testcase in testcases:

            round_leaders, round_partitions = defaultdict(TestGenerator.empty_list), defaultdict(
                TestGenerator.empty_list)

            for round_number, partition in enumerate(testcase):

                # (0, [[0, 1, 2, 3, 4, 5, 6], [7], [8]])
                # leader - 0
                # partition - [[0, 1, 2, 3, 4, 5, 6], [7], [8]]

                round_leader = partition[0]

                round_partition = partition[1]

                round_leaders[round_number+1].append(round_leader)

                if round_leader in self.byzentine_nodes:
                    round_leaders[round_number+1].append(self.get_twin(round_leader))

                round_partitions[round_number+1].append(round_partition)

            json_dump.append([{
                'round_leaders': round_leaders,
                'partitions': round_partitions
            }])

        return dumps(
            {
                'number_of_nodes': len(self.total_nodes),
                'number_of_twins': len(self.byzentine_nodes),
                'test_case_scenarios': json_dump
            },

            indent=4
        )

    def write_to_file(self, json_dump, file_name):

        with open(file_name, 'a') as file:
            file.write(json_dump)

        print("Writing Done, Thank You")


    def run(self, offline: bool):

        partitions = self.make_partitions(4, 3)

        scenarios = self.combine_partitions_leaders(partitions)

        testcases = self.combine_scenarios_with_rounds(scenarios)

        limit = 10

        testcases_new = []

        for testcase in testcases:

            if limit == 0:
                break

            limit -= 1

            testcases_new.append(testcase)

        json_dump = self.get_json_dump(testcases_new)

        if not offline:
            return json_dump

        self.write_to_file(json_dump, 'testcase_1.json')



if __name__ == '__main__':

    gen = TestGenerator([0, 1, 2, 3, 4, 5, 6], 2)

    gen.run(True)




