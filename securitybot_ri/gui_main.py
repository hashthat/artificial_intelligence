# lets import the libraries needed for the RL project!
# tkinter is for the current GUI
import tkinter as tk
import random
from main import DIRECTIONS, HISTORY_FILE

# Creating the main Window

window = tk.Tk()
# setting put the attributes ex. Title
window.title("Training a new Security Bot")

# cells size ~ 15-25 pixels per cell for good visibility
# 16x16 grid for snake game
cell_size = 25

# states/rows/columns
# start in center of 16x16 grid
robot_row = 8
robot_col = 8

# RL Rewards System
food_row = 0
food_col = 0
score = 0
last_reward = 0  # Track the most recent reward for RL training

# Reward values (tune these for your RL algorithm)
REWARD_FOOD = 10.0      # Reward for collecting food
REWARD_STEP = 0.0       # No step penalty
REWARD_WALL = -10.0     # Penalty for hitting a wall (ends episode)
REWARD_CLOSER = 2.0     # STRONG bonus for moving closer to food
REWARD_FARTHER = -2.0   # STRONG penalty for moving away from food

# Episode tracking
episode_done = False
episode_count = 1

def spawn_food():
    """Spawn food at a random position (not on robot)."""
    global food_row, food_col # food position as robot finds some food to eat!
    while True:
        food_row = random.randint(0, 15) # respawn random row for food
        food_col = random.randint(0, 15) # respawn random column for food
        # Make sure food doesn't spawn on robot!!
        if food_row != robot_row or food_col != robot_col:
            break

def check_food_collision(): # Reward function for the robot to feel accomplished!
    """Check if robot collected food, return reward."""
    global score, last_reward
    if robot_row == food_row and robot_col == food_col:
        score += 1 # increase score when food is collected
        last_reward = REWARD_FOOD # set last reward for RL Q-Learning
        spawn_food() # respawn food after collection
        print(f"FOOD COLLECTED! Score: {score}")
        return REWARD_FOOD # return reward for collecting food
    last_reward = REWARD_STEP # working on rewards to help the robot find food!~
    return REWARD_STEP # small penalty to encourage the robot to find food faster!

def get_state():
    """Return current state tuple for RL: (robot_row, robot_col, food_row, food_col)."""
    return (robot_row, robot_col, food_row, food_col) 

def get_relative_state():
    """
    Return state relative to food position - easier for RL to learn.
    Returns: (delta_row, delta_col) where negative=food is above/left, positive=food is below/right
    """
    delta_row = food_row - robot_row  # positive = food is below
    delta_col = food_col - robot_col  # positive = food is right
    return (delta_row, delta_col)

def get_simple_state():
    """
    Simplified state - just the DIRECTION to food.
    Only 9 possible states: (-1/0/1, -1/0/1)
    This makes learning almost instant!
    """
    delta_row = food_row - robot_row # positive = food is below
    delta_col = food_col - robot_col # positive = food is right

    # Convert to simple direction: -1 (up/left), 0 (same), +1 (down/right)
    dir_row = 0 if delta_row == 0 else (1 if delta_row > 0 else -1) # positive = food is below, negative = food is above
    dir_col = 0 if delta_col == 0 else (1 if delta_col > 0 else -1) # positive = food is right, negative = food is left

    return (dir_row, dir_col)

def get_optimal_action():
    """
    Returns the BEST action to take right now.
    This is what the agent SHOULD learn to do.
    Kenobi's cheat sheet for finding food! Hopefully he learns this on his own eventually!
    """
    state = get_simple_state()
    dir_row, dir_col = state  # grab the direction to the tasty food!

    # Priority: move toward food - Kenobi's belly is rumbling!
    # If food is above (dir_row = -1), go up (action 0)
    # If food is below (dir_row = 1), go down (action 1)
    # If food is left (dir_col = -1), go left (action 2)
    # If food is right (dir_col = 1), go right (action 3)

    if dir_row == -1:  # food is above - look up Kenobi!
        return 0  # go up
    elif dir_row == 1:  # food is below - it's downstairs!
        return 1  # go down
    elif dir_col == -1:  # food is left - check your left side buddy!
        return 2  # go left
    elif dir_col == 1:  # food is right - it's right there!
        return 3  # go right
    else:
        return 0  # shouldn't happen, Kenobi is confused but let's go up anyway!

