# ************************************

# Python Snake

# ************************************

from tkinter import *

from PIL import ImageTk, Image

import random

import time

import threading

import winsound

global splash

global lebron

lebron = False

GAME_WIDTH = 700

GAME_HEIGHT = 700

SPEED = 120

SPACE_SIZE = 50

BODY_PARTS = 3

disco = False

direction = 'down'



img = Image.open("snake.png")

def splash_window():
    global splash
    global SNAKE_COLOR
    global FOOD_COLOR
    global BACKGROUND_COLOR
    global SPEED

    SNAKE_COLOR = "#00FF00"

    FOOD_COLOR = "#FF0000"

    BACKGROUND_COLOR = "#000000"

    splash = Tk()
    splash.title('Start Screen')
    splash.geometry("700x700")

    img = ImageTk.PhotoImage(Image.open("snake.png"))
    panel = Label(splash, image = img)
    panel.pack(side="bottom", fill="both")

    splash.bind("<KeyRelease>", game_restart)

    splash.mainloop()


def mode_window():
    global mode
    mode = Tk()
    mode.title('Select Mode')
    mode.geometry("700x700")

    img1 = ImageTk.PhotoImage(Image.open("select mode.png"))
    panel = Label(mode, image=img1)
    panel.pack(side="bottom", fill="both")

    mode.bind("<KeyRelease>", change_mode)

    mode.mainloop()


def change_mode(event):
    global BACKGROUND_COLOR
    global SPEED
    global disco
    global lebron
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



def disco_time():
    global canvas
    global BACKGROUND_COLOR
    i = 1
    while i == 1:
        winsound.PlaySound('DiscoTimeIntro.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)
        time.sleep(7.25)
        winsound.PlaySound('DiscoTimeSound.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)
        i -= 1
    while True:
        random_number = random.randint(0,4)
        colours = ["#7C02A8", "#251ABA", "#EE0008", "#178B00", "#DCDC00"]
        BACKGROUND_COLOR = colours[random_number]
        canvas.config(background=BACKGROUND_COLOR)
        time.sleep(1)


class Snake:


    def __init__(self):

        self.body_size = BODY_PARTS

        self.coordinates = []

        self.squares = []

        for i in range(0, BODY_PARTS):

            self.coordinates.append([0, 0])

        for x, y in self.coordinates:

            #square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")

            if lebron == True:
                square = canvas.create_image(x, y, anchor=N, image=image)
            elif lebron == False:
                square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag='snake')


            self.squares.append(square)


class Food:

    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE

        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        if lebron == False:
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")
        elif lebron == True:
            canvas.create_image(x, y, anchor=N, image=basketball)


def next_turn(snake, food):

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

    if lebron == True:
        square = canvas.create_image(x, y, anchor=N,image=image)
    elif lebron == False:
        square = canvas.create_rectangle(x,y,x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag='snake')

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

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


def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


def game_restart(event):
    if event.keysym == 'r':
        window.destroy()
        main_window()
    elif event.keysym == 's':
        splash.destroy()
        main_window()
    elif event.keysym == 'm':
        splash.destroy()
        mode_window()

def game_over():
    canvas.delete(ALL)
    window.bind("<KeyRelease>", game_restart)

    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 - 30, font=('consolas', 70),
                       text="GAME OVER", fill="red", tag="gameover")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 40, font=('consolas', 40),
                       text="Press 'r' to Restart", fill="red", tag="gameover")


def main_window():
    global window, canvas, label, score, disco, image, the_canvas,basketball



    winsound.PlaySound('Background.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)

    if disco is True:
        thread = threading.Timer(1, disco_time)
        thread.start()

    window = Tk()

    window.title("Snake game")

    window.resizable(False, False)

    score = 0

    label = Label(window, text="Score:{}".format(score), font=('consolas', 40))

    label.pack()

    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)

    canvas.pack()

    window.update()

    window_width = window.winfo_width()

    window_height = window.winfo_height()

    screen_width = window.winfo_screenwidth()

    screen_height = window.winfo_screenheight()

    image = PhotoImage(file='lebron.png')
    basketball = PhotoImage(file='basketball.png')

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
