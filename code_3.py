#SpaceWar


import os
import random
import winsound
import time
import math
import turtle

# Initial turtle setup
turtle.fd(0)    #forward
turtle.speed(0)    #speed of the animation set to the max
turtle.bgcolor("black")
turtle.title("SpaceWar")
try:
    turtle.bgpic("starfield.gif")
except:
    pass
turtle.ht()    #hide the default turtle
turtle.setundobuffer(1)    #saves the memory
turtle.tracer(0)     #speeds up the animation


#creating a sprite class , to define the objects in our game
#based on the turtle class , so , inheriting from the turtle class, which is under the turtle module
# Sprite class
class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape=spriteshape)
        #setting the speed of animation , not the speed it moves at
        #speed for every sprite in this game is set to zero
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):            #creates a default movement function for the sprite class
        self.fd(self.speed)
        # Boundary detection
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and \
           (self.xcor() <= (other.xcor() + 20)) and \
           (self.ycor() >= (other.ycor() - 20)) and \
           (self.ycor() <= (other.ycor() + 20)):
            return True
        return False

# Player class
class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed = 4
        self.lives = 4
        self.shielded = False
        self.shield_timer = 0
        self.speed_boost_timer = 0

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

    def update(self):
        if self.shielded and time.time() - self.shield_timer > 10:
            self.shielded = False
        if self.speed > 4 and time.time() - self.speed_boost_timer > 10:
            self.speed = 4

# Enemy class
class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 4
        self.setheading(random.randint(0, 360))

# Boss class
class Boss(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.health = 3
        self.speed = 3
        self.shapesize(stretch_wid=2, stretch_len=2)

    def move(self):
        self.fd(self.speed)
        self.sety(self.ycor() + 10 * math.sin(self.xcor() / 20))
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

# Ally class
class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 8
        self.setheading(random.randint(0, 360))

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

# Missile class
class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            try:
                winsound.PlaySound("laser.wav", winsound.SND_ASYNC)
            except:
                pass
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"
            game.missiles_fired += 1

    def move(self):
        if self.status == "ready":
            self.goto(-1000, 1000)
        if self.status == "firing":
            self.fd(self.speed)
            if self.xcor() < -290 or self.xcor() > 290 or \
               self.ycor() < -290 or self.ycor() > 290:
                self.goto(-1000, 1000)
                self.status = "ready"

# Particle class
class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000, -1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))
        self.frame = 1
        self.color(random.choice(["orange", "yellow", "red"]))
        self.shapesize(stretch_wid=random.uniform(0.1, 0.3), stretch_len=random.uniform(0.1, 0.3))

    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1
        if self.frame > 20:
            self.frame = 0
            self.goto(-1000, -1000)

# Star class
class Star(Sprite):
    def __init__(self):
        Sprite.__init__(self, "circle", "white", random.randint(-300, 300), random.randint(-300, 300))
        self.shapesize(stretch_wid=0.1, stretch_len=0.1)
        self.speed = random.randint(1, 3)
        self.setheading(270)

    def move(self):
        self.fd(self.speed)
        if self.ycor() < -300:
            self.goto(random.randint(-300, 300), 300)
            self.setheading(270)
        if self.xcor() > 300:
            self.setx(300)
            self.setheading(270)
        if self.xcor() < -300:
            self.setx(-300)
            self.setheading(270)

