import pygame, sys
import random, math
from pygame.locals import *
clock = pygame.time.Clock()
pygame.init()

GAMEWINDOW_SIZE = (1200,800)
VIEWPORT_SIZE = (600,400)
gamewindow = pygame.display.set_mode(GAMEWINDOW_SIZE)
display = pygame.Surface(VIEWPORT_SIZE) #A scaled surface for rendering

pygame.display.set_caption("Gold Mine")

right_pressed = left_pressed = up_pressed = down_pressed = False
velocity = [0,0]
true_scroll = [0,0]

def load_map(path):
    f = open(path,'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    seed_map = []
    for row in data:
        game_map.append(list(row))
        seed_map.append(list(row))
    return game_map, seed_map

game_map, seed_map = load_map('map/map.txt')

player_img = pygame.image.load('sprites/player/player.png').convert()
player_img.set_colorkey((255, 255, 255))
player_img = pygame.transform.scale(player_img, (25, 25))
player_rect = pygame.Rect(100,100,player_img.get_width(),player_img.get_height())

grass_img1 = pygame.image.load('sprites/terrain/grass/bisque/grass1.png')
grass_img1 = pygame.transform.scale(grass_img1, (35, 35))
grass_img2 = pygame.image.load('sprites/terrain/grass/bisque/grass2.png')
grass_img2 = pygame.transform.scale(grass_img2, (35, 35))
grass_img3 = pygame.image.load('sprites/terrain/grass/bisque/grass3.png')
grass_img3 = pygame.transform.scale(grass_img3, (35, 35))
grass_img4 = pygame.image.load('sprites/terrain/grass/bisque/grass4.png')
grass_img4 = pygame.transform.scale(grass_img4, (35, 35))
grass_img5 = pygame.image.load('sprites/terrain/grass/bisque/grass5.png')
grass_img5 = pygame.transform.scale(grass_img5, (35, 35))
grass_img6 = pygame.image.load('sprites/terrain/grass/bisque/grass6.png')
grass_img6 = pygame.transform.scale(grass_img6, (35, 35))
grass = [grass_img1, grass_img2, grass_img3, grass_img4, grass_img5, grass_img6]

dirt_img1 = pygame.image.load('sprites/terrain/dirt/dirt1.png')
dirt_img1 = pygame.transform.scale(dirt_img1, (35, 35))
dirt_img2 = pygame.image.load('sprites/terrain/dirt/dirt2.png')
dirt_img2 = pygame.transform.scale(dirt_img2, (35, 35))
dirt_img3 = pygame.image.load('sprites/terrain/dirt/dirt3.png')
dirt_img3 = pygame.transform.scale(dirt_img2, (35, 35))
dirt = [dirt_img1, dirt_img2, dirt_img3]

bg0 = pygame.image.load('sprites/backgrounds/0.png').convert()
bg0 = pygame.transform.scale(bg0, (2000, 2000))
bg1 = pygame.image.load('sprites/backgrounds/1.png').convert()
bg1 = pygame.transform.scale(bg1, (1000, 500))
bg2 = pygame.image.load('sprites/backgrounds/2_white.png').convert()
bg2 = pygame.transform.scale(bg2, (1000, 300))
bg3 = pygame.image.load('sprites/backgrounds/3_white.png').convert()
bg3 = pygame.transform.scale(bg3, (1000, 260))
bg4 = pygame.image.load('sprites/backgrounds/4_white.png').convert()
bg4 = pygame.transform.scale(bg4, (1000, 260))
bg5 = pygame.image.load('sprites/backgrounds/5.png').convert()
bg5 = pygame.transform.scale(bg5, (1000, 225))
bg0.set_colorkey((255, 255, 255))
bg1.set_colorkey((255, 255, 255))
bg2.set_colorkey((255, 255, 255))
bg3.set_colorkey((255, 255, 255))
bg4.set_colorkey((255, 255, 255))
bg5.set_colorkey((255, 255, 255))
background_objects = [[0.4, 0.5, [-500,-1600,1000,1000]],[0.5, 0.6, [0,0,1000,1000]],[0.67, 0.7,[0,0,1000,1000]],[0.75, 0.8,[0,0,1000,1000]],[0.85, 0.9,[0,0,1000,1000]], [0.9, 0.97,[0,0,1000,1000]]]
backgrounds = [bg0, bg1, bg2, bg3, bg4, bg5]

factory = pygame.image.load('sprites/buildings/factory.png').convert()
factory.set_colorkey((255, 255, 255))
garage = pygame.image.load('sprites/buildings/garage.png').convert()
garage.set_colorkey((255, 255, 255))
gas_station = pygame.image.load('sprites/buildings/gas-station.png').convert()
gas_station.set_colorkey((255, 255, 255))
gas_station = pygame.transform.scale(gas_station, (120, 120))

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

run = True
while run:
    display.fill((255,255,255))

    if (player_rect.x > VIEWPORT_SIZE[0]/2 and player_rect.x < ((len(game_map[0]) * grass_img1.get_width()) - VIEWPORT_SIZE[0]/2 - player_img.get_width())):
        true_scroll[0] += (player_rect.x-true_scroll[0]-(VIEWPORT_SIZE[0]/2)+(player_img.get_width()/2))/15
    elif (player_rect.x < VIEWPORT_SIZE[0]/2):
        true_scroll[0] += (VIEWPORT_SIZE[0]/2-true_scroll[0]-(VIEWPORT_SIZE[0]/2)+(player_img.get_width()/2))/15
    elif (player_rect.x > ((len(game_map[0]) * grass_img1.get_width()) - VIEWPORT_SIZE[0]/2 - player_img.get_width())):
        true_scroll[0] += (((len(game_map[0]) * grass_img1.get_width()) - VIEWPORT_SIZE[0]/2 - player_img.get_width())-true_scroll[0]-(VIEWPORT_SIZE[0]/2)+(player_img.get_width()/2))/15

    true_scroll[1] += (player_rect.y-true_scroll[1]-(VIEWPORT_SIZE[1]/2)+(player_img.get_height()/2))/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    #mousex, mousey = pygame.mouse.get_pos()

    counter = 0
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[2][0]-scroll[0]*background_object[0],background_object[2][1]-scroll[1]*background_object[1],background_object[2][2],background_object[2][3])
        display.blit(backgrounds[counter],obj_rect)
        counter += 1

    display.blit(factory,(500-scroll[0],20-scroll[1], 200, 200))
    display.blit(garage,(840-scroll[0],65-scroll[1], 200, 200))
    display.blit(gas_station,(200-scroll[0],55-scroll[1], 200, 200))

    tile_rects = []
    y = 0
    dirtiter = 0
    grassiter = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if seed_map[y][x] == '1':
                if tile == '1':
                    display.blit(dirt[dirtiter],(x*dirt[dirtiter].get_width()-scroll[0],y*dirt[dirtiter].get_width()-scroll[1]))
                if (dirtiter == len(dirt)-1):
                    dirtiter = 0
                else:
                    dirtiter += 1
            if seed_map[y][x] == '2':
                if tile == '2':
                    display.blit(grass[grassiter],(x*grass[grassiter].get_width()-scroll[0],y*grass[grassiter].get_width()-scroll[1]))
                if (grassiter == len(grass)-1):
                    grassiter = 0
                else:
                    grassiter += 1
            if tile != '0':
                tile_rects.append(pygame.Rect(x*grass_img1.get_width(),y*grass_img1.get_width(),grass_img1.get_width(),grass_img1.get_width()))
            x += 1
        y += 1

    player_movement = [0,0]
    if right_pressed == True:
        velocity[0] += 0.3
    if left_pressed == True:
        velocity[0] -= 0.3
    if up_pressed == True:
        velocity[1] -= 0.1
    if down_pressed == True:
        velocity[1] += 0.2
    if up_pressed == False:
        velocity[1] += 0.3

    if velocity[0] >= 3:
        velocity[0] = 3
    elif velocity[0] <= -3:
        velocity[0] = -3

    if velocity[1] >= 8:
        velocity[1] = 8
    elif velocity[1] <= -5:
        velocity[1] = -5

    player_movement[1] += velocity[1]
    player_movement[0] += velocity[0]

    player_rect,collisions = move(player_rect,player_movement,tile_rects)

    if collisions['top'] == True:
        velocity[1] = 0
    elif collisions['bottom'] == True:
        velocity[1] = 0
        if left_pressed == False and right_pressed == False:
            velocity[0] = 0
    else:
        velocity[0] = velocity[0]*0.95

    display.blit(player_img,(player_rect.x-scroll[0],player_rect.y-scroll[1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == 100: #D key
                right_pressed = True
            if event.key == 97: #A key
                left_pressed = True
            if event.key == 119: #W key
                up_pressed = True
            if event.key == 115: #S key
                down_pressed = True
                game_map[6][3] = 0
        if event.type == KEYUP:
            if event.key == 100: #D key
                right_pressed = False
            if event.key == 97: #A key
                left_pressed = False
            if event.key == 119: #W key
                up_pressed = False
            if event.key == 115: #S key
                down_pressed = False

    gamewindow.blit(pygame.transform.scale(display,GAMEWINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
