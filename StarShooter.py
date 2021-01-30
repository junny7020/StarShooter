import os
import datetime
import time
from random import randint as rand
import turtle
import tkinter

w = input("Enter the width of the screen resolutions: ")
h = input("Enter the height of the screen resolutions: ")
print("If your inputs are not valid the game" +
      " will be played on default resolutions")
time.sleep(1)
try:
    screen_width = int(w)
    screen_height = int(h)
except ValueError:
    print("That's not an int!")
    screen_width = 1920
    screen_height = 1080

screen = turtle.Screen()
screen.setup(width=screen_width*0.5,
             height=screen_height*0.75,
             startx=100,
             starty=0)
turtle.fd(0)
turtle.speed(0)
turtle.bgcolor("black")

# All the image files are personally made

turtle.bgpic("space.gif")
turtle.title("StarShooter")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)
is_paused = False
is_boss = False
freeze = False
wasd = False


class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, colour, start_x, start_y):
        turtle.Turtle.__init__(self, shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(colour)
        self.fd(0)
        self.goto(start_x, start_y)
        self.speed = 1

    def move(self):
        self.fd(self.speed)
        hor_direction = self.heading()

        if self.xcor() > 290:
            self.setx(290)
            self.setheading(180 - hor_direction)

        if self.xcor() < -290:
            self.setx(-290)
            self.setheading(180 - hor_direction)

        if self.ycor() > 290:
            self.sety(290)
            self.setheading(360 - hor_direction)

        if self.ycor() < -290:
            self.sety(-290)
            self.setheading(360 - hor_direction)

    def collision(self, other):
        if ((self.xcor() >= (other.xcor()-20)) and
            (self.xcor() <= (other.xcor()+20)) and
            (self.ycor() >= (other.ycor()-20)) and
                (self.ycor() <= (other.ycor()+20))):
            return True
        else:
            return False


class Player(Sprite):

    def __init__(self, spriteshape, colour, start_x, start_y):
        Sprite.__init__(self, spriteshape, colour, start_x, start_y)
        self.shapesize(stretch_wid=0.5, stretch_len=1.3, outline=None)
        self.speed = 4
        self.lives = 3

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accel(self):
        self.speed += 1

    def decel(self):
        self.speed -= 1

    def cheat(self):
        global freeze
        freeze = True


class Astriod(Sprite):
    def __init__(self, spriteshape, colour, start_x, start_y):
        Sprite.__init__(self, spriteshape, colour, start_x, start_y)
        self.speed = 6
        self.setheading(rand(0, 360))


class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 8
        self.setheading(rand(0, 360))

    def move(self):
        self.fd(self.speed)

        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)

# sound files from https://www.soundfishing.eu/ Royalty free


class Bullet(Sprite):
    def __init__(self, spriteshape, colour, start_x, start_y):
        Sprite.__init__(self, spriteshape, colour, start_x, start_y)
        self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.speed = 25
        self.status = "ready to fire"
        self.goto(0, -310)

    def fire(self):
        if self.status == "ready to fire":
            os.system("afplay sfshooting.mp3&")
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "      !fired!      "

    def move(self):
        if self.status == "      !fired!      ":
            self.fd(self.speed)

        if self.status == "ready to fire":
            self.goto(0, -310)

        if ((self.xcor() < -500 or
             self.xcor() > 500) or
            (self.ycor() < -500 or
                self.ycor() > 500)):
            self.goto(0, -310)
            self.status = "ready to fire"


class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "starting"
        self.pen = turtle.Turtle()
        self.lives = 3
        self.loaded = "None"

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for i in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        if game.lives > 0:
            msg = "[%s] Level: %s Lives: %s Score: %s  (%s)" % (self.state,
                                                                self.level,
                                                                self.lives,
                                                                self.score,
                                                                self.loaded)
        else:
            msg = "Game Over Score: %s" % (self.score)
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))

    def show_starting(self):
        turtle.bgpic("intro.gif")
        turtle.update()
        time.sleep(5)
        turtle.bgpic("space.gif")
        self.state = "setup"

    def set_state(self, state):
        states = ["playing", "setup",
                  "starting", "restart",
                  "gameover", "boss"]
        if state in states:
            self.state = state
        else:
            state = "starting"

    def save(self):
        f = open("save_file.txt", "w")
        f.write("%s %s %s" % (str(self.level),
                              str(self.lives),
                              str(self.score)))
        f.close()

    def load(self):
        f = open("save_file.txt", "r")
        file_content = f.read()
        save_content = file_content.split()
        self.level = int(save_content[0])
        self.lives = int(save_content[1])
        self.score = int(save_content[2])
        self.loaded = "Loaded"
        f.close()


def boss_key():
    global is_boss
    if is_boss is False:
        boss = True
        game.state = "boss"

    else:
        is_boss = False
        game.state = "restart"


def gameover_m():
    player_name = input("Enter your name: ")
    result = tkinter.messagebox.showinfo("Game Over",
                                         "Your Score: %s"
                                         % (game.score))
    f = open("recentscore.txt", "r")
    file_content = f.read()
    tkinter.messagebox.showinfo("Leader Board",
                                "%s" % (file_content))
    f = open("recentscore.txt", "a")
    date_record = datetime.date.today()
    if freeze is True:
        f.write("%s %s %s %s(Cheat)\n" % (date_record,
                                          game.score,
                                          player_name,
                                          game.loaded))
    else:
        f.write("%s %s %s %s\n" % (date_record,
                                   game.score,
                                   player_name,
                                   game.loaded))
    f.close()


