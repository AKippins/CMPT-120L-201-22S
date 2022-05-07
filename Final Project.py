from cmath import rect
from pickle import FALSE
import pygame 
from sys import exit
from random import randint

def display_score():
# Play Screen Score Display
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = font.render(f'Score: {current_time}',False,(64,64,64))
    score_rectangle = score_surface.get_rect(center =(400,50))
    screen.blit(score_surface,score_rectangle)
    return current_time

# Screen Sizing & Game Defaults
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('campusrun')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
game_active = False
start_time = 0
score = 0

# Sky & Ground Backround Image
sky = pygame.image.load('graphics/Sky.png').convert()
ground = pygame.image.load('graphics/ground.png').convert()

# Enemy Image Load
fox_spawn = pygame.image.load('graphics/fox.png').convert_alpha()
car_spawn = pygame.image.load('graphics/car.png').convert_alpha()

enemy_rect_list = []

# RUNNER Placement
runner= pygame.image.load('graphics/runner.png').convert_alpha()
runner_rectangle = runner.get_rect(midbottom=(80,300))
runner_gravity = 0

# Begginning Screen
runner_screen_rectangle = runner.get_rect(center=(400,200))

game_name = font.render('Campus Run',False,'Orange')
game_name_rectangle = game_name.get_rect(center =(400,120))

message = font.render('Press the SPACE bar to run',False,'Orange')
message_rectangle = message.get_rect(center = (400,280))

# Obstacle Clock
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,900)

# Obstacle Collisions
def collisions(player,enemy):
    if enemy:
        for enemy_rectangle in enemy:
            if player.colliderect(enemy_rectangle):return False
    return True

# Speed of Enemies
def obstacle_movement(enemy_list):
    if enemy_list:
        for enemy_rectangle in enemy_list:
            enemy_rectangle.x -= 7

            # Random Spawn Between Fox & Car
            if enemy_rectangle.bottom == 320:screen.blit(fox_spawn,enemy_rectangle)
            else:screen.blit(car_spawn,enemy_rectangle) 

        enemy_list = [obstacle for obstacle in enemy_list if obstacle.x > -75]

        return enemy_list
    else: return []

# Maintaining & Closing Display
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        #Allows user to click instead of pressing SPACE bar 
        if game_active:
            if event.type==pygame.MOUSEBUTTONDOWN:
                if runner_rectangle.collidepoint(event.pos) and runner_rectangle.bottom >=300:
                    runner_gravity = -20

# Places Runner at the start
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and runner_rectangle.bottom >=300:
                    runner_gravity = -20
        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)
# Randomly Generates Either Fox or Car 
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                enemy_rect_list.append(fox_spawn.get_rect(bottomright=(randint(900,1100),320)))
            else:
                enemy_rect_list.append(car_spawn.get_rect(bottomright=(randint(900,1100),321)))

# SKY & GROUND PLACEMENT 
    if game_active:
        screen.blit(sky,(0,0))
        screen.blit(ground,(0,300))
        score = display_score()

        #RUNNER JUMPING & DAMAGE SENSOR
        runner_gravity += 1.42
        runner_rectangle.y += runner_gravity
        if runner_rectangle.bottom >= 300: runner_rectangle.bottom =300
        screen.blit(runner,runner_rectangle)

    # Enemy Movement
        enemy_rect_list = obstacle_movement(enemy_rect_list)

        #Collision Detection
        game_active = collisions(runner_rectangle,enemy_rect_list)

    else: 
        screen.fill((94,129,162))
        screen.blit(runner,runner_screen_rectangle)
        enemy_rect_list.clear()

#GAME OVER SCREEN 
        again_message = font.render(f'Press SPACE to play again',False, 'Orange')
        again_message_rectangle = again_message.get_rect(center =(400,335))
        score_message = font.render(f'Your Score: {score}',False, 'Orange')
        score_message_rectangle = score_message.get_rect(center = (400,275))
        screen.blit(game_name,game_name_rectangle)

        if score ==0:
            screen.blit(message,message_rectangle)
        else: 
            screen.blit(score_message,score_message_rectangle)
            screen.blit(again_message,again_message_rectangle)


    # GAME CLOCK 
    pygame.display.update()
    clock.tick(60)
    #framerate
