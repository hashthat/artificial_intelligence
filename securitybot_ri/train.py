# Training script for the Q-Learning Security Bot
# Time to teach Kenobi how to find his snacks!
import tkinter as tk
from q_agent import QLearningAgent

# Import game environment (but don't start mainloop yet)
# Kenobi's training ground awaits!
import gui_main as game

# Kenobi's possible moves - WASD style but with numbers!
ACTION_NAMES = ["UP", "DOWN", "LEFT", "RIGHT"]

def show_optimal_demo(episodes=3, speed=100):
    """
    Demo the OPTIMAL policy - robot goes directly to food.
    This shows what the Q-learning agent SHOULD learn to do.
    Like showing Kenobi a video of a pro player before he tries!
    """
    print("\n=== OPTIMAL POLICY DEMO ===")
    print("Watch how the robot SHOULD behave:\n")

    for episode in range(1, episodes + 1):
        game.reset_game()  # fresh start for the demo!
        steps = 0

        while steps < 30:  # max 30 steps should be plenty for a 16x16 grid!
            # Use the optimal action (always moves toward food)
            # This is Kenobi on his best day - no mistakes!
            action = game.get_optimal_action()
            _, reward, done = game.step(action)
            steps += 1

            game.window.update()  # show the magic happening!
            game.window.after(speed)  # slow down so humans can see

            if done:  # uh oh, hit a wall somehow?
                break

            # Check if we got food (score increased means new food spawned)
            # Yummy! Kenobi found his snack!
            if reward == game.REWARD_FOOD:
                print(f"  Episode {episode}: Found food in {steps} steps!")
                break

        print(f"  Episode {episode}: Score {game.score} in {steps} steps")


def train(episodes=100, max_steps=30, visualize=True, speed=50):
    """
    Train the Q-learning agent.
    This is where Kenobi goes to school and learns to find food!
    """
    # Create Kenobi's brain - the Q-learning agent!
    agent = QLearningAgent(
        learning_rate=0.8,      # Learn VERY fast - Kenobi is a quick learner!
        discount=0.9,           # Future rewards matter - think ahead Kenobi!
        epsilon=0.1,            # Only 10% random moves - trust the reward signals!
        epsilon_decay=0.95,     # Get less random over time as Kenobi gets smarter
        epsilon_min=0.01        # Always keep a tiny bit of curiosity!
    )

    print(f"\n=== Starting Training: {episodes} episodes ===\n")
    print("Kenobi is entering the training arena!\n")

    total_scores = []  # keep track of how well Kenobi is doing!

    for episode in range(1, episodes + 1):
        game.reset_game()  # new episode, new chances to find food!
        state = game.get_simple_state()  # where's the food relative to Kenobi?
        steps = 0

        while steps < max_steps:  # don't let Kenobi wander forever!
            # Agent chooses action - what does Kenobi's brain say to do?
            action = agent.choose_action(state)

            # What SHOULD the action be? (for debugging Kenobi's choices)
            optimal = game.get_optimal_action()

            # Take action in environment - Kenobi makes his move!
            _, reward, done = game.step(action)
            next_state = game.get_simple_state()

            # Agent learns from this experience - updating Kenobi's brain!
            # This is where the magic happens!
            agent.learn(state, action, reward, next_state, done)

            state = next_state  # remember the new state
            steps += 1

            if visualize:  # show Kenobi moving around
                game.window.update()
                game.window.after(speed)

            if done:  # episode over (probably hit a wall, ouch!)
                break

        agent.decay_epsilon()  # Kenobi gets a bit less random each episode
        total_scores.append(game.score)  # how many foods did Kenobi find?

        # Print every episode for visibility
        if episode % 5 == 0:
            avg = sum(total_scores[-5:]) / 5
            print(f"Ep {episode:3d} | Avg Score: {avg:.1f} | Epsilon: {agent.epsilon:.2f}")

    # Show what the agent learned - peek inside Kenobi's brain!
    print("\n=== What Kenobi learned ===")
    print("This is Kenobi's decision table - his brain!")
    print("State -> Best Action (Q-values)")
    print("-" * 50)

    # Human readable state names so we can understand Kenobi's thinking!
    state_meanings = {
        (-1, -1): "Food is UP-LEFT",
        (-1, 0): "Food is UP",
        (-1, 1): "Food is UP-RIGHT",
        (0, -1): "Food is LEFT",
        (0, 0): "Food is HERE",
        (0, 1): "Food is RIGHT",
        (1, -1): "Food is DOWN-LEFT",
        (1, 0): "Food is DOWN",
        (1, 1): "Food is DOWN-RIGHT",
    }

    # Print out what Kenobi thinks is the best move for each situation!
    for state in sorted(agent.q_table.keys()):
        q_vals = agent.q_table[state]
        best_action = q_vals.index(max(q_vals))  # highest Q-value = best choice!
        meaning = state_meanings.get(state, str(state))
        print(f"  {meaning:20s} -> {ACTION_NAMES[best_action]:5s}  Q={[f'{q:.1f}' for q in q_vals]}")

    agent.save()  # save Kenobi's brain to disk for later!
    print("\nKenobi's brain has been saved to q_table.pkl!")
    return agent


