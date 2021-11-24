class Network_Playground:

	def __init__(self, round_partitions: [], round_leaders:[], pids: [], num_of_twins, delay, intra_partition_drops[], twins):
		self.round_partitions = round_partitions
		self.round_leaders = round_leaders
		self.num_of_twins = num_of_twins
		self.delay = delay
		self.pids = pids
		self.twins = twins ##[0,1] -> These two nodes are twins
		self.nodes = dict()
		self.intra_partition_drops = intra_partition_drops


	## To create a mapping of nodes and the process ids
	def add_node(self, node, pid):
		self.nodes[pid] = node

	## Generate a mappings for twin id vs process id 
	def mapping_nodes_process_ids():
		count = 0
		for pid in pids:
			add_node(pid, count)
			count++

	## Receive messages sent by the replicas
	def receive(('message',message), from_=node):
		self.send(node, message.to_node, message)


	def send(self, from_node, to_node, message):
		"""
		Restricted Send function based on partitions

		Keyword arguments:
		from_node -- Node Sending the message
		to_node -- Node to which the message is to be sent
		message -- Message that has to be sent
		"""

		##In this function we selctively choose if we should send the message or not based on the partions in the scnearios.
		##If the nodes are in the same partition only then we forward the message to the destination.
		##Otherwise we drop the message to simulate the scenario.
		from_node_id = self.nodes[from_node]
		to_node_id = self.nodes[to_node]
		round = from_node.round

		if round in self.round_partitions:

			#Get the partitions for the specific round. As mentioned in the paper, nodes have their own view of which round they are in and this is included in the message that is sent.
			partitions = self.round_partitions[round]

			#Checks if the sender and reciever are in the same partition.
			should_send = any(to_node_id in p and from_node_id in p for p in partitions) && intra_partition_message_drop

			#Conditionally send the messages.
			if should_send:
				
				##if the to_node_id is a twin id and if the second twin_id in twins is also in same partition then we send the message to both node.
				is_twins = any(to_node_id in p for p in partitions)
				
				if is_twins:
					##Distalgo send over here to the validator.
					send(('message', message), to = to_node)
					send(('message', message), to = to_twin_node)
				else:
					send(('message', message), to = to_node)



	def intra_partition_message_drop() -> boolean:
		return any(to_node_id in p for p in intra_partition_drops)