def get_last_reward(): 
    """Return the most recent reward signal for RL training."""
    return last_reward 

def reset_game(): # reset the game for a new phase/episode to train the robot to find the food.
    """Reset game state for new episode."""
    global robot_row, robot_col, score, last_reward, episode_done, episode_count 
    robot_row = 8 # reset robot to original position when the game started
    robot_col = 8 # reset robot to original position when the game started
    score = 0 # reset score for new episode --? Hopefully the robot learns to get a higher score.
    last_reward = 0 # reset last reward for new episode
    episode_done = False 
    episode_count += 1 
    spawn_food() # call to spawn food in a new quadrant.
    print(f"=== Episode {episode_count} started ===") # keeping track of episodes to view progress.

def check_wall_collision(new_row, new_col): # wall detection to help robot stay inbounds!
    """Check if movement would hit a wall. Returns True if wall hit."""
    return new_row < 0 or new_row > 15 or new_col < 0 or new_col > 15 # out of bounds means wall collision

def get_distance_to_food(row, col): # distance function as part of the robots reward system.
    """Calculate Manhattan distance from position to food."""
    return abs(row - food_row) + abs(col - food_col) 

def calculate_distance_reward(old_row, old_col, new_row, new_col): # another calculation to help the robot learn.
    """Reward for moving closer to food, penalty for moving away."""
    old_dist = get_distance_to_food(old_row, old_col)
    new_dist = get_distance_to_food(new_row, new_col)

    if new_dist < old_dist: # calculating new and old distance to the food. Hopefully this helps kenobi bot learn!
        return REWARD_CLOSER  # Got closer!
    elif new_dist > old_dist: # Calcuate new distance
        return REWARD_FARTHER  # Moved away
    return 0  # Same distance

# Initialize food position
spawn_food()

# area!

canvas = tk.Canvas(window, width=400, height=420, bg="grey")
# add the canvas just made to gui window
canvas.pack()

# creating a function to draw a grid on the screen
# keeping it simple!

def draw_grid():
    for i in range(17):
        canvas.create_line(i * cell_size, 0, i * cell_size, 400, fill="black")  # vertical
        canvas.create_line(0, i * cell_size, 400, i * cell_size, fill="black")  # horizontal