def test(agent, episodes=5, speed=100):
    """Test the trained agent (no exploration).
    Time to see if Kenobi actually learned something!
    """
    print(f"\n=== Testing Kenobi's Skills ===\n")
    print("No more random moves - pure skill only!\n")

    agent.epsilon = 0  # No random moves - Kenobi uses only what he learned!

    for episode in range(1, episodes + 1):
        game.reset_game()  # fresh test environment!
        state = game.get_simple_state()
        steps = 0

        while steps < 30:  # give Kenobi 30 steps to show off
            action = agent.choose_action(state)  # what did Kenobi learn to do?
            _, reward, done = game.step(action)
            state = game.get_simple_state()
            steps += 1

            game.window.update()  # show Kenobi in action!
            game.window.after(speed)

            if done:  # oops, Kenobi hit a wall - needs more training!
                print(f"  Test {episode}: HIT WALL after {steps} steps, score {game.score}")
                break

        if not done:  # Kenobi survived! How many foods did he find?
            print(f"  Test {episode}: Score {game.score} in {steps} steps - Good job Kenobi!")


# Main program - where the training adventure begins!
if __name__ == "__main__":
    print("=" * 50)
    print("   Q-Learning Training for Security Bot")
    print("   Teaching Kenobi to find his food!")
    print("=" * 50)
    print("\nOptions:")
    print("1. Show OPTIMAL demo first (see how it SHOULD work)")
    print("2. Train the agent (watch Kenobi learn)")
    print("3. Train fast, then test (for the impatient!)")

    choice = input("\nChoose (1/2/3): ").strip()

    if choice == "1":
        # First show the perfect robot, then train Kenobi to match it!
        show_optimal_demo(episodes=3, speed=80)
        input("\nPress Enter to start training Kenobi...")
        agent = train(episodes=30, max_steps=30, visualize=True, speed=30)
        test(agent, episodes=3, speed=100)
        game.window.mainloop()

    elif choice == "2":
        # Watch Kenobi learn in real-time - educational and fun!
        agent = train(episodes=50, max_steps=30, visualize=True, speed=20)
        test(agent, episodes=3, speed=100)
        game.window.mainloop()

    elif choice == "3":
        # Speed run! Train fast then show off Kenobi's skills
        print("\nTraining Kenobi in hyperspeed mode...")
        agent = train(episodes=100, max_steps=30, visualize=False, speed=1)
        print("\nNow watch the trained Kenobi in action:")
        test(agent, episodes=5, speed=80)
        game.window.mainloop()

    else:
        # Default: just show the optimal demo
        show_optimal_demo(episodes=2, speed=100)
        game.window.mainloop()
