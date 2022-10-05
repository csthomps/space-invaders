import pygame as p
import random
import math
from pygame import mixer

class game()
    # initialize pygame
    p.init()

    # create the screen
    screen = p.display.set_mode((800,600)) # 800p wide, 600p tall

    # background
    background = p.image.load('fun_projects/Space Invaders/background.png')

    # background sound
    mixer.music.load('fun_projects/Space Invaders/background.wav')
    mixer.music.play(-1)

    # title and icon personalization
    p.display.set_caption("Space Invaders")
    icon = p.image.load('fun_projects\Space Invaders\spaceship.png')
    p.display.set_icon(icon)

    # player

    player_img = p.image.load("fun_projects\Space Invaders\spaceship_resized.png")
    # player starting coordinates
    playerX = 370
    playerY = 480
    playerX_change = 0

    def player(x,y):
        screen.blit(player_img, (x, y))

    # enemy
    enemy_img = []
    enemyX = []
    enemyY  = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6
    enemyX_change_constant = 2
    enemyY_change = 40
    for i in range(num_of_enemies):
        enemy_img.append( p.image.load("fun_projects\Space Invaders\enemy.png"))
        # enemy starting coordinates
        enemyX.append( random.randint(0,736))
        enemyY.append( random.randint(0,100))
        enemyX_change.append( random.choice([1,-1]) * enemyX_change_constant)


    def enemy(x,y, i):
        screen.blit(enemy_img[i], (x, y))


    # explosions
    explosion_sound = mixer.Sound("fun_projects\Space Invaders\explosion.wav")
    explosion_img = p.image.load("fun_projects\Space Invaders\explode.png")
    explosion_coords = []
    def display_explosions(explosion_coords):
        if len(explosion_coords) > 0:
            for i in range(len(explosion_coords)):
                screen.blit(explosion_img, (explosion_coords[i][0],explosion_coords[i][1]))
                explosion_coords[i][2] -= 1
                if explosion_coords[i][2] == 0:
                    explosion_coords.pop(i)
                    
                


    # bullet
    bullet_sound = mixer.Sound('fun_projects/Space Invaders/laser.wav')
    bullet_img = p.image.load("fun_projects/Space Invaders/bullet.png")
    # enemy starting coordinates
    bulletX = 0
    bulletY = 480
    bulletY_change = 8
    bullet_ready = True

    def bullet(x,y):
        global bullet_ready
        bullet_ready = False
        screen.blit(bullet_img, (x + 14, y + 10))
        
    def collision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
        return distance
        
    # score
    score_value = 0

    font = p.font.SysFont("times new roman", 20, True, False)

    textX = 10
    textY = 10

    def score_display(score_value, x,y):
        score = font.render("Score :" + str(score_value), True, 'white')
        screen.blit(score, (x, y))

    # game over 
    game_over = False
    game_over_font = p.font.SysFont("Helvetica", 100, True, False)

    def game_over_text(score_value):
        over_text = font.render("GAME OVER | " + "Score: " + str(score_value), True, 'white')
        screen.blit(over_text, (300,250))
        


    # game loop
    running = True
    while running:
        
        # background image
        screen.blit(background, (0,0))
        
        # events
        for event in p.event.get():
            if event.type == p.QUIT: # if hit the close button, end the loop
                running = False 
                
                
            # if keystroke is pressed, check whether it's right or left
            if event.type == p.KEYDOWN:
                if event.key == p.K_LEFT:
                playerX_change = -4
                LEFT = True
                RIGHT = False
                if event.key == p.K_RIGHT:
                playerX_change = 4
                RIGHT = True
                LEFT = False
                if event.key == p.K_UP and bullet_ready == True:
                    bulletX = playerX
                    bullet_sound.play()           
                    bullet(bulletX, bulletY)
                if event.key == p.K_r: # reset game
                    playerX = 370
                    playerY = 480
                    playerX_change = 0
                    enemy_img = []
                    enemyX = []
                    enemyY  = []
                    enemyX_change = []
                    enemyY_change = []
                    num_of_enemies = 6
                    enemyX_change_constant = 2
                    enemyY_change = 40
                    for i in range(num_of_enemies):
                        enemy_img.append( p.image.load("fun_projects\Space Invaders\enemy.png"))
                        # enemy starting coordinates
                        enemyX.append( random.randint(0,736))
                        enemyY.append( random.randint(0,100))
                        enemyX_change.append( random.choice([1,-1]) * enemyX_change_constant)
                    score_value = 0
                    bulletX = 0
                    bulletY = 480
                    bullet_ready = True
                    explosion_coords = []
                    game_over = False
            if event.type == p.KEYUP:
                if (event.key == p.K_LEFT and LEFT) or (event.key == p.K_RIGHT and RIGHT):
                playerX_change = 0
        
        
        # moving player without going off screen
        if playerX + playerX_change < 740 and playerX + playerX_change > 0:
            playerX += playerX_change
        
        # moving enemy side to side wihout going off screen
        if game_over == False:
            for i in range(len(enemyX)):
                
                # game over
                player_collision = collision(enemyX[i], enemyY[i], playerX, playerY)
                if player_collision < 50:
                    game_over_text(score_value)
                    game_over = True
                    break   
                
                enemyX[i] += enemyX_change[i]  
                if enemyX[i] < 0:
                    enemyX[i] = 0
                    enemyX_change[i] = -enemyX_change[i]
                    enemyY[i] += enemyY_change
                if enemyX[i] > 736:
                    enemyX[i] = 736
                    enemyX_change[i] = -enemyX_change[i]
                    enemyY[i] += enemyY_change
                    
                # collision
                if bullet_ready == False:
                    distance = collision(enemyX[i], enemyY[i], bulletX, bulletY)
                    if distance < 27:
                        explosion_sound.play()
                        explosion_coords.insert(0,[enemyX[i], enemyY[i], 100])
                        bulletY = 480
                        bullet_ready = True
                        score_value += 1
                        if score_value % 10 == 0: # increase difficulty every 10 score
                            enemyX_change_constant += .75
                            enemyY_change +=5
                            enemy_img.append( p.image.load("fun_projects\Space Invaders\enemy.png"))
                            # enemy starting coordinates
                            enemyX.append( random.randint(0,736))
                            enemyY.append( random.randint(0,100))
                            enemyX_change.append( random.choice([1,-1]) * enemyX_change_constant)
                        enemyX[i] = random.randint(0,736)
                        enemyY[i] = random.randint(0,100)
                        enemyX_change[i] = random.choice([1,-1]) * enemyX_change_constant    

                enemy(enemyX[i],enemyY[i], i)  
            if bullet_ready == False:
                bulletY -= bulletY_change
                bullet(bulletX,bulletY)
                if bulletY <= 0:
                    bullet_ready = True
                    bulletY = 480
        if game_over:
            game_over_text(score_value)
            
    
        player(playerX,playerY) # draw player on screen
        display_explosions(explosion_coords)
        score_display(score_value, textX, textY)
        p.display.update()
