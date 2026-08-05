import math 
from queue import PriorityQueue

# 1. Data Structures for Graph
coords = {}   # node id is the key, (x, y) as value
adjlist = {}  # node id is the key, list of (neighbor, cost) as value

# 2. Reading input.txt based on faculty instructions [1, 2, 7]
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

# 3. Heuristic Function: Euclidean Distance [1, 3]
def heuristic(node, goal):
    x1, y1 = coords[node]
    x2, y2 = coords[goal]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# 4. State Class to maintain search status [4]
class State:
    def __init__(self, node_id, parent, g, f):
        self.node_id = node_id
        self.parent = parent
        self.g = g
        self.f = f

    # Custom comparison for PriorityQueue to order by 'f' [5, 10]
    def __lt__(self, other):
        return self.f < other.f

# 5. A* Search Implementation [5, 6, 11]
def a_star_search(start, goal):
    minQ = PriorityQueue()
    
    # Initialize start state [4]
    h_start = heuristic(start, goal)
    start_state = State(start, None, 0, h_start)
    minQ.put(start_state)

    while not minQ.empty():
        # Extract node with minimum f value [6]
        curr_state = minQ.get()
        u = curr_state.node_id

        # Goal Test [6]
        if u == goal:
            return curr_state

        # Expand neighbors [6, 11]
        for v, cost in adjlist.get(u, []):
            g_new = curr_state.g + cost
            h_new = heuristic(v, goal)
            f_new = g_new + h_new
            
            new_state = State(v, curr_state, g_new, f_new)
            minQ.put(new_state)
            
    return None

# 6. Backtracking and Output [2, 6]
result_state = a_star_search(startnode, goalnode)

if result_state:
    path = []
    temp = result_state
    total_cost = result_state.g
    
    # Backtrack to find path [6, 12]
    while temp is not None:
        path.append(temp.node_id)
        temp = temp.parent
    
    path.reverse()
    print(f"Solution path: {' – '.join(path)}")
    print(f"Solution cost: {total_cost}")
else:
    print("No path found.")





 # input.txt file

6
S 6 0      # s = node, (x, y) = (6, 0)    node and cordinate
A 6 0
B 1 0
C 2 0
D 1 0
G 0 0
9
S A 1     # eadge and cost
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