# Asteroid class
class Asteroid(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = random.randint(1, 3)
        self.setheading(random.randint(0, 360))

    def move(self):
        self.fd(self.speed)
        if self.xcor() > 290 or self.xcor() < -290 or self.ycor() > 290 or self.ycor() < -290:
            self.goto(random.randint(-200, 200), random.randint(-200, 200))

# PowerUp class
class PowerUp(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 2
        self.setheading(random.randint(0, 360))
        self.type = random.choice(["shield", "speed", "life"])

    def move(self):
        self.fd(self.speed)
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

# Game class
class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "start"
        self.pen = turtle.Turtle()
        self.lives = 4
        self.enemies_destroyed = 0
        self.missiles_fired = 0
        self.achievements = {"destroy_10_enemies": False}

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()

    def show_status(self):
        self.pen.undo()
        msg = f"Score: {self.score}  Lives: {self.lives}  Level: {self.level}"
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))

    def show_start_screen(self):
        self.pen.penup()
        self.pen.goto(0, 50)
        self.pen.color("white")
        self.pen.write("SpaceWar", align="center", font=("Arial", 30, "bold"))
        self.pen.goto(0, 0)
        self.pen.write("Press S to Start", align="center", font=("Arial", 16, "normal"))
        turtle.update()

    def show_game_over(self):
        self.pen.clear()
        self.pen.penup()
        self.pen.color("red")
        self.pen.goto(0, 100)
        self.pen.write("Game Over!", align="center", font=("Arial", 30, "bold"))
        self.pen.goto(0, 20)
        self.pen.color("white")
        self.pen.write(f"Score: {self.score}\nEnemies Destroyed: {self.enemies_destroyed}\nMissiles Fired: {self.missiles_fired}", align="center", font=("Arial", 16, "normal"))
        self.pen.goto(0, -60)
        self.pen.write("Press R to Restart", align="center", font=("Arial", 16, "normal"))
        turtle.update()

    def show_level_up(self):
        self.pen.penup()
        self.pen.goto(0, 0)
        self.pen.color("yellow")
        self.pen.write(f"Level {self.level}!", align="center", font=("Arial", 24, "bold"))
        turtle.update()
        time.sleep(1)
        self.pen.undo()

    def toggle_pause(self):
        self.state = "paused" if self.state == "playing" else "playing"
        if self.state == "paused":
            self.pen.penup()
            self.pen.goto(0, 0)
            self.pen.color("white")
            self.pen.write("Paused", align="center", font=("Arial", 30, "bold"))
            turtle.update()
        else:
            self.pen.undo()

    def start_game(self):
        self.state = "playing"
        self.pen.clear()
        self.score = 0
        self.lives = 4
        self.level = 1
        self.enemies_destroyed = 0
        self.missiles_fired = 0
        self.achievements = {"destroy_10_enemies": False}
        player.goto(0, 0)
        player.setheading(0)
        player.speed = 4
        player.shielded = False
        for enemy in enemies:
            enemy.goto(random.randint(-200, 200), random.randint(-200, 200))
            enemy.speed = 4
        for ally in allies:
            ally.goto(random.randint(-200, 200), random.randint(-200, 200))
        for powerup in powerups:
            powerup.goto(random.randint(-200, 200), random.randint(-200, 200))
        self.show_status()

    def next_level(self):
        self.level += 1
        self.show_level_up()
        for enemy in enemies:
            enemy.speed += 0.3
        if self.level % 3 == 0:
            self.boss = Boss("circle", "purple", 0, 200)

# Create game objects
game = Game()
game.draw_border()
game.show_start_screen()

# Create sprites
player = Player("triangle", "white", 0, 0)
missiles = [Missile("triangle", "yellow", 0, 0) for _ in range(2)]
enemies = [Enemy("circle", "red", -100, 0) for _ in range(6)]
allies = [Ally("square", "blue", 100, 0) for _ in range(6)]
particles = [Particle("circle", "orange", 0, 0) for _ in range(20)]
stars = [Star() for _ in range(50)]
asteroids = [Asteroid("circle", "gray", random.randint(-200, 200), random.randint(-200, 200)) for _ in range(3)]
powerups = [PowerUp("circle", "green", random.randint(-200, 200), random.randint(-200, 200)) for _ in range(2)]

# Keyboard bindings
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(lambda: [missile.fire() for missile in missiles if missile.status == "ready"], "space")
turtle.onkey(game.toggle_pause, "p")
turtle.onkey(game.start_game, "s")
turtle.onkey(game.start_game, "r")
turtle.listen()

