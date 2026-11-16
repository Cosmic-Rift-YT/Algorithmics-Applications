
import pygame
from pygame import *

pygame.init()

# Window settings
WIDTH = 300
HEIGHT = 210

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Hard Platformer Adventure")

clock = time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
GREEN = (50, 200, 50)
YELLOW = (255, 220, 0)
RED = (255, 50, 50)
ORANGE = (255, 120, 0)
SKY_BLUE = (135, 206, 235)

# Player settings
player_radius = 9
player_speed = 2.5
jump_power = -7.5
gravity = 0.35
y_velocity = 0

player = pygame.Rect(12, 162, 18, 18)

# Game settings
lives = 3
score = 0
current_area = 0

run = True
on_ground = False
won = False
game_over = False

# Areas
areas = [

    # Level 1
    {
        "platforms": [
            pygame.Rect(0, 190, 300, 20),
            pygame.Rect(60, 156, 36, 9),
            pygame.Rect(132, 126, 36, 9),
            pygame.Rect(204, 96, 36, 9)
        ],

        "spikes": [
            pygame.Rect(60, 178, 12, 12),
            pygame.Rect(96, 178, 18, 12),
            pygame.Rect(150, 178, 18, 12),
            pygame.Rect(198, 178, 18, 12)
        ],

        "lava": [],

        "coins": [
            pygame.Rect(69, 138, 9, 9),
            pygame.Rect(141, 108, 9, 9)
        ]
    },

    # Level 2
    {
        "platforms": [
            pygame.Rect(0, 190, 300, 20),
            pygame.Rect(42, 150, 30, 9),
            pygame.Rect(108, 120, 30, 9),
            pygame.Rect(174, 90, 30, 9),
            pygame.Rect(240, 60, 30, 9)
        ],

        "spikes": [
            pygame.Rect(42, 178, 12, 12),
            pygame.Rect(84, 178, 18, 12),
            pygame.Rect(138, 178, 18, 12)
        ],

        "lava": [
            pygame.Rect(180, 178, 42, 12)
        ],

        "coins": [
            pygame.Rect(48, 132, 9, 9),
            pygame.Rect(114, 102, 9, 9)
        ]
    },

    # Level 3
    {
        "platforms": [
            pygame.Rect(0, 190, 300, 20),
            pygame.Rect(48, 150, 27, 9),
            pygame.Rect(102, 120, 27, 9),
            pygame.Rect(156, 90, 27, 9),
            pygame.Rect(210, 60, 27, 9)
        ],

        "spikes": [
            pygame.Rect(48, 178, 12, 12),
            pygame.Rect(90, 178, 18, 12),
            pygame.Rect(138, 178, 18, 12),
            pygame.Rect(186, 178, 18, 12)
        ],

        "lava": [],

        "coins": [
            pygame.Rect(54, 132, 9, 9),
            pygame.Rect(108, 102, 9, 9)
        ]
    },

    # Level 4
    {
        "platforms": [
            pygame.Rect(0, 190, 300, 20),
            pygame.Rect(36, 150, 24, 9),
            pygame.Rect(84, 120, 24, 9),
            pygame.Rect(132, 90, 24, 9),
            pygame.Rect(180, 60, 24, 9),
            pygame.Rect(228, 30, 36, 9)
        ],

        "spikes": [
            pygame.Rect(36, 178, 12, 12),
            pygame.Rect(72, 178, 18, 12),
            pygame.Rect(120, 178, 18, 12)
        ],

        "lava": [
            pygame.Rect(168, 178, 48, 12)
        ],

        "coins": [
            pygame.Rect(42, 132, 9, 9),
            pygame.Rect(90, 102, 9, 9)
        ]
    },

    # Level 5
    {
        "platforms": [
            pygame.Rect(0, 190, 300, 20),
            pygame.Rect(30, 150, 30, 9),
            pygame.Rect(90, 120, 30, 9),
            pygame.Rect(150, 90, 30, 9),
            pygame.Rect(210, 60, 30, 9)
        ],

        "spikes": [
            pygame.Rect(30, 178, 12, 12),
            pygame.Rect(90, 178, 12, 12),
            pygame.Rect(150, 178, 12, 12)
        ],

        "lava": [
            pygame.Rect(180, 178, 60, 12)
        ],

        "coins": [
            pygame.Rect(36, 132, 9, 9),
            pygame.Rect(96, 102, 9, 9)
        ]
    },

    # Level 6
    {
        "platforms": [
            pygame.Rect(0, 190, 300, 20),
            pygame.Rect(36, 150, 24, 9),
            pygame.Rect(84, 120, 24, 9),
            pygame.Rect(132, 90, 24, 9),
            pygame.Rect(180, 60, 24, 9),
            pygame.Rect(240, 30, 30, 9)
        ],

        "spikes": [
            pygame.Rect(36, 178, 12, 12),
            pygame.Rect(84, 178, 12, 12),
            pygame.Rect(132, 178, 12, 12)
        ],

        "lava": [
            pygame.Rect(156, 178, 60, 12)
        ],

        "coins": [
            pygame.Rect(42, 132, 9, 9),
            pygame.Rect(90, 102, 9, 9)
        ]
    },

    # Level 7: Final level
    {
        "platforms": [
            pygame.Rect(0, 190, 300, 20),
            pygame.Rect(30, 150, 24, 9),
            pygame.Rect(78, 120, 24, 9),
            pygame.Rect(126, 90, 24, 9),
            pygame.Rect(174, 60, 24, 9),
            pygame.Rect(240, 30, 30, 9)
        ],

        "spikes": [
            pygame.Rect(30, 178, 12, 12),
            pygame.Rect(78, 178, 12, 12),
            pygame.Rect(126, 178, 12, 12)
        ],

        "lava": [
            pygame.Rect(150, 178, 66, 12)
        ],

        # The final coin!
        "coins": [
            pygame.Rect(252, 12, 12, 12)
        ]
    }
]