def Pause():
    global is_paused
    if is_paused is False:
        is_paused = True
    else:
        is_paused = False


accel_key = "Up"
decel_key = "Down"
rturn_key = "Right"
lturn_key = "Left"


def setting():
    global wasd
    global accel_key
    global decel_key
    global rturn_key
    global lturn_key

    if wasd is False:
        rturn_key = "d"
        accel_key = "w"
        decel_key = "s"
        lturn_key = "a"
        wasd = True

    else:
        accel_key = "Up"
        decel_key = "Down"
        rturn_key = "Right"
        lturn_key = "Left"
        wasd = False

    turtle.onkey(player.turn_left, lturn_key)
    turtle.onkey(player.turn_right, rturn_key)
    turtle.onkey(player.accel, accel_key)
    turtle.onkey(player.decel, decel_key)


game = Game()
game.draw_border()
game.show_status()

if game.state == "starting":
    game.show_starting()
if game.state == "setup":
    player = Player("triangle", "white", 0, 0)
    bullet = Bullet("triangle", "yellow", 0, 0)

    allies = []
    num_allies = 6
    for i in range(num_allies):
        allies.append(Ally("square", "blue", 100, 0))

    astriods = []
    num_astriods = 6
    for i in range(num_astriods):
        astriods.append(Astriod("circle", "red", -100, 0))

    game.set_state("playing")


turtle.onkey(player.turn_left, lturn_key)
turtle.onkey(player.turn_right, rturn_key)
turtle.onkey(player.accel, accel_key)
turtle.onkey(player.decel, decel_key)

turtle.onkey(bullet.fire, "space")
turtle.onkey(Pause, "p")
turtle.onkey(boss_key, "b")
turtle.onkey(player.cheat, "c")
turtle.onkey(game.save, "o")
turtle.onkey(game.load, "l")


turtle.listen()


while True:
    setting = screen.getcanvas()
    activate_setting = tkinter.Button(setting.master,
                                      text="(arrow) keys to wasd",
                                      font=("Arial", 16, "normal"),
                                      fg="white",
                                      bg="grey",
                                      command=setting)
    if wasd is True:
        activate_setting.config(text="(wasd) to arrow keys")
    else:
        activate_setting.config(text="(arrow keys) to wasd")
    setting.create_window(280, 320, window=activate_setting)
    if not is_paused and not is_boss:
        turtle.update()
        if game.state == "restart":
            game.lives = 3
            game.score = 0
            player.speed = 0
            player.goto(0, 0)
            player.setheading(0)
            player.dx = 0
            player.dy = 0

            for astriod in astriods:
                astriod.goto(-100, 0)
                astriod.speed = 1

            for ally in allies:
                ally.goto(100, 0)
                ally.speed = 1

            game.set_state("playing")

        if game.state == "boss":
            game.save()
            for ally in allies:
                ally.ht()
                ally.clear()
                del ally

            for astriod in astriods:
                astriod.ht()
                astriod.clear()
                del astriod
            player.ht()
            player.clear()
            ammo.config(text="                        ", bg="white")
            canvas.create_window(-100, 320, window=ammo)
            boss_canvas = screen.getcanvas()
            bossimage = tkinter.PhotoImage(file="bosskey.gif")
            boss_canvas.create_image(0, 0, image=bossimage)

            screen.update()

        if game.state == "playing":
            game.show_status()
            player.move()
            time.sleep(0.02)
            bullet.move()
            for ally in allies:
                ally.move()
                if bullet.collision(ally):
                    os.system("afplay explosion.mp3&")
                    x = rand(-250, 250)
                    y = rand(-250, 250)
                    ally.goto(x, y)
                    bullet.status = "ready to fire"
                    game.score -= 50

            for astriod in astriods:
                astriod.move()
                if bullet.collision(astriod):
                    os.system("afplay explosion.mp3&")
                    x = rand(-250, 250)
                    y = rand(-250, 250)
                    astriod.goto(x, y)
                    bullet.status = "ready to fire"
                    game.score += 100

                if player.collision(astriod):
                    x = rand(-250, 250)
                    y = rand(-250, 250)
                    astriod.goto(x, y)
                    game.lives -= 1
                    if game.lives < 1:
                        game.set_state("gameover")

            if freeze is True:
                for ally in allies:
                    ally.speed = 0
                for astriod in astriods:
                    astriod.speed = 0

            canvas = screen.getcanvas()
            ammo = tkinter.Label(canvas.master, text="Shoot The Astriods!!!",
                                 font=("Arial", 16, "normal"),
                                 fg="white",
                                 bg="black")
            ammo.config(text=("%s" % (bullet.status)))
            canvas.create_window(-100, 320, window=ammo)
    elif is_paused:
        screen.update()

    if game.state == "gameover":
        for i in range(360):
            player.rt(1)
        popup = screen.getcanvas()
        popup.create_window(0, 0, window=gameover_m())
        exit()

    if game.score / (game.level) > 500:
        game.level += 1
        astriods.append(Astriod("circle", "red",
                                rand(-250, 250),
                                rand(-250, 250)))
        allies.append(Ally("square", "blue", rand(-250, 250), rand(-250, 250)))
delay = input("Press enter to finish. >")
