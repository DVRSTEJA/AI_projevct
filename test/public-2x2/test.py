import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..')))

from slidingpuzzle import *
import pickle, random

def randboard(W, steps = 50):
    # This version ensures randboard is deterministic
    random.seed(123456)
    b = Board(W)
    st = State(b, [], 0)
    for step in range(steps):
        acts = sorted(st.board.actions())
        randact = random.sample(acts,1)[0]
        st = st.step(randact)
    return st.board

board = None # randboard(2)
with open("input", "rb") as f:
    board = pickle.load(f)
print(board.data)
answer = solve(board)
print(answer.board.data)
print(answer.moves)
with open('output', 'wb') as f:
  pickle.dump(answer.moves, f)
