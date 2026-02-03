# lets import the libraries needed for the RL project!
# tkinter is for the current GUI
import tkinter as tk
import random

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

# area!

canvas = tk.Canvas(window, width=400, height=400, bg="grey")
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
    except tk.TclError:
        # window was closed during animation
        pass

# time to move the robot!
def move_robot():
    # keep track of Kenobi's State aka position
    global robot_row, robot_col
    # Kenobi has 4 valide directions to move "WASD" "ULDR" with a list of possible directions
    directions = ["up", "down", "left", "right"]
    # choose a random direction from the list
    direction = random.choice(directions)

    # evaluate the direction Kenobi chooses
    if direction == "up":
        # Move robot by decreasing the row number but not past zero which would be the wall.
        robot_row = max(0, robot_row -1)
        # move robot down a row simply by increasing the row number not past the wall in the grid
    elif direction == "down":
        robot_row = min(15, robot_row +1)
        # moving left and right!
        # decrease the col number not past 0
    elif direction == "left":
        robot_col = max(0, robot_col -1)
        # increase the col number not past 0
    elif direction == "right":
        robot_col = min(15, robot_col +1)

    # redraw the robot as the new position is updated.
    draw_robot()
    print(f"Kenobi moved {direction} to position: row {robot_row}, Column {robot_col}")

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

window.mainloop()
