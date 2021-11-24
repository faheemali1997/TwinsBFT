class LeaderElection:
    def __init__(self, node, round_leaders):
        self.round_leaders = round_leaders
        self.node = node


    def get_leader(self, round):
    	if round in self.round_leaders:
    		return self.round_leaders[round]
    	else:
    		return none
