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
import os
import sys
from collections import defaultdict
import hashlib
import re



# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

sys.path.append('../../generator/testcase_1.json')
sys.path.append('../config')


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

        partitions = self.partitions_per_round[str(round_no)]

        message_drop = self.random_message_drops_per_round[str(round_no)]

        if message_drop and 'Proposal' in message_drop and p in message_drop and d in message_drop:
            return False

        for partition in partitions[0]:

            if p in partition and d in partition:
                return True

        return False

    def should_send_vote_msg(self, p, d, round_no):

        partitions = self.partitions_per_round[str(round_no)]

        message_drop = self.random_message_drops_per_round[str(round_no)]

        if message_drop and 'Vote' in message_drop and p in message_drop and d in message_drop:
            return False

        for partition in partitions[0]:

            if p in partition and d in partition:
                return True

        return False

    def should_send_timeout_msg(self, p, d, round_no):

        partitions = self.partitions_per_round[str(round_no)]

        message_drop = self.random_message_drops_per_round[str(round_no)]

        if message_drop and 'Timeout' in message_drop and p in message_drop and d in message_drop:
            return False

        for partition in partitions[0]:

            if p in partition and d in partition:
                return True

        return False


def check_safety():
    path = os.path.realpath('../') + '/ledgers'
    configs_gen = os.listdir(path)
    for config in configs_gen:
        if config == '.DS_Store':
            continue
        config_no = int(re.findall(r'\d+', config)[0])
        ledgers = os.listdir(path + '/' + config)
        ledger_hash = defaultdict(int)
        for ledger in ledgers:
            ledger_path = path + '/' + config + '/' + ledger
            with open(ledger_path, 'rb') as f:
                md5 = hashlib.md5()
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    md5.update(data)
                ledger_hash[md5.hexdigest()] += 1

        for count in ledger_hash:
            if ledger_hash[count] > 2:
                print('Safety Holds')
            else:
                print('Safety Violated')

def check_safety1():
    path = os.path.realpath('../') + '/ledgers' + '/' + 'config0'
    ledgers = os.listdir(path)
    ledger_hash = defaultdict(int)
    for ledger in ledgers:
        ledger_path = path + '/' + '/' + ledger
        with open(ledger_path, 'rb') as f:
            md5 = hashlib.md5()
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
            ledger_hash[md5.hexdigest()] += 1

    for count in ledger_hash:
        if ledger_hash[count] > 2:
            print('Safety Holds')
        else:
            print('Safety Violated')

def check_liveness():
    path = os.path.realpath('../') + '/ledgers'
    configs = os.listdir(path)
    for config in configs:
        if config == '.DS_Store':
            continue
        ledgers = os.listdir(path + '/' + config)
        ledger_hash = defaultdict(int)
        for ledger in ledgers:
            ledger_path = path + '/' + config + '/' + ledger
            if os.stat(ledger_path).st_size == 0:
                ledger_hash[config] += 1

        for count in ledger_hash:
            if ledger_hash[count] > 4:
                print('Liveliness Holds')
            else:
                print('Liveliness Violated')

def check_liveness1():
    path = os.path.realpath('../') + '/ledgers' + '/' + 'config0'
    ledgers = os.listdir(path)
    count = 0
    for ledger in ledgers:
        ledger_path = path + '/' + '/' + ledger
        if os.stat(ledger_path).st_size == 0:
            count += 1

    if count > 2:
        print('Liveness Holds')
    else:
        print('Liveness Violated')

if __name__ == '__main__':
    check_safety1()
    check_liveness1()


    # with open('../testcases/testcase_1.json') as f:
    #
    #     data = json.load(f)
    #
    #     test_case_scenarios = data['test_case_scenarios']
    #
    #     for test in test_case_scenarios:
    #         nh = NetworkHub(data, dict(), test[0])
    #         val = nh.should_send_proposal_msg(0, 4, 1)
    #         print(val)
