
# Create a Maze Game!
import pygame
from pygame import *

pygame.init()

# Window settings
window = display.set_mode((700, 500))
display.set_caption("Maze")

clock = time.Clock()
FPS = 60
run = True
finish = False
won = False

# Background
background = transform.scale(
    image.load("background.jpg"), (700, 500)
)

# Music and sounds
mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play(-1)

kick = mixer.Sound("kick.ogg")
money = mixer.Sound("money.ogg")


# Sprite class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, speed):
        super().__init__()

        self.player_image = transform.scale(
            image.load(player_image), (50, 50)
        )

        self.image = self.player_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.xcor = x
        self.ycor = y
        self.player_speed = speed

    def reset(self):
        # Keep the collision rectangle synchronized
        self.rect.topleft = (self.xcor, self.ycor)
        window.blit(self.player_image, self.rect)


# Player class
class Player(GameSprite):
    def movement(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT]:
            self.xcor -= self.player_speed

        if keys_pressed[K_RIGHT]:
            self.xcor += self.player_speed

        if keys_pressed[K_UP]:
            self.ycor -= self.player_speed

        if keys_pressed[K_DOWN]:
            self.ycor += self.player_speed

        # Keep player inside the window
        self.xcor = max(0, min(self.xcor, 650))
        self.ycor = max(0, min(self.ycor, 450))

        self.rect.topleft = (self.xcor, self.ycor)


# Enemy class
class Enemy(GameSprite):
    def __init__(self, player_image, x, y, speed):
        super().__init__(player_image, x, y, speed)
        self.direction = "left"

    def update(self):
        if self.xcor <= 470:
            self.direction = "right"

        if self.xcor >= 650:
            self.direction = "left"

        if self.direction == "left":
            self.xcor -= self.player_speed
        else:
            self.xcor += self.player_speed

        self.rect.topleft = (self.xcor, self.ycor)


# Wall class
class Wall(sprite.Sprite):
    def __init__(
        self, color_1, color_2, color_3,
        wall_x, wall_y, wall_width, wall_height
    ):
        super().__init__()

        self.image = surface.Surface(
            (wall_width, wall_height)
        )
        self.image.fill((color_1, color_2, color_3))

        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, self.rect)


# Create sprites
hero = Player("hero.png", 20, 430, 3)
cyborg = Enemy("cyborg.png", 650, 300, 3)
treasure = GameSprite("treasure.png", 550, 400, 0)

# Create walls
w1 = Wall(151, 204, 46, 100, 20, 550, 10)
w2 = Wall(151, 204, 46, 100, 470, 450, 10)
w3 = Wall(151, 204, 46, 100, 20, 10, 370)
w4 = Wall(151, 204, 46, 170, 170, 10, 340)
w5 = Wall(151, 204, 46, 240, 20, 10, 340)
w6 = Wall(151, 204, 46, 450, 100, 10, 370)
w7 = Wall(151, 204, 46, 400, 100, 120, 10)
wtop = Wall(255, 0, 0, 0, 0, 700, 10)
wbottom = Wall(255, 0, 0, 0, 490, 700, 10)
wleft = Wall(255, 0, 0, 0, 0, 10, 500)
wright = Wall(255, 0, 0, 690, 0, 10, 500)

walls = [w1, w2, w3, w4, w5, w6, w7, wtop, wbottom, wleft, wright]

# Game messages
game_font = font.Font(None, 70)
win_text = game_font.render(
    "YOU WIN!", True, (255, 215, 0)
)
lose_text = game_font.render(
    "YOU LOSE!", True, (255, 0, 0)
)

# Main game loop
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        # Draw background
        window.blit(background, (0, 0))

        # Move sprites
        hero.movement()
        cyborg.update()

        # Draw sprites
        hero.reset()
        cyborg.reset()
        treasure.reset()
       
        for wall in walls:
            wall.draw_wall()


        # Check collision with enemy
        if sprite.collide_rect(hero, cyborg):
            finish = True
            won = False
            kick.play()

        # Check collision with walls
        for wall in walls:
            if sprite.collide_rect(hero, wall):
                finish = True
                won = False
                kick.play()
                break

        # Check whether player reaches treasure
        if sprite.collide_rect(hero, treasure):
            finish = True
            won = True
            money.play()

    # Display the final result
    if finish:
        if won:
            window.blit(win_text, (200, 200))
        else:
            window.blit(lose_text, (200, 200))

    display.update()
    clock.tick(FPS)

pygame.quit()
