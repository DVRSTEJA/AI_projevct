#
# Project 0 for AI: CS 460/660/760
# Complete a sliding puzzle solver using search with heuristics
#
# Check for instances of "TODO" in the starter below and get it working using BFS first.
# Then see what heuristics you can apply from Chapter 3 to make this faster.


import random, copy, queue

class Board:
    def __init__(self, W):
        # Sets up a WxW board in solved position
        self.W = W
        self.data = []
        self.pos = (0,0)
        next = 0
        for i in range(self.W):
            self.data.append([])
            for j in range(self.W):
                self.data[-1].append(next)
                next += 1
    def __eq__(self, other):
        for i in range(self.W):
            for j in range(self.W):
                if self.data[i][j] != other.data[i][j]: return False
        return True
    def __hash__(self):
        h = 0
        for i in range(self.W):
            for j in range(self.W):
                h *= 3
                h ^= hash(self.data[i][j]);
        return h
    def actions(self):
        i,j = self.pos
        a = frozenset()
        if i > 0: a |= {"up"}
        if i < self.W-1: a |= {"down"}
        if j > 0: a |= {"left"}
        if j < self.W-1: a |= {"right"}
        return a
    def step(self, action):
        # Assuming action is applicable, return successor board
        i0, j0 = self.pos
        i1, j1 = i0, j0
        if action == "up": i1 -= 1
        elif action == "down": i1 += 1
        elif action == "left": j1 -= 1
        elif action == "right": j1 += 1
        nextboard = copy.deepcopy(self)
        nextboard.data[i0][j0] = nextboard.data[i1][j1]
        nextboard.data[i1][j1] = 0
        nextboard.pos = (i1,j1)
        return nextboard
    def goal(self):
        next = 0
        for i in range(self.W):
            for j in range(self.W):
                if self.data[i][j] != next: return False
                next += 1
        return True

    
class State:
    def __init__(self, board, moves, pathcost):
        self.board = board
        self.moves = moves
        self.pathcost = pathcost
    def __eq__(self, other):
        if len(self.moves) != len(other.moves): return False
        for i in range(len(self.moves)):
            if self.moves[i] != other.moves[i]: return False
        return self.board == other.board and self.pathcost == other.pathcost
    def __hash__(self):
        h = 0
        for i in range(len(self.moves)):
            h *= 3
            h ^= hash(self.moves[i])
        return h ^ hash(self.board) ^ hash(self.pathcost)
    def __lt__(self, other):
        return self.eval() < other.eval()
    def step(self, act):
        return State(self.board.step(act), self.moves+[act], self.pathcost+1)
    def successors(self):
        successor_states = []
        for action in self.board.actions():
            successor_states.append(self.step(action))
        return successor_states
    def goal(self):
        return self.board.goal()
    def eval(self):
        return self.pathcost + manhattan_distance(self.board)


# Potentially useful helper for generating randomly permuted boards using State.step
def randomboard(W, steps = 50, seed = 0):
    random.seed(seed)
    b = Board(W)
    st = State(b, [], 0)
    for step in range(steps):
        acts = sorted(st.board.actions())
        randact = random.sample(acts,1)[0]
        st = st.step(randact)
    return st.board

def manhattan_distance(board):
    distance = 0
    for i in range(board.W):
        for j in range(board.W):
            value = board.data[i][j]
            if value != 0:
                target_row, target_col = divmod(value - 1, board.W)
                distance += abs(i - target_row) + abs(j - target_col)

    return distance    

def solve(startboard):
    # Create a priority queue for the frontier set
    frontier = queue.PriorityQueue()
    # Create a hashset for already-visited boards
    seenset = set()
    # Add a state for the starting board at pathcost==0
    start = State(startboard, [], 0)
    frontier.put(start)

    # Loop until the frontier is exhausted
    while not frontier.empty():
        current_state = frontier.get()

        if current_state.goal():
            return current_state

        if current_state.board in seenset:
            continue

        seenset.add(current_state.board)

        for action in current_state.board.actions():
            next_state = current_state.step(action)
            if next_state.board not in seenset:
                frontier.put(next_state)

    # Oops, no solution found
    return None