# Main game loop
last_time = time.time()
while True:
    current_time = time.time()
    if current_time - last_time >= 1/60:  # 60 FPS
        turtle.update()
        last_time = current_time

        if game.state == "paused" or game.state == "start" or game.state == "gameover":
            continue

        # Move sprites
        player.move()
        player.update()
        for missile in missiles:
            missile.move()
        for star in stars:
            star.move()
        for asteroid in asteroids:
            asteroid.move()
        for powerup in powerups:
            powerup.move()

        # Power-up collisions
        for powerup in powerups:
            if player.is_collision(powerup):
                try:
                    winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                except:
                    pass
                if powerup.type == "shield":
                    player.shielded = True
                    player.shield_timer = time.time()
                elif powerup.type == "speed":
                    player.speed = 6
                    player.speed_boost_timer = time.time()
                elif powerup.type == "life" and player.lives < 5:
                    player.lives += 1
                powerup.goto(random.randint(-200, 200), random.randint(-200, 200))
                game.show_status()

        # Enemy and boss movement
        for enemy in enemies:
            enemy.move()
            if player.is_collision(enemy) and not player.shielded:
                try:
                    winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                except:
                    pass
                x = random.randint(-250, 250)
                y = random.randint(-250, 250)
                enemy.goto(x, y)
                game.score -= 50
                game.lives -= 1
                game.show_status()
                if game.lives <= 0:
                    game.state = "gameover"
                    game.show_game_over()
                    break

            for missile in missiles:
                if missile.is_collision(enemy):
                    try:
                        winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                    except:
                        pass
                    x = random.randint(-250, 250)
                    y = random.randint(-250, 250)
                    enemy.goto(x, y)
                    missile.status = "ready"
                    game.score += 100
                    game.enemies_destroyed += 1
                    game.show_status()
                    for particle in particles:
                        particle.explode(missile.xcor(), missile.ycor())
                    if game.enemies_destroyed >= 10 and not game.achievements["destroy_10_enemies"]:
                        game.achievements["destroy_10_enemies"] = True
                        game.pen.penup()
                        game.pen.goto(0, 0)
                        game.pen.write("Achievement: Destroy 10 Enemies!", align="center", font=("Arial", 16, "normal"))
                        turtle.update()
                        time.sleep(1)
                        game.pen.undo()

        if hasattr(game, 'boss'):
            game.boss.move()
            if player.is_collision(game.boss) and not player.shielded:
                try:
                    winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                except:
                    pass
                game.lives -= 1
                game.score -= 100
                game.show_status()
                if game.lives <= 0:
                    game.state = "gameover"
                    game.show_game_over()
                    break
            for missile in missiles:
                if missile.is_collision(game.boss):
                    try:
                        winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                    except:
                        pass
                    game.boss.health -= 1
                    missile.status = "ready"
                    game.score += 200
                    game.enemies_destroyed += 1
                    game.show_status()
                    for particle in particles:
                        particle.explode(missile.xcor(), missile.ycor())
                    if game.boss.health <= 0:
                        del game.boss
                    if game.enemies_destroyed >= 10 and not game.achievements["destroy_10_enemies"]:
                        game.achievements["destroy_10_enemies"] = True
                        game.pen.penup()
                        game.pen.goto(0, 0)
                        game.pen.write("Achievement: Destroy 10 Enemies!", align="center", font=("Arial", 16, "normal"))
                        turtle.update()
                        time.sleep(1)
                        game.pen.undo()

        for ally in allies:
            ally.move()
            for missile in missiles:
                if missile.is_collision(ally):
                    try:
                        winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                    except:
                        pass
                    x = random.randint(-250, 250)
                    y = random.randint(-250, 250)
                    ally.goto(x, y)
                    missile.status = "ready"
                    game.score -= 50
                    game.show_status()

        for particle in particles:
            particle.move()

        # Asteroid collision
        for asteroid in asteroids:
            if player.is_collision(asteroid) and not player.shielded:
                game.lives -= 1
                game.score -= 25
                asteroid.goto(random.randint(-200, 200), random.randint(-200, 200))
                game.show_status()
                if game.lives <= 0:
                    game.state = "gameover"
                    game.show_game_over()
                    break

        # Level progression
        if game.score >= game.level * 1500:
            game.next_level()
