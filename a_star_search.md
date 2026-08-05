# A* Search Algorithm in Python

This project implements the **A\* (A-Star) Search Algorithm** using Python. It reads a graph from an `input.txt` file, calculates the shortest path using the **Euclidean Distance heuristic**, and prints the solution path and total cost.

---

## Python Code (`a_star_search.py`)

```python
import math
from queue import PriorityQueue

# 1. Data Structures for Graph
coords = {}   # node id is the key, (x, y) as value
adjlist = {}  # node id is the key, list of (neighbor, cost) as value

# 2. Reading input.txt
with open('input.txt', 'r') as f:
    # Read Vertices
    line = f.readline().strip()
    if not line:
        V = 0
    else:
        V = int(line)

    for _ in range(V):
        strs = f.readline().split()
        if strs:
            nid, x, y = strs[0], int(strs[1]), int(strs[2])
            coords[nid] = (x, y)
            adjlist[nid] = []

    # Read Edges
    line = f.readline().strip()
    if line:
        E = int(line)
        for _ in range(E):
            strs = f.readline().split()
            if strs:
                u, v, cost = strs[0], strs[1], int(strs[2])
                adjlist[u].append((v, cost))

    # Read Start and Goal Nodes
    startnode = f.readline().strip()
    goalnode = f.readline().strip()

# 3. Heuristic Function
def heuristic(node, goal):
    x1, y1 = coords[node]
    x2, y2 = coords[goal]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# 4. State Class
class State:
    def __init__(self, node_id, parent, g, f):
        self.node_id = node_id
        self.parent = parent
        self.g = g
        self.f = f

    def __lt__(self, other):
        return self.f < other.f

# 5. A* Search
def a_star_search(start, goal):
    minQ = PriorityQueue()

    h_start = heuristic(start, goal)
    start_state = State(start, None, 0, h_start)
    minQ.put(start_state)

    while not minQ.empty():
        curr_state = minQ.get()
        u = curr_state.node_id

        if u == goal:
            return curr_state

        for v, cost in adjlist.get(u, []):
            g_new = curr_state.g + cost
            h_new = heuristic(v, goal)
            f_new = g_new + h_new

            new_state = State(v, curr_state, g_new, f_new)
            minQ.put(new_state)

    return None

# 6. Print Result
result_state = a_star_search(startnode, goalnode)

if result_state:
    path = []
    temp = result_state
    total_cost = result_state.g

    while temp is not None:
        path.append(temp.node_id)
        temp = temp.parent

    path.reverse()

    print(f"Solution path: {' -> '.join(path)}")
    print(f"Solution cost: {total_cost}")
else:
    print("No path found.")
```

---

## Input File (`input.txt`)

```text
6
S 6 0
A 6 0
B 1 0
C 2 0
D 1 0
G 0 0
9
S A 1
S C 2
S D 4
A B 2
B A 2
B G 1
C S 2
C G 4
D G 4
S
G
```

---

## Input Format

### Vertices

```
<number_of_vertices>
node_id x_coordinate y_coordinate
...
```

Example:

```text
6
S 6 0
A 6 0
B 1 0
C 2 0
D 1 0
G 0 0
```

---

### Edges

```
<number_of_edges>
source destination cost
...
```

Example:

```text
9
S A 1
S C 2
S D 4
A B 2
B A 2
B G 1
C S 2
C G 4
D G 4
```

---

### Start and Goal Node

```text
S
G
```

---

## Heuristic Function

The heuristic uses the **Euclidean Distance**.

$$
h(n)=\sqrt{(x_1-x_2)^2+(y_1-y_2)^2}
$$

Where:

- \(x_1, y_1\) = Coordinates of the current node
- \(x_2, y_2\) = Coordinates of the goal node
- \(h(n)\) = Estimated distance from the current node to the goal

---

## Evaluation Function

\[
f(n)=g(n)+h(n)
\]

where:

- **g(n)** = Cost from Start Node to Current Node
- **h(n)** = Estimated Cost from Current Node to Goal
- **f(n)** = Total Estimated Cost

---

## Output

```text
Solution path: S -> A -> B -> G
Solution cost: 4
```

---

## How to Run

```bash
python a_star_search.py
```


## Author

**Arafat Khan Pathan**
