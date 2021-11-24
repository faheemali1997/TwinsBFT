Class Test_Generator {
    function partition_generator(limit)“””
    generate all possible partitions given n nodes into k partitions by capping the limit the number of partitions.
    The concept used to generate partitions here is "Stirling Number of Second    Kind" - it returns the total number of ways nodes can be divided into k partitions.

    “””
    // Returns: list of  all possible partitions.
    function stirling2kinds(n, k)
    //  Arguments
    //  n : The number of objects.
    //  k : The number of sets. If k = n the nodes in the set will be divided in only n partitions.
    // assuming always the case that n and k are greater than 0

    if k equal 1
    return (node
        for node in range(n))
    elif k equal n
    return (list(node) for node in range(n))
    else
        recursion_n1k1 = stirling2kinds(n - 1, k - 1)
    for i in range(len(recursion_n1k1))
    recursion_n1k1[i].append(list(n - 1))
    var = stirling2kinds(n - 1, k)
    recursion_n1k = []
    while range(k)
    recursion_n1k = recursion_n1k +
        var
    for i in range(len(tmp) * k)
    recursion_n1k[i][i // len(var)] = recursion_n1k [i][i // len(var)] +  [n-1]
            return (recursion_n1k1 + recursion_n1k)

            return stirling2kinds(len(nodes), min(no_of_partition, limit))




            function leader_selection(nodes, flag, byz_nodes):
            // The function performs a flag check if 0 then any node can become leader and if 1 only byzantine nodes can become leader
            // It returns set of leader nodes.
            if flag == 0
            return (nodes)
            else
                leader_nodes = []
            for node in nodes
            if node in byz_nodes
            leader_nodes.append(node)
            return (leader_nodes)


            function partition_leader_pair(partitions, limit)
            // Each Partition from the previous function should be assigned possible leaders.
            // Arguments : l set of possible leaders, L set of all possible leaders
            // Output: A sequence of tuples of (leader, partition) pair
            // Limit the number of tuples
            leaders = leader_selection(partitions, flag, byz_nodes)
            tuples = []
            for partition in partitions
            for leader in leaders
            If len(tuples) > limit:
            break
            tuples.append(tuple(leader, partition))

            return tuples


            function partition_leader_round_pair(scenarios)
            // join all leader-partition pair scenarios with rounds.
            // Arguments : tuple of leader-partition pair from partition_leader_pair function        
            // Output: A sequence of all testcases.
            // The product function from Itertools library generates cartesian product of provided scenarios with itself for given number of rounds
            // For optimization purposes we will discard those leader-partition round pairs which are textually different but logically same.
            Example - [B, A, C][C ', D] is logically equivalent to [A,D,C][C', B] or[C ',A][B,C,D]
                scenarios = partition_leader_pair(scenarios) return product(scenarios, repeat = rounds)


                function intra_partition_m_drop(partition)
                // This function drops messages for specified nodes within a partition
                // Arguments: partition where those nodes lie.

                return (stirling2kinds(partiton, 2))
                // above function will return all possible subpartition for the partition provided[A,A',B,C]
                // we will choose only that partition where the case is [A,C][A',B], given we want to drop a message from C for A' and B


                function writer(threshold)
                // This function will write all the generated scenarios in a file for offline function
                // Arguments: Here we pass a threshold (variable) which prunes or discards those test scenarios which contains less than 2f+1 nodes in at least one partition also for
                number of consecutive threshold partition pairs.
                // for example: if threshold = 2, then the function will prune
                [A, B][A ',C], [A,C][A', B], [A, B][A '][C] - generator will reject this entire set of scenario [A, B][A ',C][D], [A,B,C][A', D],
                    [A, B, C, D][A '] - generator will pass this
                        // The above will ensure that only those test cases are passed for which generator can guarantee liveness 
                        function live_pruner(testcases)
                        testcases = partition_leader_round_pair(scenarios)
                        flag = 1
                        for partitioncase in testcases
                        for partition in partitioncase
                        If(any(subpartition) of partition) is not equal 2 f + 1 and flag = 1
                        count = count + 1
                        flag = 1
                        else
                            flag = 0
                        If count equal threshold
                        testcases.remove(partitioncase)
                        refined_testcases = live_pruner(testcases)
                        write_to_file(refined_testcases)


                        function rand_determ(flag, no_of_scenarios, testcases)
                        //This function will determine if the user is asking for deterministic test cases or random test cases
                        // if flag = 0, random else deterministic
                        // for deterministic, we have implemented that it will return only first n number of scenarios requested by tester, but for future implementation we will implement deterministic according to tester needs, i.e. tester or user can ask for a specific chunk of testcases.
                        if flag == 0
                        Items = random.randrange(no_of_scenarios)
                        for item in items:
                        feed_data = read_from_file(testcases[item])
                        return (feed_data)
                        else
                            return (read_from_files(testcases[: no_of_scenarios]))

                        function execution_feeder()
                        //the function requests chunk of test cases by calling rand_determ function
                        and then feeding it to scenario executor one by one.
                        feed_data = rand_determ(flag, no_of_scenarios, testcases)
                        for i in range(len(feed_data))
                        send_to_executor(feed_data[i])


                    }