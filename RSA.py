#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/23 16:26
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : RSA.py
# @Statement : The ripple-spreading algorithm (RSA) for the shortest path problem
# @Reference : Hu X B, Wang M, Leeson M S, et al. Deterministic agent-based path optimization by mimicking the spreading of ripples[J]. Evolutionary Computation, 2016, 24(2): 319-346.
from numpy import inf


class Ripple:
    def __init__(self, epicenter, radius, path, length):
        self.epicenter = epicenter
        self.radius = radius
        self.path = path
        self.length = length

    def spread(self, v):
        self.radius += v


def find_neighbors(network):
    # find the neighbors of each node
    neighbor = []
    for i in network.keys():
        neighbor.append(list(network[i].keys()))
    return neighbor


def find_speed(network, neighbor):
    # find the ripple-spreading speed
    v = inf
    for i in network.keys():
        for j in neighbor[i]:
            v = min(v, network[i][j])
    return v


def main(network, source, destination):
    """
    The main function
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param source: the source node
    :param destination: the destination node
    :return:
    """
    # Step 1. Initialization
    nn = len(network)  # node number
    neighbor = find_neighbors(network)
    v = find_speed(network, neighbor)
    nr = 0  # the number of ripples - 1
    ripples = []  # ripple set
    active_ripples = []  # active ripple set
    omega = {}  # the set that records the ripple generated at each node
    for node in range(nn):
        omega[node] = -1

    # Step 2. Initialize the first ripple
    ripples.append(Ripple(source, 0, [source], 0))
    active_ripples.append(nr)
    omega[source] = nr
    nr += 1

    # Step 3. The main loop
    while omega[destination] == -1:

        # Step 3.1. If there is a feasible solution?
        if not ripples:
            print('No feasible solution!')
            return {}

        # Step 3.2. Active ripples spread out
        incoming_ripples = {}
        for r in active_ripples:
            ripple = ripples[r]
            ripple.spread(v)
            for node in neighbor[ripple.epicenter]:
                temp_length = network[ripple.epicenter][node]
                if omega[node] == -1 and temp_length <= ripple.radius:
                    new_path = ripple.path.copy()
                    new_path.append(node)
                    if node in incoming_ripples:
                        incoming_ripples[node].append(Ripple(node, ripple.radius - temp_length, new_path, ripple.length + temp_length))
                    else:
                        incoming_ripples[node] = [Ripple(node, ripple.radius - temp_length, new_path, ripple.length + temp_length)]

        # Step 3.3. Generate new ripples
        for node in incoming_ripples.keys():
            new_ripple = sorted(incoming_ripples[node], key=lambda x: x.radius, reverse=True)[0]
            ripples.append(new_ripple)
            active_ripples.append(nr)
            omega[node] = nr
            nr += 1

        # Step 3.4. Active -> inactive
        remove_ripples = []
        for r in active_ripples:
            ripple = ripples[r]
            flag_inactive = True
            for node in neighbor[ripple.epicenter]:
                if omega[node] == -1:
                    flag_inactive = False
                    break
            if flag_inactive:
                remove_ripples.append(r)
        for r in remove_ripples:
            active_ripples.remove(r)

    # Step 4. Select the best path
    best_ripple = ripples[omega[destination]]
    return best_ripple.path
    # return {'path': best_ripple.path, 'length': best_ripple.length}


if __name__ == '__main__':
    test_network = {
        0: {1: 62, 2: 44, 3: 67},
        1: {0: 62, 2: 32, 4: 52},
        2: {0: 44, 1: 33, 3: 32, 4: 52},
        3: {0: 67, 2: 32, 4: 54},
        4: {1: 52, 2: 52, 3: 54}
    }
    s = 0
    d = 4
    print(main(test_network, s, d))
