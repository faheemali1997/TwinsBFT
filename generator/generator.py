import random

from generator.stringling import stirling2
from itertools import product
from json import dumps
from collections import defaultdict
from itertools import combinations
from iteration_utilities import random_combination
from os.path import join
import os


class TestGenerator:

    def __init__(self, config):
        """
        0 1 2 3 4.....n -> Nodes
        0 1 2 3 4.....f -> byzentine nodes
        n + f -> Twin

        For example, if n = 7, we have 2 byzentine nodes

        byzentine   normal       twins of byzentine nodes
        0 1       | 2 3 4 5 6  | 7 8

        """
        num_nodes = int(config['nvalidators'])
        rounds = int(config['rounds'])
        limit = int(config['limit_test_cases'])
        randomness = config['randomness'] == 'True'
        num_byzentine = int(config['nfaulty'])
        self.num_partitions = int(config['partitions'])
        nodes = [i for i in range(num_nodes)]
        self.total_nodes = nodes
        self.rounds = rounds
        self.number_of_byzentine_nodes = num_byzentine
        self.byzentine_nodes = [w for w in range(self.number_of_byzentine_nodes)]
        self.nodes = [w for w in range(len(self.total_nodes) + len(self.byzentine_nodes))]
        self.limit = limit
        self.twins = self.generate_twins(self.byzentine_nodes)
        self.randomness = randomness
        self.output_file = config['output_file_name']

    def generate_twins(self, byzentine_nodes: list):

        twins = defaultdict(list)

        for node in byzentine_nodes:
            twins[node] = self.get_twin(node)

        return twins

    def get_twin(self, node):

        assert node in self.byzentine_nodes
        return self.nodes[len(self.total_nodes) + node]

    def make_partitions(self, limit: int = 4):

        return stirling2(len(self.nodes), min(limit, self.num_partitions))

    def combine_leader_partition_random(self, partitions):

        all_leaders = self.byzentine_nodes[::]

        size = len(partitions)

        while size > 0:

            random_partition = random.randint(0, size - 1)

            partition = partitions[random_partition]

            if len(all_leaders) == 0:
                leader = 0
            else:
                leader = random.randint(0, len(all_leaders) - 1)

            yield leader, partition

            size -= 1

            partitions.pop(random_partition)

    def combine_partitions_leaders(self, partitions):

        """:ivar

        We need generators here to limit. Generators are like iterators in Java/C++.

        """

        all_leaders = self.byzentine_nodes[::]

        for partition in partitions:

            for leader in all_leaders:

                yield leader, partition

    def combine_scenarios_with_rounds(self, cases, limit: int):

        # select random combinations of leader, round and partition
        return combinations(cases, r=self.rounds)

    @staticmethod
    def empty_list():
        return []

    @staticmethod
    def select_random_nodes_within_partition(partition: list):

        result = []

        idx = random.randint(0, len(partition) - 1)

        if len(partition[idx]) < 2:
            return []

        # select two nodes within random partition and drop the messages among them
        li = random.sample(range(0, len(partition) - 1), 2)

        message = ['Proposal', 'Vote', 'Timeout']

        return [message[random.randint(0, len(message) - 1)], partition[idx][li[0]], partition[idx][li[1]]]

    def get_json_dump(self, testcases):

        json_dump = []

        """
        
        If we have only one node in round_leaders, it is non-byzentine
        else, it is byzentine.
             
        """

        for testcase in testcases:

            round_leaders, round_partitions = defaultdict(TestGenerator.empty_list), defaultdict(
                TestGenerator.empty_list)

            random_message_drops = defaultdict(list)

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

                message_drop = random.randint(0, 1)

                # Generate random message drops
                message_drops_nodes = TestGenerator.select_random_nodes_within_partition(round_partition)

                if message_drop:
                    random_message_drops[round_number + 1].append(message_drops_nodes)

            json_dump.append([{
                'round_leaders': round_leaders,
                'partitions': round_partitions,
                'random_message_drops': random_message_drops
            }])

        return dumps(
            {
                'number_of_nodes': len(self.total_nodes),
                'number_of_twins': len(self.byzentine_nodes),
                'test_case_scenarios': json_dump,
                'twins': self.twins
            },
            indent=3
        )

    def write_to_file(self, json_dump, file_name):

        with open('../testcases/' + file_name, 'a') as file:
            file.write(json_dump)

        print("Writing Done, Thank You")

    def run(self, offline: bool):

        # make partitions make_partitions(limit, number_of_partitions)
        partitions = self.make_partitions()

        # Generate leader partition pairs randomly
        if self.randomness:
            scenarios = self.combine_leader_partition_random(partitions)

        # Generate leader partition pairs in order based on user input
        else:
            scenarios = self.combine_partitions_leaders(partitions)

        # Limit generated during constructor, if it's None, it is defaulted to 10
        limit = 10 if self.limit is None else self.limit

        # Generate leader_partition_pairs with rounds
        testcases = self.combine_scenarios_with_rounds(scenarios, limit)

        # Create a new array for holding testcases
        testcases_new = []

        # Generate all test_cases
        for testcase in testcases:

            if limit == 0:
                break

            limit -= 1

            testcases_new.append(testcase)

        # Create json dump for dumping to file
        json_dump = self.get_json_dump(testcases_new)

        # Offline means writing to file
        if not offline:
            return json_dump

        # Write to file so that executor reads it from there
        self.write_to_file(json_dump, self.output_file)


if __name__ == '__main__':

    config = {
        'nvalidators': "7",
        'nfaulty': "2",
        'rounds': "10",
        'limit_test_cases': "20",
        'randomness': 'True',
        'partitions': 3,
        'output_file_name': 'testcase_1.json'
    }

    gen = TestGenerator(config)

    gen.run(True)