# Save original coins
original_coins = []

for area in areas:

    original_coins.append(
        [coin.copy() for coin in area["coins"]]
    )

# Total coins
total_coins = sum(
    len(area["coins"]) for area in areas
)

# Load current area
platforms = areas[current_area]["platforms"]
spikes = areas[current_area]["spikes"]
lava = areas[current_area]["lava"]
coins = areas[current_area]["coins"]

# Fonts
font1 = font.Font(None, 16)
font2 = font.Font(None, 32)


# Reset player
def reset_player():

    global y_velocity, on_ground

    player.x = 12
    player.y = 162

    y_velocity = 0
    on_ground = False


# Restart game
def restart_game():

    global lives, score, current_area
    global platforms, spikes, lava, coins
    global won, game_over

    lives = 3
    score = 0
    current_area = 0

    # Restore every coin
    for i in range(len(areas)):

        areas[i]["coins"] = [
            coin.copy() for coin in original_coins[i]
        ]

    # Load starting area
    platforms = areas[current_area]["platforms"]
    spikes = areas[current_area]["spikes"]
    lava = areas[current_area]["lava"]
    coins = areas[current_area]["coins"]

    won = False
    game_over = False

    reset_player()


# Main game loop
while run:

    clock.tick(FPS)

    # Events
    for e in event.get():

        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN:

            if e.key == K_r and (game_over or won):

                restart_game()

    # Game logic
    if not won and not game_over:

        keys = key.get_pressed()

        # Move left
        if keys[K_LEFT]:
            player.x -= player_speed

        # Move right
        if keys[K_RIGHT]:
            player.x += player_speed

        # Next level
        if player.right >= WIDTH:

            if current_area < len(areas) - 1:

                current_area += 1

                platforms = areas[current_area]["platforms"]
                spikes = areas[current_area]["spikes"]
                lava = areas[current_area]["lava"]
                coins = areas[current_area]["coins"]

                player.left = 0

            else:

                player.right = WIDTH

        # Previous level
        elif player.left <= 0:

            if current_area > 0:

                current_area -= 1

                platforms = areas[current_area]["platforms"]
                spikes = areas[current_area]["spikes"]
                lava = areas[current_area]["lava"]
                coins = areas[current_area]["coins"]

                player.right = WIDTH

            else:

                player.left = 0

        # Jump
        if keys[K_SPACE] and on_ground:

            y_velocity = jump_power
            on_ground = False

        # Gravity
        previous_bottom = player.bottom

        y_velocity += gravity
        player.y += int(y_velocity)

        # Platform collision
        on_ground = False

        for platform in platforms:

            if player.colliderect(platform):

                if (
                    y_velocity > 0
                    and previous_bottom <= platform.top
                ):

                    player.bottom = platform.top
                    y_velocity = 0
                    on_ground = True

        # Spike collision
        hit_spike = False

        for spike in spikes:

            if player.colliderect(spike):

                hit_spike = True
                break

        # Lava collision
        hit_lava = False

        for pool in lava:

            if player.colliderect(pool):

                hit_lava = True
                break

        # Lose a life
        if hit_spike or hit_lava:

            lives -= 1
            reset_player()

        # Collect coins
        for coin in coins[:]:

            if player.colliderect(coin):

                coins.remove(coin)
                score += 1

        # Falling off the map
        if player.top > HEIGHT:

            lives -= 1
            reset_player()

        # Lose condition
        if lives <= 0:

            game_over = True

        # Win condition
        if score >= total_coins:

            won = True

    # Draw background
    window.fill(SKY_BLUE)

    # Draw platforms
    for platform in platforms:

        draw.rect(window, GREEN, platform)

    # Draw spikes
    for spike in spikes:

        draw.polygon(
            window,
            RED,
            [
                (spike.left, spike.bottom),
                (spike.centerx, spike.top),
                (spike.right, spike.bottom)
            ]
        )

    # Draw lava pools
    for pool in lava:

        draw.rect(window, ORANGE, pool)

        draw.line(
            window,
            RED,
            (pool.left, pool.top),
            (pool.right, pool.top),
            2
        )

    # Draw coins
    for coin in coins:

        draw.circle(
            window,
            YELLOW,
            coin.center,
            5
        )

    # Draw player
    draw.circle(
        window,
        BLUE,
        player.center,
        player_radius
    )

    # Draw score
    score_text = font1.render(
        "Coins: " + str(score) + "/" + str(total_coins),
        True,
        BLACK
    )

    window.blit(score_text, (5, 5))

    # Draw lives
    lives_text = font1.render(
        "Lives: " + str(lives),
        True,
        BLACK
    )

    window.blit(lives_text, (5, 20))

    # Draw level
    area_text = font1.render(
        "Level: " + str(current_area + 1),
        True,
        BLACK
    )

    window.blit(area_text, (5, 35))

    # Game over
    if game_over:

        game_over_text = font2.render(
            "GAME OVER",
            True,
            RED
        )

        restart_text = font1.render(
            "Press R to Restart",
            True,
            BLACK
        )

        window.blit(
            game_over_text,
            (75, 100)
        )

        window.blit(
            restart_text,
            (100, 135)
        )

    # Win message
    if won:

        win_text = font2.render(
            "YOU WIN!",
            True,
            GREEN
        )

        restart_text = font1.render(
            "Press R to Restart",
            True,
            BLACK
        )

        window.blit(
            win_text,
            (90, 100)
        )

        window.blit(
            restart_text,
            (100, 135)
        )

    # Update screen
    display.update()

pygame.quit()
