"""
1a. Two(Twins) leaders send Proposal message to network hub
    - If both twins are in same partition:
        - Send to all nodes with normal node as leader within that partition
    - If both are in different partition
        - Send from both twins to all nodes in those partitions, sending sender as normal node
1b. Leader is non byzentine,
    - Send to only nodes within that partition,rest drop messages

=========================Next Leader Election happens==========================================

1a.

1 :Two(Twins) leaders send Proposal message to network hub
2: If both twins are in same partition:
   Send to all nodes with normal node as leader
"""
import json
import sys
from collections import defaultdict

sys.path.append('../../generator/testcase_1.json')

# loop through array of partitions, partition[0] -> array of partitions
def get_partition_per_round(test_case):

    ans = defaultdict(list)

    for k, v in test_case['partitions'].items():

        ans[k].append(v[0])

    return ans

# starightforward, round_leaders[k] -> array
def get_round_leaders(test_case):

    ans = defaultdict(list)

    for k, v in test_case['round_leaders'].items():

        ans[k].append(v)

    return ans


def get_random_message_drops(test_case):

    ans = defaultdict(list)

    for k, v in test_case['random_message_drops'].items():

        if len(v) > 0:
            ans[k].append(v[0])

    return ans


class NetworkHub:

    def __init__(self, test_case, validators_map: dict, test_case_scenario):

        self.number_of_nodes = int(test_case['number_of_nodes'])
        self.number_of_twins = int(test_case['number_of_twins'])
        self.twins = test_case['twins']
        self.process_ids = validators_map
        self.blocked = {}
        self.test_case_scenario = test_case_scenario
        self.round_leaders = test_case_scenario['round_leaders']
        self.partitions = test_case_scenario['partitions']
        self.random_message_drops = test_case_scenario['random_message_drops']
        self.partitions_per_round = get_partition_per_round(test_case_scenario)
        self.round_leaders_per_round = get_round_leaders(test_case_scenario)
        self.random_message_drops_per_round = get_random_message_drops(test_case_scenario)

    def should_send_proposal_msg(self, p, d, round_no):

        partitions = self.partitions_per_round[round_no]

        message_drop = self.random_message_drops_per_round[round_no]

        if message_drop and 'Proposal' in message_drop and p in message_drop and d in message_drop:
            return False

        for partition in partitions:

            if p in partition and d in partition:
                return True

        return False

    def should_send_vote_msg(self, p, d, round_no):

        partitions = self.partitions_per_round[round_no]

        message_drop = self.random_message_drops_per_round[round_no]

        if message_drop and 'Vote' in message_drop and p in message_drop and d in message_drop:
            return False

        for partition in partitions:

            if p in partition and d in partition:
                return True

        return False

    def should_send_timeout_msg(self, p, d, round_no):

        partitions = self.partitions_per_round[round_no]

        message_drop = self.random_message_drops_per_round[round_no]

        if message_drop and 'Timeout' in message_drop and p in message_drop and d in message_drop:
            return False

        for partition in partitions:

            if p in partition and d in partition:
                return True

        return False


if __name__ == '__main__':
    with open('../testcases/testcase_1.json') as f:

        data = json.load(f)

        test_case_scenarios = data['test_case_scenarios']

        for test in test_case_scenarios:
            nh = NetworkHub(data, dict(), test[0])
            val = nh.should_send_proposal_msg(0, 4, 1)
            print(val)


