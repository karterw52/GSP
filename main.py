from tkinter import *
from PIL import ImageTk, Image
import random
import time
import threading
import winsound
import database

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 120
SPACE_SIZE = 50
BODY_PARTS = 3

# Global variables
direction = 'down'
disco = False
lebron = False
perfection = False
i = 0
connection = database.connect()


def splash_window():
    splash = Tk()
    splash.title('Start Screen')
    splash.geometry("700x700")

    # Display an image on the splash screen
    img = ImageTk.PhotoImage(Image.open("snake.png"))
    panel = Label(splash, image=img)
    panel.pack(side="bottom", fill="both")

    splash.bind("<KeyRelease>", lambda event: game_restart(event, splash))
    splash.mainloop()


def mode_window():
    mode = Tk()
    mode.title('Select Mode')
    mode.geometry("700x700")

    img1 = ImageTk.PhotoImage(Image.open("select mode.png"))
    panel = Label(mode, image=img1)
    panel.pack(side="bottom", fill="both")

    mode.bind("<KeyRelease>", lambda event: change_mode(event, mode))
    mode.mainloop()


def change_mode(event, mode):
    global BACKGROUND_COLOR, SPEED, disco, lebron, perfection

    if event.keysym == 's':
        mode.destroy()
        main_window()
    elif event.keysym == '1':
        BACKGROUND_COLOR = "#FFFFFF"
    elif event.keysym == '4':
        disco = True
    elif event.keysym == '2':
        SPEED = 140
    elif event.keysym == '3':
        SPEED = 50
    elif event.keysym == '6':
        lebron = True
    elif event.keysym == '9':
        perfection = True


def disco_time():
    global BACKGROUND_COLOR, canvas

    # Play disco music
    winsound.PlaySound('DiscoTimeIntro.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)
    time.sleep(7.25)
    winsound.PlaySound('DiscoTimeSound.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)

    while True:
        random_number = random.randint(0, 4)
        colours = ["#7C02A8", "#251ABA", "#EE0008", "#178B00", "#DCDC00", '#000000']
        BACKGROUND_COLOR = colours[random_number]
        canvas.config(background=BACKGROUND_COLOR)
        time.sleep(2)


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for _ in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_image(x, y, anchor=N, image=image) if lebron else canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="#00FF00", tag='snake'
            )
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        self.image = canvas.create_image(x, y, anchor=N, image=basketball) if lebron else canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="#FF0000", tag="food"
        )

    def delete_food(self):
        canvas.delete(self.image)


def next_turn(snake, food):
    global score
    global i

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    if lebron is True:
        square = canvas.create_image(x, y, anchor=N, image=image)
    elif lebron is False and perfection is False:
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="#00FF00", tag='snake')
    elif perfection is True:
        i += 1
        if i % 3 == 0:
            square = canvas.create_image(x, y, image=shane)
        elif i % 3 == 1:
            square = canvas.create_image(x, y, image=henry)
        elif i % 3 == 2:
            square = canvas.create_image(x, y, image=hariz)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score:{}".format(score))
        food.delete_food()
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_restart(event, window):
    global direction

    if event.keysym == 'r':
        direction = 'down'
        window.destroy()
        main_window()
    elif event.keysym == 's':
        window.destroy()
        main_window()
    elif event.keysym == 'm':
        window.destroy()
        mode_window()


def game_over():
    global connection, score
    canvas.delete(ALL)
    database.add_score(connection, score)
    high_score = database.get_highest_score(connection)
    window.bind("<KeyRelease>", lambda event: game_restart(event, window))

    canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 30, font=('consolas', 70),
        text="GAME OVER", fill="red", tag="gameover"
    )
    canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() - 600, font=('consolas', 50),
        text=f"High Score = {high_score[0]}", fill="red", tag="gameover"
    )
    canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 40, font=('consolas', 40),
        text="Press 'r' to Restart", fill="red", tag="gameover"
    )


def main_window():
    global window, canvas, label, score, disco, image, the_canvas, basketball, shane, henry, hariz

    # Play background music
    winsound.PlaySound('Background.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)

    if disco:
        thread = threading.Timer(1, disco_time)
        thread.start()

    window = Tk()
    window.title("Snake game")
    window.resizable(False, False)
    score = 0
    label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
    label.pack()

    canvas = Canvas(window, bg="#000000", height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()

    window.update()

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    image = PhotoImage(file='lebron.png')
    basketball = PhotoImage(file='basketball.png')
    shane = PhotoImage(file='shane.png')
    henry = PhotoImage(file='henry.png')
    hariz = PhotoImage(file='hariz.png')

    the_canvas = Canvas(window)
    the_canvas.pack(pady=1)

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    window.bind('<Left>', lambda event: change_direction('left'))
    window.bind('<Right>', lambda event: change_direction('right'))
    window.bind('<Up>', lambda event: change_direction('up'))
    window.bind('<Down>', lambda event: change_direction('down'))

    snake = Snake()
    food = Food()
    next_turn(snake, food)

    window.mainloop()


splash_window()
