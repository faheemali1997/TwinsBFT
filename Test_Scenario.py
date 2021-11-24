from network_playground import NetworkPlayGround

class Test_Executor(Process):
	
	def __init__(self, file_path):
		""" 
		Initialising the Scenarion Execute_Scenario
        
		Keywork arguments:
		file_path -- Path of the file to read the testcases from.

		"""

		## To support offline mode we will be reading the testcases/scenarios from the file
		## to which test generator had written all the testcases.
		with open(file_path) as f:
            data = load(f)

        self.num_of_nodes = data['num_of_nodes']
        self.num_of_twins =data['num_of_twins']
        self.nodes = start_nodes_and_twins(num_of_nodes,num_of_twins)
        #Scenarios for testcases. This includes round_leaders and round_partitions.
        self.scenarios = data['scenarios']
    	self.round_leaders = scenario['round_leaders']
        self.round_partitions = scenario['round_partitions'] 
        
        self.twins = choose_twins_randomly()
        self.replicas = []

        # Here, we are reading config, keys and other_nodes_public_key from file and creating replicas.

        for r in self.nodes:

            replica = Replica(num = self.num_of_nodes + self.num_of_twins)
            # read the config from config file

            # If node is a twin of someother node, we get that node's public and private keys
            # Otherwise , we get the keys of that corresponding nodes
            
            if r is twin:
                setup(replica, config=config(), keys = get_keys(twin(r)), other_nodes_public_key = get_keys(all))

            else:
                setup(replica, config = config(), keys = get_keys(r), other_nodes_public_key = get_keys(all))

            self.replicas.append(replica)



    def choose_twins_randomly(self):
        if number < 1:
            return None

        return random(round_partitions, num_of_twins)



    def run(self):
    	"""
    	Main Run method

    	"""
    	#Enumerating over all the scenarios in the testcases.

    	for i, scenario in enumerate(self.scenarios):
            network_playground = new NetworkPlayGround(self.round_partitions, self.round_leaders, self.num_of_twins, self.replicas, 0)
            start(self.replicas)

        assert(safety_check())
        assert(liveness_check())


    def safety_check():
        """

        We keep the map of hashes of file contents 
        
        """
        map = dict()

        for each file in ledger_files:

                map[sha256(file)] += 1

        return max([value for key,value in map.items()]) >= 2f + 1


    def liveness_check():
        """
        We can check if the file size is increasing in bytes?

        We compare the size of the ledger file at an instance and then check the size of file again after some time has elapsed
        We either sleep for sometime or we can wait for few rounds to complete and then check liveness violations.
        We keep on doining this in parallel thread along with checking for safety violations

        """

        number = 0

        for each file in ledger_files:

                # We compare the latest speculated state id round and latest round of commited state id and calculate the difference between them
                # If it's greather than threshold, it means that node is not lively, i.e, not commiting.
                if  round of speculated_state_id - round of commit_state_id > threshold:
                       number += 1
        
        return not number > 2f + 1

"""

creat main function

"""

def main():

    file_path = input()

    test_executor = Test_Executor(file_path)

    test_executor.run()


def config():

    return from file

def get_keys():

    return from file
        



