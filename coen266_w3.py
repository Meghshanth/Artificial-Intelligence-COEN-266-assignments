import collections
import copy
import heapq
import math
import random


class Node:
  def __init__(self, state, action, cost, parent):
    self.state = state
    self.action = action
    self.cost = cost
    self.parent = parent

  def full_path(self):
    path = []
    node = self
    while node.parent:
      path.append(node)
      node = node.parent
    path.reverse()
    return path


class Environment:
  def __init__(self):
    self.nodes_expanded = 0

  def is_goal(self, node):
    self.nodes_expanded += 1
    return self.goal_test(node.state)

  def get_successors(self, node):
    state = node.state
    return [
      Node(self.successor(state, action), action, cost, node)
      for (action, cost) in self.get_actions(state)
    ]

  def heuristic(self, node):
    return self.evaluate(node.state)


class VacuumEnvironment(Environment):
  def init_state(self):
    return {"agent_loc": 0, "tiles": ["dirty"] * 5}

  def goal_test(self, state):
    for tile in state["tiles"]:
      if tile != "clean":
        return False
    return True

  def get_actions(self, state):
    return [("left", 1), ("right", 1), ("suck", 1)]

  def successor(self, state, action):
    next_state = copy.deepcopy(state)
    agent_loc = state["agent_loc"]
    if agent_loc < len(state["tiles"]) - 1 and action == "right":
      next_state["agent_loc"] += 1
    elif agent_loc > 0 and action == "left":
      next_state["agent_loc"] -= 1
    elif state["tiles"][agent_loc] == "dirty" and action == "suck":
      next_state["tiles"][agent_loc] = "clean"
    return next_state

  def evaluate(self, state):
    return sum([(1 if tile == "dirty" else 0) for tile in state["tiles"]])


class SmallRomanianPathfindingEnvironment(Environment):
  def init_state(self):
    return "Sibiu"

  def goal_test(self, state):
    return state == "Bucharest"

  def get_actions(self, state):
    if state == "Sibiu":
      return [("Fagaras", 99), ("Rimnicu Vilcea", 80), ("Atlantis", 1)]
    elif state == "Fagaras":
      return [("Sibiu", 99), ("Bucharest", 211)]
    elif state == "Rimnicu Vilcea":
      return [("Sibiu", 80), ("Pitesti", 97)]
    elif state == "Pitesti":
      return [("Rimnicu Vilcea", 97), ("Bucharest", 101)]
    elif state == "Bucharest":
      return [("Fagaras", 211), ("Pitesti", 101)]
    elif state == "Atlantis":
      return [("Bucharest", 10000)]
    else:
      return []

  def successor(self, state, action):
    return action

  def evaluate(self, state):
    return {
      "Sibiu": 253,
      "Fagaras": 176,
      "Rimnicu Vilcea": 193,
      "Pitesti": 100,
      "Atlantis": 10000,
      "Bucharest": 0
    }[state]


class IncrementalNQueensEnvironment(Environment):
  def locs_diagonal(_, loc1, loc2):
    row_diff = abs(loc1[0] - loc2[0])
    col_diff = abs(loc1[1] - loc2[1])
    return row_diff == col_diff

  def visualize(self, state):
    printable_state = ""
    for row in range(0, self.size):
      for col in range(0, self.size):
        printable_cell = "Q" if (row, col) in state else "."
        printable_state += printable_cell
      printable_state += "\n"
    return printable_state

  def init_state(self):
    self.size = 6
    return []

  def goal_test(self, state):
    if len(state) != self.size:
      return False
    for piece_loc in state:
      (x, y) = piece_loc
      for other_loc in state:
        if other_loc == piece_loc:
          continue
        if other_loc[0] == x or other_loc[1] == y or self.locs_diagonal(piece_loc, other_loc):
          return False
    return True

  def get_actions(self, state):
    if len(state) < self.size:
      row = len(state)
      return [((row, col), 1) for col in range (0, self.size)]
    return []

  def successor(self, state, action):
    next_state = copy.deepcopy(state)
    next_state.append(action)
    return next_state

  def evaluate(self, state):
    occupied_rows = set()
    occupied_cols = set()
    conflicts = 0
    for piece_loc in state:
      if piece_loc[0] in occupied_rows:
        conflicts += 1
      if piece_loc[1] in occupied_cols:
        conflicts += 1
      occupied_rows.add(piece_loc[0])
      occupied_cols.add(piece_loc[1])
    return conflicts


# YOUR AGENT FUNCTIONS GO HERE
def greedy_search_agent(root, env):
    frontier = []
    heapq.heappush(frontier, (0, 0, root))
    visited = set()
    tiebreaker = 0
    while frontier:
        node = heapq.heappop(frontier)[2]
        visited.add(str(node.state))
        if env.is_goal(node):
            return node
        for successor in env.get_successors(node):
            if str(successor.state) in visited:
                continue
            tiebreaker += 1
            heapq.heappush(frontier, (env.heuristic(successor), tiebreaker, successor))

  #return 0

def a_star_agent(root, env):
    frontier = []
    heapq.heappush(frontier, (0, 0, root))
    best_cost = {}
    best_cost[str(root. state)] = 0
    tiebreaker = 0
    while frontier:
        node = heapq.heappop(frontier)[2]
        if env.is_goal(node):
            return node
        for successor in env. get_successors (node):
            prev_best_cost = best_cost.get(str(successor.state), math.inf)
            new_best_cost = best_cost[str (node.state)] + successor.cost
            if new_best_cost < prev_best_cost:
                tiebreaker += 1
                best_cost [str(successor.state)] = new_best_cost
                heapq.heappush(frontier, (new_best_cost + env. heuristic(successor), tiebreaker, successor))

 # return 0

def main():
  env = VacuumEnvironment() # change this line to switch environments
  root = Node(env.init_state(), None, 0, None)
  agent = greedy_search_agent # change this line to switch agent functions
  goal = agent(root, env)
  path = goal.full_path()
  print("ENV   :", env.__class__.__name__)
  print("AGENT :", agent.__name__)
  print("PATH  :", [(node.action, node.cost) for node in path])
  print("COST  :", sum([node.cost for node in path]))
  print("NODES :", env.nodes_expanded)


if __name__ == "__main__":
  main()