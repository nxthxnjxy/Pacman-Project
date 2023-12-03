

from random import choice, randrange
from turtle import *
from freegames import floor, vector
import time
import turtle

time_limit = 120
start_time = time.time()
elapsed_time = int(time.time() - start_time)
time_left = time_limit - elapsed_time

state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(10, 0)
pacman = vector(-60, 40)
ghosts = [
    [vector(0, 0), vector(20, 0)],
    [vector(-180, -160), vector(0, 10)],
    [vector(100, 160), vector(0, -10)],
    [vector(100, -160), vector(-10, 0)],
    [vector(100, 150), vector(-10, 0)],
    [vector(-150, 130), vector(10, 0)]
]
# fmt: off
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0,
    0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 3, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 3, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on


def square(x, y, color='white'):
    """Draw square using path at (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    path.color('blue')  # Set the fill color
    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Draw world using path."""
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(5, 'white')
            elif tile == 3:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(5, 'orange')

ghost_colors = ['red', 'white', 'green', 'orange', 'purple', 'pink']
special_pellet_color = 'orange'
def game_win():
        style = ('Arial', 50)
        writer.penup()
        writer.goto(0, 0)  # Adjust the position as needed
        writer.color('Yellow')
        writer.write("YOU WIN!", align='center', font=style) 
       


def move():
    if time_left == 0:
        return
    writer.undo()
    writer.write(state['score'])

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 3:
        tiles[index] = 2
        state['score'] += 5
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y, special_pellet_color)

    elif tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)
        
        
    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for i, (point, course) in enumerate(ghosts):
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(10, 0),
                vector(-10, 0),
                vector(0, 10),
                vector(0, -10),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        if i == 0:
            dot(30, ghost_colors[i])  # Increase size to 30
        else:
            dot(20, ghost_colors[i])

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return game_over()
        
    if state['score'] == 179:  # Assuming 179 is the total number of pellets
        game_win()
        return

    ontimer(move, 100)


def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

def update_time():
    global start_time, time_left

    elapsed_time = int(time.time() - start_time)
    time_left = max(0, time_limit - elapsed_time)

    if time_left > 0:
        ontimer(update_time, 1000)  # Update every 1000 milliseconds (1 second)
    else:
        game_over()
        return
        


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
def game_over():
    style = ('Arial', 50)
    writer.penup()
    writer.goto(0, 0)  # Adjust the position as needed
    writer.color('Yellow')
    writer.write("GAME OVER!", align='center', font=style)
update_time()
world()
move()
done()
