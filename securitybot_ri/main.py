import random

DIRECTIONS = {1: "up", 2: "left", 3: "down", 4: "right"}
HISTORY_FILE = "mvmnt_hist.txt"


def automate_moves(moves=100):
    """Move automatically a specified number of times."""
    print(f"\nI am about to move {moves} times and record the movements!")
    for _ in range(moves):
        direction_number = random.randint(1, 4)
        print(f"I moved {DIRECTIONS[direction_number]}")
        with open(HISTORY_FILE, "a") as f:
            f.write(str(direction_number) + ",")
    print("Automated moves complete!")


def kenobi_moves():
    """Interactive mode: move one step at a time with user confirmation."""
    should_continue = "yes"
    while should_continue.lower() in ["yes", "y"]:
        direction_number = random.randint(1, 4)
        print(f"\nI moved {DIRECTIONS[direction_number]}")
        with open(HISTORY_FILE, "a") as f:
            f.write(str(direction_number) + ",")
        print("I just wrote the movement down in the history file!")
        should_continue = input("\nWould you like me to move again? (yes/no): ")


def main():
    print("\n\t*** Training a new Security Bot ***\n")
    print("Hi! I am Kenobi Bot, training to be the best security bot here at Board to Death!\n")
    print("I can move in the following directions (WASD mapped to 1234):")
    print("1 - up | 2 - left | 3 - down | 4 - right\n")

    mode = input("Choose mode - (1) Interactive or (2) Automated: ").strip()
    if mode == "2":
        automate_moves()
    else:
        kenobi_moves()


if __name__ == "__main__":
    main()
