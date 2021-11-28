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


class NetworkHub():

    def __init__(self, number_of_nodes, number_of_twins, test_case_scenarios, twins, process_ids):
        self.number_of_nodes = number_of_nodes
        self.number_of_twins = number_of_twins
        self.test_case_scenarios = test_case_scenarios
        self.twins = twins
        self.process_ids = process_ids

    def run(self):

        round_no = 1

        partitions = self.get_partition_for_round(round_no)

        print(list(partitions.values())[0][0])

        from_node_id = self.get_node_id('node1')
        dest_node_id = self.get_node_id('node3')

        partitions = list(self.get_partition_for_round(round_no).values())[0][0]

        should_send = any(dest_node_id in p and from_node_id in p for p in partitions)

        print(should_send)

    def get_node_id(self, process_id):
        key_list = list(self.process_ids.keys())
        val_list = list(self.process_ids.values())
        return key_list[val_list.index(process_id)]

    def get_process_id(self, node_id):
        return self.process_ids[node_id]

    def get_partition_for_round(self, round_no):
        return self.test_case_scenarios[round_no][0]['partitions']

    def receive(self, proposal_msg, p):

        from_node_id = self.get_node_id(p)
        dest_node_id = self.get_node_id(proposal_msg.dest)
        round_no = proposal_msg.round

        if round_no in self.round_partitions:

            # Get the partitions for the specific round. As mentioned in the paper, nodes have their own view of
            # which round they are in and this is included in the message that is sent.
            partitions = list(self.get_partition_for_round(round_no).values())[0][0]

            # Checks if the sender and reciever are in the same partition.
            should_send = any(dest_node_id in p and from_node_id in p for p in partitions)

            # Conditionally send the messages.
            if should_send:

                # if the dest_node_id is a twin id and if the second twin_id in twins is also in same partition then
                # we send the message to both node.
                is_twins = any(dest_node_id in p for p in partitions)

                if is_twins:
                    ##Distalgo send over here to the validator.
                    send(('message', message), to=to_node)
                    send(('message', message), to=to_twin_node)
                else:
                    send(('message', message), to=to_node)

    def receive_vote_msg(self, vote_msg, p):

        from_node_id = self.get_node_id(p)

        dest_node_id = self.get_node_id(vote_msg.dest)

        round_no = vote_msg.round

        if round_no in self.round_partitions:

            # Get the partitions for the specific round. As mentioned in the paper, nodes have their own view of
            # which round they are in and this is included in the message that is sent.
            partitions = list(self.get_partition_for_round(round_no).values())[0][0]

            # Checks if the sender and receiver are in the same partition.
            should_send = any(dest_node_id in p and from_node_id in p for p in partitions)

            # Conditionally send the messages.
            if should_send:

                # if the dest_node_id is a twin id and if the second twin_id in twins is also in same partition then
                # we send the message to both node.
                is_twins = any(dest_node_id in p for p in partitions)

                if is_twins:
                    ##Distalgo send over here to the validator.
                    send(('message', message), to=to_node)
                    send(('message', message), to=to_twin_node)
                else:
                    send(('message', message), to=to_node)

    def receive_timeout(self, timeout_msg, p):

        from_node_id = self.get_node_id(p)

        dest_node_id = self.get_node_id(timeout_msg.dest)

        round_no = timeout_msg.round

        blocked = {}

        if round_no in self.round_partitions:

            # Get the partitions for the specific round. As mentioned in the paper, nodes have their own view of
            # which round they are in and this is included in the message that is sent.
            partitions = list(self.get_partition_for_round(round_no).values())[0][0]

            # Checks if the sender and receiver are in the same partition.
            should_send = any(dest_node_id in p and from_node_id in p for p in partitions) or blocked[(from_node_id, dest_node_id)] == 1

            # Conditionally send the messages.
            if should_send:

                # if the dest_node_id is a twin id and if the second twin_id in twins is also in same partition then
                # we send the message to both node.
                is_twins = any(dest_node_id in p for p in partitions)

                if is_twins:
                    ##Distalgo send over here to the validator.
                    send(('message', message), to=to_node)
                    send(('message', message), to=to_twin_node)
                else:
                    send(('message', message), to=to_node)
            else:
                blocked[(from_node_id,dest_node_id)] = 1



if __name__ == '__main__':
    f = open('../../generator/testcase_1.json')

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    number_of_nodes = data['number_of_nodes']
    number_of_twins = data['number_of_twins']
    twins = data['twins']

    test_case_scenarios = data['test_case_scenarios']

    process_ids = {0: 'node0', 1: 'node1', 2: 'node2', 3: 'node3', 4: 'node4', 5: 'node5', 6: 'node6', 7: 'node7',
                   8: 'node8'}

    network_hub = NetworkHub(number_of_nodes, number_of_twins, test_case_scenarios, twins, process_ids)

    network_hub.run()
