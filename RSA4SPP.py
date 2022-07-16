#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/1 9:34
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com.com
# @File    : RSA4SPP.py
# @Statement : The ripple-spreading algorithm for the shortest path problem
# @Reference : Hu X B, Wang M, Leeson M S, et al. Deterministic agent-based path optimization by mimicking the spreading of ripples[J]. Evolutionary Computation, 2016, 24(2): 319-346.
import copy


def find_neighbor(network):
    """
    Find the neighbor of each node
    :param network:
    :return: {node 1: [the neighbor nodes of node 1], ...}
    """
    nn = len(network)
    neighbor = []
    for i in range(nn):
        neighbor.append(list(network[i].keys()))
    return neighbor


def find_speed(network, neighbor):
    """
    Find the ripple-spreading speed
    :param network:
    :param neighbor:
    :return:
    """
    speed = 1e10
    for i in range(len(network)):
        for j in neighbor[i]:
            speed = min(speed, network[i][j])
    return speed


def main(network, source, destination):
    """
    The ripple-spreading algorithm for the shortest path problem
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param source: the source node
    :param destination: the destination node
    :return:
    """
    # Step 1. Initialization
    nn = len(network)  # node number
    neighbor = find_neighbor(network)  # the neighbor set
    v = find_speed(network, neighbor)  # the ripple-spreading speed
    t = 0  # simulated time index
    nr = 0  # the current number of ripples - 1
    epicenter_set = []  # epicenter set
    radius_set = []  # radius set
    # length_set = []  # length set
    path_set = []  # path set
    active_set = []  # the set containing all active ripples
    omega = {}  # the set that records the ripple generated at each node
    for node in range(nn):
        omega[node] = -1

    # Step 2. Initialize the first ripple
    epicenter_set.append(source)
    radius_set.append(0)
    # length_set.append(0)
    path_set.append([source])
    active_set.append(nr)
    omega[source] = nr
    nr += 1

    # Step 3. The main loop
    while omega[destination] == -1:

        # Step 3.1. If there is feasible solution
        if not active_set:
            print('No feasible solution!')
            return []

        # Step 3.2. Time updates
        t += 1
        incoming_ripples = {}

        for ripple in active_set:

            # Step 3.3. Active ripples spread out
            radius_set[ripple] += v

            # Step 3.4. New incoming ripples
            epicenter = epicenter_set[ripple]
            path = path_set[ripple]
            radius = radius_set[ripple]
            # length = length_set[ripple]
            for node in neighbor[epicenter]:
                if omega[node] == -1:  # the node is unvisited
                    temp_length = network[epicenter][node]
                    if temp_length <= radius < temp_length + v:
                        temp_path = copy.deepcopy(path)
                        temp_path.append(node)
                        if node in incoming_ripples.keys():
                            incoming_ripples[node].append({
                                'path': temp_path,
                                'radius': radius - temp_length,
                                # 'length': length + temp_length,
                            })
                        else:
                            incoming_ripples[node] = [{
                                'path': temp_path,
                                'radius': radius - temp_length,
                                # 'length': length + temp_length
                            }]

        # Step 3.5. Generate new ripples
        for node in incoming_ripples.keys():
            new_ripple = sorted(incoming_ripples[node], key=lambda x: x['radius'], reverse=True)[0]
            path_set.append(new_ripple['path'])
            epicenter_set.append(node)
            radius_set.append(new_ripple['radius'])
            active_set.append(nr)
            omega[node] = nr
            # length_set.append(new_ripple['length'])
            nr += 1

        # Step 3.6. Active -> inactive
        remove_ripple = []
        for ripple in active_set:
            epicenter = epicenter_set[ripple]
            flag_inactive = True
            for node in neighbor[epicenter]:
                if omega[node] == -1:
                    flag_inactive = False
                    break
            if flag_inactive:
                remove_ripple.append(ripple)
        for ripple in remove_ripple:
            active_set.remove(ripple)

    # Step 4. Select the best path
    best_ripple = omega[destination]
    return path_set[best_ripple]


if __name__ == '__main__':
    test_network = {
        0: {1: 62, 2: 44, 3: 67},
        1: {0: 62, 2: 32, 4: 52},
        2: {0: 44, 1: 33, 3: 32, 4: 52},
        3: {0: 67, 2: 32, 4: 54},
        4: {1: 52, 2: 52, 3: 54}
    }
    source = 0
    destination = 4
    print(main(test_network, source, destination))
