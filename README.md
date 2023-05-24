### The Ripple-Spreading Algorithm for the Shortest Path Problem

##### Reference: Hu X B, Wang M, Leeson M S, et al. Deterministic agent-based path optimization by mimicking the spreading of ripples[J]. Evolutionary Computation, 2016, 24(2): 319-346.

| Variables     | Meaning                                                      |
| ------------- | ------------------------------------------------------------ |
| network       | Dictionary, {node1: {node2: length, node3: length, ...}, ...} |
| source        | The source node                                              |
| destination   | The destination node                                         |
| nn            | The number of nodes                                          |
| neighbor      | Dictionary, {node1: [the neighbor nodes of node1], ...}      |
| v             | The ripple-spreading speed (i.e., the minimum length of arcs) |
| t             | The simulated time index                                     |
| nr            | The number of ripples - 1                                    |
| epicenter_set | List, the epicenter node of the ith ripple is epicenter_set[i] |
| path_set      | List, the path of the ith ripple from the source node to node i is path_set[i] |
| radius_set    | List, the radius of the ith ripple is radius_set[i]          |
| active_set    | List, active_set contains all active ripples                 |
| Omega         | Dictionary, Omega[n] = i denotes that ripple i is generated at node n |

#### Example (RSA4SPP.py)

![](https://github.com/Xavier-MaYiMing/The-ripple-spreading-algorithm-for-the-shortest-path-problem/blob/main/SPP_example.png)

```python
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
```

##### Output: [0, 2, 4]

##### The RSA.py was written in class.
