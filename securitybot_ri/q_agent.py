# Q-Learning Agent for the Security Bot
# This is Kenobi's brain! Where all the learning happens!
import random
import pickle  # for saving Kenobi's brain to disk
import os

class QLearningAgent:
    # The brains behind Kenobi's food-finding abilities!
    def __init__(self, learning_rate=0.1, discount=0.95, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        """
        Q-Learning agent for the robot.

        Args:
            learning_rate: How fast the agent learns (0-1)
            discount: How much future rewards matter (0-1)
            epsilon: Exploration rate (starts high, decays over time)
            epsilon_decay: How fast epsilon decreases
            epsilon_min: Minimum exploration rate
        """
        self.q_table = {}  # Maps state -> [Q-values for each action] - Kenobi's memory!
        self.lr = learning_rate  # how fast Kenobi learns from mistakes
        self.discount = discount  # how much Kenobi cares about future rewards
        self.epsilon = epsilon  # how often Kenobi tries random stuff
        self.epsilon_decay = epsilon_decay  # Kenobi gets less random over time
        self.epsilon_min = epsilon_min  # Kenobi always stays a little curious!
        self.actions = [0, 1, 2, 3]  # up, down, left, right - Kenobi's movement options!

    def get_q_values(self, state):
        """Get Q-values for a state, initializing if needed."""
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0, 0.0, 0.0]
        return self.q_table[state]

    def choose_action(self, state):
        """
        Choose action using epsilon-greedy policy.
        Explores randomly with probability epsilon, otherwise picks best action.
        Kenobi decides: should I try something new or stick with what works?
        """
        if random.random() < self.epsilon:
            # Explore: random action - Kenobi is feeling adventurous!
            return random.choice(self.actions)
        else:
            # Exploit: best known action - Kenobi uses his training!
            q_values = self.get_q_values(state)
            max_q = max(q_values)
            # If multiple actions have same Q-value, pick randomly among them
            # Kenobi flips a coin when he's equally confident about multiple moves
            best_actions = [a for a, q in enumerate(q_values) if q == max_q]
            return random.choice(best_actions)

    def learn(self, state, action, reward, next_state, done):
        """
        Update Q-table using the Q-learning formula:
        Q(s,a) = Q(s,a) + lr * (reward + discount * max(Q(s')) - Q(s,a))
        This is where Kenobi's brain gets updated after each experience!
        """
        q_values = self.get_q_values(state)  # what did Kenobi think before?
        old_q = q_values[action]

        if done:
            # Terminal state - no future rewards (Kenobi hit a wall, ouch!)
            target = reward
        else:
            # Future reward from best action in next state
            # Kenobi thinks ahead: "if I keep making good moves, I'll get more food!"
            next_q_values = self.get_q_values(next_state)
            target = reward + self.discount * max(next_q_values)

        # Update Q-value - Kenobi adjusts his thinking based on what happened!
        # If the move was good, increase Q. If bad, decrease Q.
        q_values[action] = old_q + self.lr * (target - old_q)

    def decay_epsilon(self):
        """Reduce exploration rate over time."""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def save(self, filename="q_table.pkl"):
        """Save Q-table to file."""
        with open(filename, "wb") as f:
            pickle.dump({
                "q_table": self.q_table,
                "epsilon": self.epsilon
            }, f)
        print(f"Saved Q-table ({len(self.q_table)} states) to {filename}")

    def load(self, filename="q_table.pkl"):
        """Load Q-table from file."""
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                data = pickle.load(f)
                self.q_table = data["q_table"]
                self.epsilon = data["epsilon"]
            print(f"Loaded Q-table ({len(self.q_table)} states) from {filename}")
            return True
        return False