# Create a function to draw the robot
def draw_robot():
    try:
        # call and redraw with a delete function
        canvas.delete('all')
        # redraw the grid with the new updated position!
        draw_grid()

        # Draw the food as a red square
        fx1 = food_col * cell_size
        fy1 = food_row * cell_size
        fx2 = fx1 + cell_size
        fy2 = fy1 + cell_size
        canvas.create_rectangle(fx1, fy1, fx2, fy2, fill="red")
        canvas.create_text(fx1 + cell_size//2, fy1 + cell_size//2, text="F", fill="white", font=("Arial", 14, "bold"))

        # Calculate position or state
        # Calculate the x position or left side of the robot square
        x1 = robot_col * cell_size
        # calculate the y position or the top of the robot square
        y1 = robot_row * cell_size
        # calculate the x position for the right side of the robot square
        x2 = x1 + cell_size
        # calculate the y position for the bottom side of the robot square
        y2 = y1 + cell_size
        # time to draw the robot as a text with a (neon) green square
        canvas.create_rectangle(x1,y1,x2,y2, fill="green")
        # time to add text for the future image of Kenobi's identity.
        canvas.create_text(x1 + cell_size//2, y1 + cell_size//2, text="ROBOT", fill="white", font=("Arial", 12, "bold", "italic"))

        # Draw score display
        dist = get_distance_to_food(robot_row, robot_col)
        canvas.create_text(200, 405, text=f"Ep: {episode_count} | Score: {score} | Dist: {dist} | Reward: {last_reward:.1f}", fill="white", font=("Arial", 9, "bold"))
    except tk.TclError:
        # window was closed during animation
        pass

# time to move the robot!
def move_robot():
    # keep track of Kenobi's State aka position
    global robot_row, robot_col, last_reward
    # Kenobi has 4 valide directions to move "WASD" "ULDR" with a list of possible directions
    directions = ["up", "down", "left", "right"]
    # choose a random direction from the list
    direction = random.choice(directions)

    # Save old position for distance reward
    old_row, old_col = robot_row, robot_col

    # Calculate intended new position
    new_row, new_col = robot_row, robot_col
    if direction == "up":
        new_row = robot_row - 1
    elif direction == "down":
        new_row = robot_row + 1
    elif direction == "left":
        new_col = robot_col - 1
    elif direction == "right":
        new_col = robot_col + 1

    # Check for wall collision
    if check_wall_collision(new_row, new_col):
        last_reward = REWARD_WALL
        print(f"WALL HIT! Kenobi crashed into the wall. Final score: {score}")
        draw_robot()
        # Auto-reset after wall hit
        window.after(1000)  # Brief pause to show collision
        window.update()
        reset_game()
        draw_robot()
        return REWARD_WALL

    # Move is valid, update position
    robot_row, robot_col = new_row, new_col

    # Check for food collection and get reward
    reward = check_food_collision()

    # Add distance-based shaping (only if didn't eat food)
    if reward != REWARD_FOOD:
        distance_reward = calculate_distance_reward(old_row, old_col, new_row, new_col)
        reward += distance_reward
        last_reward = reward

    # redraw the robot as the new position is updated.
    draw_robot()
    dist = get_distance_to_food(robot_row, robot_col)
    print(f"Kenobi moved {direction} to ({robot_row}, {robot_col}) | Reward: {reward:.1f} | Distance to food: {dist}")
    return reward

def step(action):
    """
    RL-friendly step function. Takes an action (0-3) and returns (state, reward, done).
    Actions: 0=up, 1=down, 2=left, 3=right
    """
    global robot_row, robot_col, episode_done, last_reward

    # Save old position for distance reward
    old_row, old_col = robot_row, robot_col

    # Calculate intended new position
    new_row, new_col = robot_row, robot_col
    if action == 0:  # up
        new_row = robot_row - 1
    elif action == 1:  # down
        new_row = robot_row + 1
    elif action == 2:  # left
        new_col = robot_col - 1
    elif action == 3:  # right
        new_col = robot_col + 1

    # Check for wall collision
    if check_wall_collision(new_row, new_col):
        last_reward = REWARD_WALL
        episode_done = True
        print(f"WALL HIT! Episode over. Final score: {score}")
        draw_robot()
        return get_state(), REWARD_WALL, True

    # Move is valid, update position
    robot_row, robot_col = new_row, new_col

    # Check for food collection
    reward = check_food_collision()

    # Add distance-based shaping (only if didn't eat food)
    if reward != REWARD_FOOD:
        distance_reward = calculate_distance_reward(old_row, old_col, new_row, new_col)
        reward += distance_reward
        last_reward = reward

    # Redraw
    draw_robot()

    return get_state(), reward, False

# create a function to handle the event for moving Kenobi with a button!

def move_kenobi():
    try:
        # user places number within the textbox.
        num_moves = int(entry.get())
        # now loop the number of moves
        for i in range(num_moves):
            #move robot each move
            move_robot()
            # update window
            window.update()
            # delay and see kenobi move in human speed
            window.after(500)
    except tk.TclError:
        # window was closed during animation
        pass

# create a label to inform the user on what to do.
label = tk.Label(window, text="number of moves?", font=("Arial", 12))
# add label to window created
label.pack()

# creating the textbox for number of moves
entry = tk.Entry(window, font=("Arial", 12))
entry.pack()

# button!
button = tk.Button(window, text="Move Kenobi Bot", command=move_kenobi, font=("Arial",12), bg="lightgreen")
button.pack()



draw_robot()
draw_grid()
#let user know what's up
print("Robot has been awakened!")
print(f"Kenobi start position Row: {robot_row}, Column {robot_col}")

# Only run mainloop if this file is run directly (not imported)
if __name__ == "__main__":
    window.mainloop()
