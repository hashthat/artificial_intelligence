# import main libraries for the RL vision board
import random
# define the directions, player should beable to use WASD keys in the end.
DIRECTIONS = {1: "up", 2: "left", 3: "down", 4: "right"} #0123? vs 1234?
HISTORY_FILE = "mvmnt_hist.txt" # create the new file which will be looped into the main function for the robot to learn

# automated moves for the robot kenobi to move in, the robot might eventually get hungry as the game progresses?!
def automate_moves(moves=100):
    """Move automatically a specified number of times."""
    print(f"\nI am about to move {moves} times and record the movements!")
    for _ in range(moves): # using the range function to randomize WASD
        direction_number = random.randint(1, 4)
        print(f"I moved {DIRECTIONS[direction_number]}") # robot declares the move!
        with open(HISTORY_FILE, "a") as f: # open the file for the move history
            f.write(str(direction_number) + ",") # write into the mvmnt_hist.txt file
    print("Automated moves complete!") # print when the automation is complete!


def kenobi_moves(): # manual moves as the option for the user
    """Interactive mode: move one step at a time with user confirmation."""
    should_continue = "yes" # yes, as an option vs no
    while should_continue.lower() in ["yes", "y"]:
        # yes before random number moves on the grid
        direction_number = random.randint(1, 4)
        print(f"\nI moved {DIRECTIONS[direction_number]}") #directions moved
        with open(HISTORY_FILE, "a") as f: # open file to still write the created move
            f.write(str(direction_number) + ",") # writing into file
        print("I just wrote the movement down in the history file!") # declaration to affirm new file is created!
        should_continue = input("\nWould you like me to move again? (yes/no): ") # boolean logic for the robots next move.

# the main function that completes the app and initiates the functionality of the project.
def main():
    print("\n\t*** Training a new Security Bot ***\n")
    print("Hi! I am Kenobi Bot, training to be the best security bot here at Board to Death!\n")
    print("I can move in the following directions (WASD mapped to 1234):")
    print("1 - up | 2 - left | 3 - down | 4 - right\n")
    # interactive or autmomated mode?!
    mode = input("Choose mode - (1) Interactive or (2) Automated: ").strip()
    if mode == "2":
        automate_moves()
    else:
        kenobi_moves()


if __name__ == "__main__":
    main()
