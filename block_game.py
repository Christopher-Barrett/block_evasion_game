import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (0,0,0)
player_size = 50
player_1 = [WIDTH/2, HEIGHT-2*player_size]

enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]

SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

def set_level(score, SPEED):
    if score < 10:
        SPEED = 6
    elif score <20:
        SPEED = 7
    elif score < 30:
        SPEED = 8
    else:
        SPEED = 15
    return SPEED

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.2:
        x_pos = random.randint(0, WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemies_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def collision_check(enemy_list, player_1):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_1):
            return True
        return False    


def detect_collision(player_1, enemy_pos):
    p_x = player_1[0]
    p_y = player_1[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x <(e_x+enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y <(e_y+enemy_size)):
            return True
    return False

while not game_over:

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            x = player_1[0]
            y= player_1[1]

            if event.key == pygame.K_LEFT:
                x -= player_size                
            elif event.key == pygame.K_RIGHT:
                x += player_size

            player_1 = [x,y]

    screen.fill(BACKGROUND_COLOR)

    #updating pos of enemy
    # if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
    #     enemy_pos[1] += SPEED
    # else:
    #     enemy_pos[0] = random.randint(0, WIDTH-enemy_size) 
    #     enemy_pos[1] = 0

    if detect_collision(player_1, enemy_pos):
        game_over = True
        # break

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    SPEED = set_level(score, SPEED)

    text = "Score:" + str(score)
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label, (WIDTH-200, HEIGHT-40))
    


    if collision_check(enemy_list, player_1):
        game_over = True
        # break

    draw_enemies(enemy_list)    
    pygame.draw.rect(screen, GREEN, (player_1[0], player_1[1], player_size, player_size) )

    clock.tick(20)

    pygame.display.update()