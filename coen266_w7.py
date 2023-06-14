import copy
import math
import random


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


class FiveStateGridworldMDP:
  state_set = ["A", "B", "C", "D", "E", "exited"]

  def reward(self, state, action, state_prime):
    if action == "exit" and state == "A":
      return -10
    elif action == "exit" and state == "D":
      return 10
    else:
      return -1

  def transition_prob(self, state, action, state_prime):
    probs = {
      ("B", "right", "C"): 1,
      ("E", "up", "C"): 1,
      ("C", "right", "D"): 0.8,
      ("C", "right", "A"): 0.1,
      ("C", "right", "E"): 0.1,
      ("C", "left", "B"): 0.8,
      ("C", "left", "A"): 0.1,
      ("C", "left", "E"): 0.1,
      ("C", "up", "A"): 0.8,
      ("C", "up", "B"): 0.1,
      ("C", "up", "D"): 0.1,
      ("C", "down", "E"): 0.8,
      ("C", "down", "B"): 0.1,
      ("C", "down", "D"): 0.1,
      ("A", "exit", "exited"): 1,
      ("D", "exit", "exited"): 1,
    }
    return probs.get((state, action, state_prime), 0)

  def successor_states(self, state, action):
    if state == "B":
      return ["C"]
    elif state == "E":
      return ["C"]
    elif state == "C":
      return ["A", "B", "D", "E"]
    elif state == "A":
      return ["exited"]
    elif state == "D":
      return ["exited"]
    else:
      return []

  def possible_actions(self, state):
    if state == "B":
      return ["right"]
    elif state == "E":
      return ["up"]
    elif state == "C":
      return ["up", "right", "down", "left"]
    elif state == "A":
      return ["exit"]
    elif state == "D":
      return ["exit"]
    else:
      return []


def weighted_random(probs):
  random_val = random.uniform(0, 1)
  cumulative_val = 0
  for item, prob in probs.items():
    cumulative_val += prob
    if cumulative_val > random_val:
      return item


def run_episodes(mdp, num_episodes, sample_limit=100):
  episodes = []
  for i in range(num_episodes):
    # run the episode to completion, recording transitions seen (s, a, s', r)
    episode = []
    init_state = random.choice(mdp.state_set)
    state = init_state
    while len(episode) < sample_limit:
      actions = mdp.possible_actions(state)
      if not actions:
        break
      action = random.choice(mdp.possible_actions(state))
      probs = {}
      for state_prime in mdp.successor_states(state, action):
        probs[state_prime] = mdp.transition_prob(state, action, state_prime)
      state_prime = weighted_random(probs)
      episode.append((state, action, state_prime, mdp.reward(state, action, state_prime)))
      state = state_prime
    episodes.append(episode)
    print("EPISODE", i, episode)
  return episodes


# your code here

def find_value_function(mdp, num_iterations, learned_transition_probs, learned_rewards):
  V = {} # Value Dictionary
  for state in mdp.state_set:
    V[state] = 0
    
  for _ in range(num_iterations):
    V_prime = V.copy()
        
    for state in mdp.state_set:
      if not mdp.possible_actions(state):
        continue   
      action_values = []
            
      for action in mdp.possible_actions(state):
        Q = 0 # Q-state variable
        for state_prime in mdp.successor_states(state, action):
          p = learned_transition_probs.get((state, action, state_prime), 0.0)  #mdp.transition_prob(state, action, state_prime) # possible action value
          r = learned_rewards.get((state, action, state_prime), 0.0) #mdp.reward(state, action, state_prime) # reward value
          Q += p * (r + mdp.discount_factor * V[state_prime])
                
        action_values.append(Q)
            
      V_prime[state] = max(action_values)
        
    V = V_prime

  return V

def extract_policy(mdp, value_function, learned_transition_probs, learned_rewards):
  policy = {} # Policy Dictionary
    
  for state in mdp.state_set:
    best_action = None
    highest_value = float('-inf')
        
    for action in mdp.possible_actions(state):
      Q = 0 # Q-state variable
      for state_prime in mdp.successor_states(state, action):
        p = learned_transition_probs.get((state, action, state_prime), 0.0) #mdp.transition_prob(state, action, state_prime) # possible action value
        r = learned_rewards.get((state, action, state_prime), 0.0) #mdp.reward(state, action, state_prime) # reward value
        Q += p * (r + mdp.discount_factor * value_function[state_prime])
            
        if Q > highest_value:
          best_action = action
          highest_value = Q
        
    policy[state] = best_action
    
  return policy

def learn_model(mdp, episodes):
  learned_transition_probs = {}
  learned_rewards = {}
  transition_counts = {}
  reward_accumulators = {}

  for episode in episodes:
    for sample in episode:
      state, action, next_state, reward = sample
      key = (state, action, next_state)
      transition_counts[key] = transition_counts.get(key, 0) + 1
      if key in reward_accumulators:
        reward_accumulators[key] += reward
      else:
        reward_accumulators[key] = reward

  for key, count in transition_counts.items():
    state, action, next_state = key
    learned_transition_probs[key] = count / sum([c for k, c in transition_counts.items() if k[:2] == (state, action)])

    learned_rewards[key] = reward_accumulators[key] / transition_counts[key]

  return learned_transition_probs, learned_rewards

def learn_q_table(mdp, episodes, learning_rate):
  q_table = {}

  for state in mdp.state_set:
    for action in mdp.possible_actions(state):
      q_table[(state, action)] = 0

  for episode in episodes:
    for s, a, s_prime, r in episode:
      max_q = max([q_table.get((s_prime, a_prime)) for a_prime in mdp.possible_actions(s_prime)] or [0])

      q_table[(s, a)] = q_table[(s, a)] + learning_rate * ((r + mdp.discount_factor * max_q) - q_table[(s, a)])

      s = s_prime

  return q_table


def extract_policy_from_q_table(mdp, q_table):
  policy = {}

  for state in mdp.state_set:
    best_action = "None"
    for action in mdp.possible_actions(state):
      if q_table.get((state, action), 0)>q_table.get((state, best_action), 0):
        best_action = action
        policy[state] = best_action

  return policy


# to run model-based RL
mdp = FiveStateGridworldMDP()
num_episodes = 1000
mdp.discount_factor = 0.9
episodes = run_episodes(mdp, 1000)
(learned_transition_probs, learned_rewards) = learn_model(mdp, episodes)
value_function = find_value_function(mdp, num_episodes, learned_transition_probs, learned_rewards)
policy = extract_policy(mdp, value_function, learned_transition_probs, learned_rewards)
print("MDP    :", mdp.__class__.__name__)
print("T^     :", learned_transition_probs)
print("R^     :", learned_rewards)
print("VALUE  :", value_function)
print("POLICY :", policy)


# to run Q-learning
mdp = FiveStateGridworldMDP()
num_episodes = 1000
learning_rate = 1
mdp.discount_factor = 0.9
episodes = run_episodes(mdp, 1000)
q_table = learn_q_table(mdp, episodes, learning_rate)
policy = extract_policy_from_q_table(mdp, q_table)
print("MDP    :", mdp.__class__.__name__)
print("QTABLE :", q_table)
print("POLICY :", policy)

