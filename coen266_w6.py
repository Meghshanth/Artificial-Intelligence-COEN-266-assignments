class OverheatingCarMDP:
  state_set = ["cool", "warm", "overheated"]

  def reward(self, state, action, state_prime):
    if state_prime == "overheated":
      return -10
    elif action == "slow":
      return 1
    elif action == "fast":
      return 2
    else:
      return 0

  def transition_prob(self, state, action, state_prime):
    probs = {
      ("cool", "slow", "cool"): 1,
      ("cool", "fast", "cool"): 0.5,
      ("cool", "fast", "warm"): 0.5,
      ("warm", "slow", "cool"): 0.5,
      ("warm", "slow", "warm"): 0.5,
      ("warm", "fast", "overheated"): 1
    }
    return probs.get((state, action, state_prime), 0)

  def successor_states(self, state, action):
    successors = {
      ("cool", "slow"): ["cool"],
      ("cool", "fast"): ["cool", "warm"],
      ("warm", "slow"): ["cool", "warm"],
      ("warm", "fast"): ["overheated"]
    }
    return successors.get((state, action), [])

  def possible_actions(self, state):
    return [] if state == "overheated" else ["slow", "fast"]


class SimpleLeftRightMDP:
  state_set = [0, 1, 2, 3, 4, "exited"]

  def reward(self, state, action, state_prime):
    if state == 0 and action == "exit":
      return 10
    elif state == 4 and action == "exit":
      return 1
    else:
      return 0

  def transition_prob(self, state, action, state_prime):
    if state > 0 and action == "left" and state_prime == state - 1:
      return 1
    elif state < 4 and action == "right" and state_prime == state + 1:
      return 1
    elif state in [0, 4] and action == "exit" and state_prime == "exited":
      return 1
    else:
      return 0

  def successor_states(self, state, action):
    if state > 0 and action == "left":
      return [state - 1]
    elif state < 4 and action == "right":
      return [state + 1]
    elif state in [0, 4] and action == "exit":
      return ["exited"]
    else:
      return []

  def possible_actions(self, state):
    if state in [0, 4]:
      return ["exit"]
    if state == "exited":
      return []
    actions = []
    if state < 4:
      actions.append("right")
    if state > 0:
      actions.append("left")
    return actions


class DoubleBanditsMDP:
  state_set = ["won", "lost"]

  def reward(self, state, action, state_prime):
    if action == "red" and state_prime == "won":
      return 2
    elif action == "red" and state_prime == "lost":
      return 0
    elif action == "blue":
      return 1
    else:
      return 0

  def transition_prob(self, state, action, state_prime):
    if action == "red" and state_prime == "won":
      return 0.75
    elif action == "red" and state_prime == "lost":
      return 0.25
    elif action == "blue" and state_prime == "won":
      return 1
    else:
      return 0

  def successor_states(self, state, action):
    if action == "red":
      return ["won", "lost"]
    elif action == "blue":
      return ["won"]
    else:
      return []

  def possible_actions(self, state):
    return ["red", "blue"]


def find_value_function(mdp, num_iterations):
  pass # your code here


def extract_policy(mdp, value_function):
  pass # your code here


mdp = SimpleLeftRightMDP() # change this line to change which MDP you're solving
mdp.discount_factor = 0.9 # change this line to change the discount factor (gamma)
num_iterations = 10 # change this line to change how many iterations of the Bellman update you perform
value_function = find_value_function(mdp, num_iterations)
policy = extract_policy(mdp, value_function)
print("MDP    :", mdp.__class__.__name__)
print("VALUE  :", value_function)
print("POLICY :", policy)
