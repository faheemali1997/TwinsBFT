from copy import deepcopy


def stirling2(n, k):
    """ Provides solutions of the Stirling Number of the Second Kind.

    Args:
        n (int): The number of objects.
        k (int): The number of sets.

    Returns:
        list: All solutions of the Stirling number of the second kind.
    """
    assert n > 0 and k > 0
    if k == 1:
        return [[[x for x in range(n)]]]
    elif k == n:
        return [[[x] for x in range(n)]]
    else:
        s_n1_k1 = stirling2(n - 1, k - 1)
        for i in range(len(s_n1_k1)):
            s_n1_k1[i].append([n - 1])

        tmp = stirling2(n - 1, k)
        k_s_n1_k = []
        for _ in range(k):
            k_s_n1_k += deepcopy(tmp)
        for i in range(len(tmp) * k):
            k_s_n1_k[i][i // len(tmp)] += [n - 1]

        return s_n1_k1 + k_s_n1_k
