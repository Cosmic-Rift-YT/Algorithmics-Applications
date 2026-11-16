#Create your own shooter
from pygame import *
from random import randint
from time import sleep


# Window settings
window = display.set_mode((700, 500))
display.set_caption("Shooter")

clock = time.Clock()
FPS = 60
run = True
finish = False
won = False

last_shot = 0
shot_cooldown = 200

score = 0
lost = 0

font.init()
font1 = font.Font(None,100)
font2 = font.Font(None,35)

# Background
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

# Music and sounds
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play(-1)

fire = mixer.Sound("fire.ogg")

# Sprite class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, speed, size_x, size_y):
        super().__init__()

        self.player_image = transform.scale(
            image.load(player_image), (size_x, size_y)
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

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.player_speed

        if self.rect.y < 0:
            self.kill()

# Player class
class Player(GameSprite):
    def movement(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] or keys_pressed[K_a]:
            self.xcor -= self.player_speed

        if keys_pressed[K_RIGHT] or keys_pressed[K_d]:
            self.xcor += self.player_speed# Wall class

        # Keep player inside the window
        self.xcor = max(0, min(self.xcor, 650))
        self.rect.topleft = (self.xcor, self.ycor)

    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,-5,5,15)
        bullets.add(bullet)

# Enemy class
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.player_speed
        global lost

        if self.rect.y > 500:
            self.rect.x = randint(0,620)
            self.rect.y = 0
            lost = lost + 1

#create sprites
rocket = Player('rocket.png',305,380,5,80,120)
ufos = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    ufo = Enemy('ufo.png',randint(80,620),0,randint(1,2),70,50)
    ufos.add(ufo)
for i in range(3):
    asteroid = Enemy('asteroid.png',randint(80,620),0,randint(1,2),70,50)
    asteroids.add(asteroid)

win_text = font1.render("YOU WIN!", True, (255, 215, 0))
lose_text = font1.render("YOU LOSE!", True, (255, 0, 0))

# Main game loop
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE or e.key == K_f:
                current_time = time.get_ticks() 

            if current_time - last_shot >= shot_cooldown:
                last_shot = current_time
                rocket.fire()
                fire.play()

    if not finish:
        # Draw background
        window.blit(background, (0,0))

        # Move sprites
        rocket.movement()

        # Draw sprites
        rocket.reset()
        ufos.update()
        ufos.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)

        text = font2.render('Score:' + str(score),1,(255,255,255))
        window.blit(text,(0,0))
        lost_text = font2.render('Missed:' + str(lost),1,(255,255,255))
        window.blit(lost_text,(0,30))
        ufo2 = sprite.groupcollide(ufos,bullets,True,True)

        for u in ufo2:
            score += 1
            ufo = Enemy('ufo.png',randint(80,620),0,randint(1,2),70,50)
            ufos.add(ufo)

        if score > 10:
            window.blit(win_text, (150, 200))
            finish = True

        if lost > 3 or sprite.spritecollide(rocket,ufos,True):
            window.blit(lose_text, (150, 200))
            finish = True
        

    display.update()
    clock.tick(FPS)
