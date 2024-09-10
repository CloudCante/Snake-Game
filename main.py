from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 20
BODY_PARTS = 1
SNAKE_COLOR = "#0000FF"
FOOD_COLOR = "#FFFF00"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range (0, BODY_PARTS):
            self.coordinates.append([0, 0])
        
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="Snake")
            self.squares.append(square)

class Food:
    
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH//SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT//SPACE_SIZE) - 1) * SPACE_SIZE   

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="FOOD")

# Defining the next turn function
def next_turn(snake, food): 
    x, y = snake.coordinates[0] #this line tracks the head of the snake by marking its current x and y coordinates
    
    #This elif statement will adjust the x and y coordinates by adding or subtracting SPACE_SIZE 
    if direction == "up": 
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    
    
    snake.coordinates.insert(0, (x, y)) #With .insert we are replacing the first index in the snake.coordinate list and inserting the new coordinates (x, y) 

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        print(f"Food eaten at ({x}, {y})")
        global score
        score += 1
        print(f"Score updated: {score}")
        label.config(text="Score:{}".format(score))
        canvas.delete("FOOD")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    if check_collision(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction
    
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction
        

def check_collision(snake):
    x, y = snake.coordinates[0] #coordinates for the snakes head

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT: # compares the snake coordinates to width and height of the game. If either of these is true, it should return True and stop the game.
        print("Game Over")
        return True 

    for body_part in snake.coordinates[1:]: # iterates over the snake coordinates list skipping the head
        if x == body_part[0] and y == body_part[1]: 
            print("Game Over")
            return True

    return False

def game_over():
    print("Game Over - Function Called")
    
    # Clear the canvas without trying to lower it
    if canvas.winfo_exists():
        canvas.delete(ALL)
    
    canvas.create_text(
        canvas.winfo_width() / 2, 
        canvas.winfo_height() / 2 - 50, 
        font=('consolas', 70), 
        text='GAME OVER', 
        fill='red', 
        tag='GAMEOVER'
    )

    # Use the place geometry manager for buttons to ensure proper positioning
    retry_button = Button(
        window, 
        text="Retry", 
        command=restart_game, 
        font=("consolas", 20),
        bg="darkgray",  
        fg="white"
    )
    retry_button.place(relx=0.5, rely=0.6, anchor=CENTER)  # Positioning the button at 60% of the window height

    exit_button = Button(
        window, 
        text="Exit to Menu", 
        command=show_options_menu, 
        font=("consolas", 20),
        bg="darkgray",  
        fg="white"
    )
    exit_button.place(relx=0.5, rely=0.7, anchor=CENTER)  # Positioning the button at 70% of the window height

    # Force update the window to ensure changes take effect
    window.update_idletasks()
    window.update()
def restart_game():
    global window
    window.destroy()#closes the game
    main_game()#Restarts the game

#creating a difficulty selector 
def start_game():
    global SPEED

    difficulty = difficulty_var.get()
    if difficulty == "Easy":
        SPEED = 150
    elif difficulty == "Medium":
        SPEED = 100
    elif difficulty == "Hard":
        SPEED = 50

    window.destroy()
    main_game()

def show_options_menu():
    global window, difficulty_var
    window = Tk()
    window.title("Settings")

    Label(window, text="Select Difficulty:", font=("consolas", 20)).pack()

    difficulty_var = StringVar(value="Medium")
    Radiobutton(window, text="Easy", variable=difficulty_var, value="Easy", font=("consolas", 15)).pack(anchor=W)
    Radiobutton(window, text="Medium", variable=difficulty_var, value="Medium", font=("consolas", 15)).pack(anchor=W)
    Radiobutton(window, text="Hard", variable=difficulty_var, value="Hard", font=("consolas", 15)).pack(anchor=W)

    Button(window, text="Start Game", command=start_game, font=("consolas", 15)).pack()
    window.mainloop()

def main_game():
    global window, canvas, score, direction, snake, food, label   
    window = Tk()
    window.title("Snake game")
    window.resizable(False, False)

    score = 0
    direction = "down"

    label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
    label.pack()

    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()

    window.update()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width/2 - (window_width/2)))
    y = int((screen_height/2 - (window_height/2)))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    window.bind('<A>', lambda event: change_direction('left') )
    window.bind('<a>', lambda event: change_direction('left') )
    window.bind('<Left>', lambda event: change_direction('left') )
    window.bind('<D>', lambda event: change_direction('right') )
    window.bind('<d>', lambda event: change_direction('right') )
    window.bind('<Right>', lambda event: change_direction('right') )
    window.bind('<W>', lambda event: change_direction('up') )
    window.bind('<w>', lambda event: change_direction('up') )
    window.bind('<Up>', lambda event: change_direction('up') )
    window.bind('<S>', lambda event: change_direction('down') )
    window.bind('<s>', lambda event: change_direction('down') )
    window.bind('<Down>', lambda event: change_direction('down') )

    snake = Snake()
    food = Food()

    next_turn(snake, food)
    window.mainloop()
show_options_menu()

