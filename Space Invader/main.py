import pygame
import random
import math
from pygame import mixer
import time
import threading

# Initialise pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("Background1.jpg")

# Background music
mixer.music.load("background.wav")
mixer.music.play(-1)  # -1 makes it play infinitely


# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("spaceship2.png")
playerX = 368  # Not exactly in centre bc of images width
playerY = 460  # Around the bottom of the screen
playerX_change = 0
VELOCITY = 1.5

# Enemy.
EnemyImg = []
enemyX = []
enemyY = []
enemyVELOCITY = []
enemyX_change = []
enemyY_change = []
numEnemies = 5

# "Spawning" multiple enemies using a list
for i in range(numEnemies + 1):
    EnemyImg.append(pygame.image.load("Enemy.png"))
    enemyX.append(random.randint(0, 730))
    enemyY.append(random.randint(5, 120))
    enemyVELOCITY = 0.5
    enemyX_change.append(enemyVELOCITY)
    enemyY_change = 30

# Bullet
bullet = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 460
bulletVELOCITY = 4
bulletY_change = bulletVELOCITY
bullet_state = "ready"  # Ready is not visible. Fire is firing

# Score
score = 0
# You can add more fonts by downloading them online and adding them to folder
font = pygame.font.Font("freesansbold.ttf", 28)
scoreX = 10
scoreY = 575


def game_over_text():
    over_font = pygame.font.Font("freesansbold.ttf", 60)
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 20, y + 10))


def enemy(x, y, i):
    # Blit draws image on the screen/surface
    screen.blit(EnemyImg[i], (x, y))


def player(x, y):
    # Blit draws image on the screen/surface
    screen.blit(playerImg, (x, y))


def spawn_enemy():
    global numEnemies
    numEnemies += 1
    EnemyImg.append(pygame.image.load("Enemy.png"))
    enemyX.append(random.randint(0, 730))
    enemyY.append(random.randint(5, 120))
    enemyX_change.append(enemyVELOCITY)
    print(numEnemies)

# Interval for extra enemies
interval = 10


def repeat_function():
    while True:
        spawn_enemy()
        time.sleep(interval)


# Create and start a separate thread for the repeating function
thread = threading.Thread(target=repeat_function)
thread.start()


# Using distance formula to calculate distance between enemies and bullets
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 32:
        return True
    else:
        return False


running = True

#  Keeps window open. This is a game loop
while running:

    # Background/Screen
    # RGB Values
    screen.fill((0, 0, 10))

    # Background Image
    screen.blit(background, (0, 0))

    # Closes program when we quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke check for player. Check if it's right ot left then change x value
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = VELOCITY
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change = -VELOCITY
            # Space check for bullets
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a or
                    event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                playerX_change = 0

    # implementing position change
    playerX += playerX_change

    # setting player boundaries
    if playerX <= 0:
        playerX = 0

    elif playerX >= 768:
        playerX = 768

    # Enemy Movement
    for i in range(numEnemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(numEnemies):
                enemyY[j] = 2000
                playerY = 2000
            game_over_text()
            mixer.music.stop()
            break

        enemyX[i] += enemyX_change[i]
        # Square brackets to specify position in index for/of each enemy
        if enemyX[i] <= 0:
            enemyX_change[i] = enemyVELOCITY
            enemyY[i] += enemyY_change
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemyVELOCITY
            enemyY[i] += enemyY_change

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 460
            bullet_state = "ready"
            score += 1
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()

            # "Respawning" enemy to a random location when shot
            enemyX[i] = random.randint(0, 730)
            enemyY[i] = random.randint(5, 120)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += -bulletY_change
        if bulletY <= 0:
            bulletY = 460
            bullet_state = "ready"

    show_score(scoreX, scoreY)
    player(playerX, playerY)

    # Have to update display after every change to the screen
    pygame.display.update()
