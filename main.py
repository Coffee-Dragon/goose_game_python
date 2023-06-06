import pygame
import random
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
pygame.init()


FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE =(0, 0, 255)
COLOR_RED = (255, 0, 0)
FONT = pygame.font.SysFont('Verdana', 40)
IMAGE_PATH = "goose"
PLAYER_IMAGE = os.listdir(IMAGE_PATH)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bgX1 = 0
bgX2 = background.get_width()
bg_move = 3

player_size = (20, 20)
#player = pygame.Surface(player_size)
player = pygame.image.load('player.png').convert_alpha()
#player.fill(COLOR_WHITE)
player_rect = player.get_rect()
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_left =[-4, 0]
player_move_up =[0, -4]

enemies = []
bonuses = []
score = 0
image_index = 0
playing = True

def create_enemy():
    enemy_size = (30, 30)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    #enemy.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (30, 30)
    bonus = pygame.image.load('bonus.png').convert_alpha()
    #bonus.fill(COLOR_RED)
    bonus_rect = pygame.Rect(random.randint(0, WIDTH ), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

while playing:
    FPS.tick(240)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGE[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGE):
                image_index =0

    bgX1 -= bg_move
    bgX2 -= bg_move

    if bgX1 < -background.get_width():
        bgX1 = background.get_width()
    if bgX2 < -background.get_width():
        bgX2 = background.get_width()



    main_display.blit(background, (bgX1, 0))
    main_display.blit(background, (bgX2, 0))


    #main_display.fill(COLOR_BLACK)
    #main_display.blit(background, (0, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    if keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move(player_move_left)
    
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        if player_rect.colliderect(enemy[1]):
            playing = False
    
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])
        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    #enemy_rect = enemy_rect.move(enemy_move)
 
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-100, 20) )
    main_display.blit(player, player_rect)
    #print(len(enemies))
    #main_display.blit(enemy, enemy_rect)
    #player_rect = player_rect.move(player_speed)
    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
    
