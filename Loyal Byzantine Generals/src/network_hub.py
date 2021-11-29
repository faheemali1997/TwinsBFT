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

sys.path.append('../../generator/testcase_1.json')


def get_test_case_scenarios():
    f = open('../../generator/testcase_1.json')
    data = json.load(f)
    return data['test_case_scenarios'][0]


class NetworkHub:

    def __init__(self, number_of_nodes, number_of_twins, test_case_scenario, twins, process_ids):
        self.number_of_nodes = number_of_nodes
        self.number_of_twins = number_of_twins
        self.test_case_scenario = test_case_scenario
        self.twins = twins
        self.process_ids = process_ids
        self.blocked = {}

    def get_node_id(self, process_id):
        key_list = list(self.process_ids.keys())
        val_list = list(self.process_ids.values())
        return key_list[val_list.index(process_id)]

    def get_process_id(self, node_id):
        return self.process_ids[node_id]

    def get_partition_for_round(self, round_no):
        return self.test_case_scenario[0]['partitions'][str(round_no)]

    def is_twins(self, node_id):

    def should_send_proposal_msg(self, proposal_msg, p):
        from_node_id = self.get_node_id(p)
        dest_node_id = self.get_node_id(proposal_msg.dest)
        round_no = proposal_msg.round_no
        # Get the partitions for the specific round. As mentioned in the paper, nodes have their own view of
        # which round they are in and this is included in the message that is sent.
        partitions = self.get_partition_for_round(round_no)[0]

        # Checks if the sender and receiver are in the same partition
        # and also check the intra partition message drop scenario
        return any(dest_node_id in p and from_node_id in p for p in partitions)

    #
    def should_send_vote_msg(self, vote_msg, p):

        from_node_id = self.get_node_id(p)

        dest_node_id = self.get_node_id(vote_msg.dest)

        round_no = vote_msg.round_no

        # Get the partitions for the specific round. As mentioned in the paper, nodes have their own view of
        # which round they are in and this is included in the message that is sent.
        partitions = self.get_partition_for_round(round_no)[0]

        # Checks if the sender and receiver are in the same partition.
        return any(dest_node_id in p and from_node_id in p for p in partitions)

    def should_send_timeout_msg(self, timeout_msg, p):

        from_node_id = self.get_node_id(p)

        dest_node_id = self.get_node_id(timeout_msg.dest)

        round_no = timeout_msg.round_no

        # Get the partitions for the specific round. As mentioned in the paper, nodes have their own view of
        # which round they are in and this is included in the message that is sent.
        partitions = self.get_partition_for_round(round_no)[0]

        # Checks if the sender and receiver are in the same partition.
        should_send = any(dest_node_id in p and from_node_id in p for p in partitions)

        if (from_node_id,dest_node_id) in self.blocked:
            blocked_once = self.blocked[(from_node_id, dest_node_id)] == 1
        else:
            blocked_once = False

        if should_send and blocked_once:

            self.blocked[(from_node_id, dest_node_id)] = 0

            return True

        elif should_send and not blocked_once:

            self.blocked[(from_node_id, dest_node_id)] = 1

            return False

        else:

            return False


# class ProposalMsg1:
#     def __init__(self, round_no, dest):
#         self.round_no = round_no
#         self.dest = dest


# if __name__ == '__main__':
#     f = open('../../generator/testcase_1.json')
#
#     # returns JSON object as
#     # a dictionary
#     data = json.load(f)
#
#     number_of_nodes = data['number_of_nodes']
#     number_of_twins = data['number_of_twins']
#     twins = data['twins']
#
#     test_case_scenario = data['test_case_scenarios'][0]
#
#     process_ids = {0: 'node0', 1: 'node1', 2: 'node2', 3: 'node3', 4: 'node4', 5: 'node5', 6: 'node6', 7: 'node7',
#                    8: 'node8'}
#
#     network_hub = NetworkHub(number_of_nodes, number_of_twins, test_case_scenario, twins, process_ids)
#
#     proposal_msg = ProposalMsg1(
#         1,
#         'node6'
#     )
#
#     print(network_hub.should_send_timeout_msg(proposal_msg, 'node0'))
#     print(network_hub.should_send_timeout_msg(proposal_msg, 'node0'))

