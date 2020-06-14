import sys
import pygame
import random
import math

#Initialize pygame
pygame.init()

#Creates the screen
screen = pygame.display.set_mode((800,600))

#Background
background = pygame.image.load("background.png")

#Title and Icon 
pygame.display.set_caption("Mars Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('space_defender.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemeyImg = []
enemeyX = [] 
enemeyY = []
enemeyX_change = []
enemeyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemeyImg.append(pygame.image.load('space_invader.png'))
    enemeyX.append(random.randint(0,735))
    enemeyY.append(random.randint(50,150))
    enemeyX_change.append(2)
    enemeyY_change.append(10)

#Bullet 

#Ready - You can't see the bullet on the screen
#Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX =  0
bulletY =  480
bulletY_change = 5
bullet_state = "ready"

#Score tracker
score_value = 0
font = pygame.font.Font('Done Perfectly.ttf',40)
textX = 10
textY = 10

#Game Over
over_font = pygame.font.Font("Done Perfectly.ttf",64)

def game_over():
    over_render = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_render,(200,250))

def show_score(x,y):
    score = font.render("Score: " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def player(x,y):
    screen.blit(playerImg,(x, y))
    

def enemy(x,y,i):
    screen.blit(enemeyImg[i],(x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemeyX,enemeyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemeyX-bulletX,2) + math.pow(enemeyY-bulletY,2))
    if distance<27:
        return True
    else:
        return False



#Game Loop
running = True
while running:

    #RGB background
    #screen.fill((0,0,0))

    #Background Image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3             
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:    
                playerX_change = 0
            

    #Setting boundaries for the spaceship
    playerX += playerX_change
    if playerX>736:
        playerX = 736
    if playerX<0:
        playerX = 0

    #Setting boundaries for the invader

    for i in range(num_of_enemies):

        if enemeyY[i] > 440:
            for j in range(num_of_enemies):
                enemeyY[j] = 2000
            game_over()
            break

        enemeyX[i] += enemeyX_change[i]
        if enemeyX[i]>736:
            enemeyX_change[i] = -2
            enemeyY[i] += enemeyY_change[i]
        if enemeyX[i]<0:
            enemeyX_change[i] = 2 
            enemeyY[i] += enemeyY_change[i]

        #Collsion
        collision = isCollision(enemeyX[i],enemeyY[i],bulletX,bulletY)
        if collision is True:
            bullet_state = "ready"
            bulletY = 480   
            score_value += 1
            enemeyX[i] =  random.randint(0,735)
            enemeyY[i] = random.randint(50,150)
        enemy(enemeyX[i],enemeyY[i],i)

    #Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -=5
    if bulletY<0:
        bullet_state = "ready"
        bulletY = 480


    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()
