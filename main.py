#importing all neccesary libraries
import pygame, sys, random
from spritesheets.spritesheet import Spritesheet
from pygame.locals import *


#initializing pygame clock and text font families
clock = pygame.time.Clock()
pygame.init()
pygame.font.init()

defaultfont = pygame.font.SysFont('default',23)
#setting global variable default font to system default font with fontsize 23
GAMEWINDOW_SIZE = (1200,800)
VIEWPORT_SIZE = (600,400)
gamewindow = pygame.display.set_mode(GAMEWINDOW_SIZE)
#setting the pygame display to the size of GAMEWINDOW_SIZE
display = pygame.Surface(VIEWPORT_SIZE)
#setting the pygame surface to the size of VIEWPORT_SIZE


pygame.display.set_caption("Gold Mine")
#setting the caption of the game window to Gold Mine

#Initializing global variables
gameloopiter = 0 #game loop counter
right_pressed = left_pressed = up_pressed = down_pressed = False #all keys initialized as false
velocity = [0,0] #initializing velocity to be 0,0
true_scroll = [0,0]
building_tiles_x = [6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28] #declaring array for tiles in the game map where the player is not allowed to break tiles
map_width = 30
map_height_chunk = 100 #declaring the chunk size, if the player reaches 100y a new chunk will be generated
grasslevel = 5
game_map = []
seed_map = []
last_player_blit = 'left' #initializing the last displayed image to be the 'left' version of the player sprite
animation_iter = 1
inventory = [0, 0, 0, 0, 0, 0] #initializing the inventory to be empty

#This function procedurally and randomly generates the map using the built in .random() function from python, 
#based on what the value of the random number is, an element in the 'game_map' 2d array will get a certain value in that position defining
#the type of tile that will be blitted in that space
def generate_map(path):
    map = [[0] * map_width for i in range(map_height_chunk)]

    for h in range(0, map_height_chunk):
        for w in range(0, map_width):
            if h > grasslevel:
                r = random.random()
                if r > 0.75:  # ore or blank tile
                    if r > 0.98:
                        map[h][w] = 5
                    elif r > 0.95:
                        map[h][w] = 4
                    elif r > 0.90:
                        map[h][w] = 3
                    elif r > 0.75:
                        map[h][w] = 0
                else:  # dirt tile
                    map[h][w] = 1
            elif h == grasslevel:  # grass tile
                map[h][w] = 2
            elif h < grasslevel:
                map[h][w] = 0

    maptxtfile = open(path, 'w') #opening the text file in which the map is stored

    for h in range(0, map_height_chunk): #writing the map to the text file
        for w in range(0, map_width):
            maptxtfile.write(str(map[h][w]))
        maptxtfile.write('\n')

    maptxtfile.close()

#this function saves the current map 2d array to the map text file
def save_map(path, game_map): 
    maptxtfile = open(path, 'w')

    for h in range(0, len(game_map)):
        for w in range(0, len(game_map[0])):
            maptxtfile.write(str(game_map[h][w]))
        maptxtfile.write('\n')

    maptxtfile.close()

#this function loads the map in the map text file in to the global map 2d array
def load_map(path):
    f = open(path,'r')
    data = f.read()
    f.close()
    game_map1 = []
    seed_map1 = []
    data = data.split('\n')
    for row in range(0, len(data)):
        game_map1.append(list(data[row]))
        seed_map1.append(list(data[row]))

    game_map2 = [x for x in game_map1 if x != []]
    seed_map2 = [x for x in seed_map1 if x != []]
    return game_map2, seed_map2

game_map, seed_map = load_map('map.txt')

#this function generates a chunk of 100 tiles similarly to the generate_map function and appends it to the bottom of the current 2d map array
def generate_chunk(height, width):
    map_chunka = [[0] * width for i in range(height)]
    map_chunkb = [[0] * width for i in range(height)]

    for h in range(0, height):
        for w in range(0, width):
            r = random.random()
            if r > 0.75:  # ore or blank tile
                if r > 0.98:
                    map_chunka[h][w] = '5'
                    map_chunkb[h][w] = '5'
                elif r > 0.95:
                    map_chunka[h][w] = '4'
                    map_chunkb[h][w] = '4'
                elif r > 0.90:
                    map_chunka[h][w] = '3'
                    map_chunkb[h][w] = '3'
                elif r > 0.75:
                    map_chunka[h][w] = '0'
                    map_chunkb[h][w] = '0'
            else:  # dirt tile
                map_chunka[h][w] = '1'
                map_chunkb[h][w] = '1'

    return map_chunka, map_chunkb

#this function loads sprites using the spritesheet class in spritesheet.py
def load_sprites(spritesheet, filenames, r, g, b, scalex, scaley):
    arr = []
    for x in filenames:
        arr.append(spritesheet.parse_sprite(x + '.png', r, g, b))

    for i in range(0, len(arr)):
        arr[i] = pygame.transform.scale(arr[i], (scalex, scaley))

    return arr

#loading all images from the spritesheets in the spritesheets folder using the load_sprites and Spritesheet class
buildings_spritesheet = Spritesheet('spritesheets/buildings')
buildings = [buildings_spritesheet.parse_sprite('factory.png', 255, 255, 255), buildings_spritesheet.parse_sprite('garage.png', 255, 255, 255),buildings_spritesheet.parse_sprite('gas-station.png', 255, 255, 255)]
buildings[2] = pygame.transform.scale(buildings[2], (120, 120))

player_img = pygame.image.load('sprites/player/version1/player.png').convert()
player_img.set_colorkey((255, 255, 255))
player_img = pygame.transform.scale(player_img, (25, 25))
player_rect = pygame.Rect(100,100,player_img.get_width(),player_img.get_height())

player_drill_animation_spritesheet = Spritesheet('spritesheets/player')
player_drill_left = load_sprites(player_drill_animation_spritesheet, ['left1', 'left2'], 0,0,0,37, 27)
player_drill_right = load_sprites(player_drill_animation_spritesheet, ['right1', 'right2'], 0, 0,0,37,27)
player_drill_bottom = load_sprites(player_drill_animation_spritesheet, ['down1', 'down2'], 0, 0, 0, 25, 37)
player_drive_left = load_sprites(player_drill_animation_spritesheet, ['left2', 'left2-odd'], 0, 0, 0, 37, 27)
player_drive_right = load_sprites(player_drill_animation_spritesheet, ['right2', 'right2-odd'], 0, 0, 0, 37, 27)
player_fly_left = load_sprites(player_drill_animation_spritesheet, ['flyleft1', 'flyleft2', 'flyleft3'], 0, 0, 0, 37, 37)
player_fly_right = load_sprites(player_drill_animation_spritesheet, ['flyright1', 'flyright2', 'flyright3'], 0, 0, 0, 37, 37)

terrain_spritesheet = Spritesheet('spritesheets/terrain')
grass = load_sprites(terrain_spritesheet, ['grass1', 'grass2', 'grass3', 'grass4', 'grass5', 'grass6'], 255, 255, 255, 35, 35)
dirt = load_sprites(terrain_spritesheet, ['dirt1', 'dirt2', 'dirt3'], 255, 255, 255, 35, 35)
copper = load_sprites(terrain_spritesheet, ['copper1', 'copper2', 'copper3', 'copper4', 'copper5', 'copper6', 'copper7', 'copper8', 'copper9'], 255, 255, 255, 35, 35)
iron = load_sprites(terrain_spritesheet, ['iron1', 'iron2', 'iron3', 'iron4', 'iron5', 'iron6', 'iron7', 'iron8', 'iron9'], 255, 255, 255, 35, 35)
gold = load_sprites(terrain_spritesheet, ['gold1', 'gold2', 'gold3', 'gold4', 'gold5', 'gold6', 'gold7', 'gold8', 'gold9'], 255, 255, 255, 35, 35)

#background images are too large to put into a spritesheet
bg0 = pygame.image.load('sprites/backgrounds/aboveground/0.png').convert()
bg0 = pygame.transform.scale(bg0, (2000, 2000))
bg1 = pygame.image.load('sprites/backgrounds/aboveground/1_bg.png').convert()
bg1 = pygame.transform.scale(bg1, (1000, 500))
bg2 = pygame.image.load('sprites/backgrounds/aboveground/2_bg.png').convert()
bg2 = pygame.transform.scale(bg2, (1000, 300))
bg3 = pygame.image.load('sprites/backgrounds/aboveground/3_bg.png').convert()
bg3 = pygame.transform.scale(bg3, (1000, 260))
bg4 = pygame.image.load('sprites/backgrounds/aboveground/4_bg.png').convert()
bg4 = pygame.transform.scale(bg4, (1000, 260))
bg5 = pygame.image.load('sprites/backgrounds/aboveground/5.png').convert()
bg5 = pygame.transform.scale(bg5, (1000, 225))
bg0.set_colorkey((255, 255, 255))
bg1.set_colorkey((238,224,210))
bg2.set_colorkey((225,181,147))
bg3.set_colorkey((121,109,77))
bg4.set_colorkey((156,122,93))
bg5.set_colorkey((255, 255, 255))
backgrounds = [bg0, bg1, bg2, bg3, bg4, bg5]
#parralax effect on background images the numbers < 1 are the multipliers by which they are supposed to move in correlation with player movement
background_objects = [[0.4, 0.5, [-500,-1600,1000,1000]],[0.5, 0.6, [0,0,1000,1000]],[0.6, 0.7,[0,0,1000,1000]],[0.75, 0.8,[0,0,1000,1000]],[0.85, 0.9,[0,0,1000,1000]], [0.9, 0.97,[0,0,1000,1000]]]

#underground background
undergroundbg = pygame.image.load('sprites/backgrounds/underground/3.png').convert()
undergroundbg = pygame.transform.scale(undergroundbg, (1100, 450))
undergroundbg_obj = [1, 1, [0,175,1000,1000]]

#function that returns a list of colliding tiles with the player for rectangle to rectangle collision
def collision_test(rect,tiles, tile_xy):
    hit_list = []
    hit_list_xy = []
    xycount = 0
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
            hit_list_xy.append(tile_xy[xycount])
        xycount += 1
    return hit_list, hit_list_xy

#function that adds constraints to player movement and changes player position based on user input
def move(rect,movement,tiles, tile_xy):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list, hit_list_xy = collision_test(rect,tiles, tile_xy)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list, hit_list_xy = collision_test(rect,tiles,tile_xy)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types, hit_list, hit_list_xy

#function that returns camera movement by showing the section of VIEWPORT_SIZE in the GAMEWINDOW of pygame,
#it is done with arbituary divisions to have a lagging behind effect or, dragging effect.
def camera_movement():
    if VIEWPORT_SIZE[0]/2 < player_rect.x < ((len(game_map[0]) * grass[0].get_width()) - VIEWPORT_SIZE[0] / 2 - player_img.get_width()):
        true_scroll[0] += (player_rect.x-true_scroll[0]-(VIEWPORT_SIZE[0]/2)+(player_img.get_width()/2))/15
    elif player_rect.x < VIEWPORT_SIZE[0]/2:
        true_scroll[0] += (VIEWPORT_SIZE[0]/2-true_scroll[0]-(VIEWPORT_SIZE[0]/2)+(player_img.get_width()/2))/15
    elif player_rect.x > ((len(game_map[0]) * grass[0].get_width()) - VIEWPORT_SIZE[0]/2 - player_img.get_width()):
        true_scroll[0] += (((len(game_map[0]) * grass[0].get_width()) - VIEWPORT_SIZE[0]/2 - player_img.get_width())-true_scroll[0]-(VIEWPORT_SIZE[0]/2)+(player_img.get_width()/2))/15

    true_scroll[1] += (player_rect.y - true_scroll[1] - (VIEWPORT_SIZE[1] / 2) + (player_img.get_height() / 2)) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    return scroll

#function that blits all sprites according to the current viewport and scroll that is defined by the player position in the gamewindow
def blit_sprites(scroll):
    counter = 0
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[2][0] - scroll[0] * background_object[0],
                               background_object[2][1] - scroll[1] * background_object[1], background_object[2][2],
                               background_object[2][3])
        display.blit(backgrounds[counter], obj_rect)
        counter += 1

    for i in range(0,int(len(game_map)/100)*8):  # 8 = map height
        undergroundbg_rect = pygame.Rect(undergroundbg_obj[2][0] - scroll[0] * undergroundbg_obj[0],
                                         undergroundbg_obj[2][1] + (i * 450) - scroll[1] * undergroundbg_obj[1],
                                         undergroundbg_obj[2][2], undergroundbg_obj[2][3])
        display.blit(undergroundbg, undergroundbg_rect)

    display.blit(buildings[0], (500 - scroll[0], 20 - scroll[1], 200, 200))
    display.blit(buildings[1], (840 - scroll[0], 65 - scroll[1], 200, 200))
    display.blit(buildings[2], (200 - scroll[0], 55 - scroll[1], 200, 200))

    tile_rects = []
    tile_xy = []
    y = 0
    dirtiter = 0
    grassiter = 0
    copperiter = 0
    ironiter = 0
    golditer = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if seed_map[y][x] == '1':
                if tile == '1':
                    display.blit(dirt[dirtiter], (
                    x * dirt[dirtiter].get_width() - scroll[0], y * dirt[dirtiter].get_width() - scroll[1]))
                if dirtiter == len(dirt) - 1:
                    dirtiter = 0
                else:
                    dirtiter += 1
            if seed_map[y][x] == '2':
                if tile == '2':
                    display.blit(grass[grassiter], (
                    x * grass[grassiter].get_width() - scroll[0], y * grass[grassiter].get_width() - scroll[1]))
                if grassiter == len(grass) - 1:
                    grassiter = 0
                else:
                    grassiter += 1
            if seed_map[y][x] == '3':
                if tile == '3':
                    display.blit(copper[copperiter], (
                    x * copper[copperiter].get_width() - scroll[0], y * copper[copperiter].get_width() - scroll[1]))
                if copperiter == len(copper) - 1:
                    copperiter = 0
                else:
                    copperiter += 1
            if seed_map[y][x] == '4':
                if tile == '4':
                    display.blit(iron[ironiter], (
                    x * iron[ironiter].get_width() - scroll[0], y * iron[ironiter].get_width() - scroll[1]))
                if ironiter == len(iron) - 1:
                    ironiter = 0
                else:
                    ironiter += 1
            if seed_map[y][x] == '5':
                if tile == '5':
                    display.blit(gold[golditer], (
                    x * gold[golditer].get_width() - scroll[0], y * gold[golditer].get_width() - scroll[1]))
                if golditer == len(gold) - 1:
                    golditer = 0
                else:
                    golditer += 1
            if tile != '0':
                tile_xy.append((x, y))
                tile_rects.append(pygame.Rect(x * grass[0].get_width(), y * grass[0].get_width(), grass[0].get_width(),
                                              grass[0].get_width()))
            x += 1
        y += 1

    return tile_rects, tile_xy

#function that saves an image of the current screen and fakes a 'drilling' animation by showing two different images
#of the drill in rapid succesion
def drill_animation_loop(orientation, drill_tile):
	pygame.image.save(display, 'animation_loop.jpg')
	currwindow = pygame.image.load('animation_loop.jpg').convert()

	xflip = 1
	if orientation == 'bottom':
		for i in range(0,16):
			xflip = 1 - xflip
			display.blit(currwindow, (0, 0))
			pygame.time.wait(50)
			display.blit(player_drill_bottom[xflip], (player_rect[0] - scroll[0], player_rect[1] - scroll[1]))
			player_rect[1] = player_rect[1]+1
			if player_rect[0] > drill_tile[0]*dirt[0].get_width()+dirt[0].get_width()/6:
				player_rect[0] = -((player_rect[0]-drill_tile[0]*dirt[0].get_width()-dirt[0].get_width()/6)/20)+player_rect[0]
			elif player_rect[0] < drill_tile[0]*dirt[0].get_width()+(dirt[0].get_width()*5/6):
				player_rect[0] = player_rect[0]+((drill_tile[0]*dirt[0].get_width()+(dirt[0].get_width()*5/6)-player_rect[0])/20)
			gamewindow.blit(pygame.transform.scale(display,GAMEWINDOW_SIZE),(0,0))
			pygame.display.update()
			clock.tick(60)
	elif orientation ==  'right':
		for i in range(0,20):
			xflip = 1 - xflip
			display.blit(currwindow, (0, 0))
			pygame.time.wait(50)
			display.blit(player_drill_right[xflip], (player_rect[0] - scroll[0], player_rect[1]-2 - scroll[1]))
			player_rect[0] = player_rect[0]+1
			gamewindow.blit(pygame.transform.scale(display,GAMEWINDOW_SIZE),(0,0))
			pygame.display.update()
			clock.tick(60)
	elif orientation == 'left':
		for i in range(0,20):
			xflip = 1 - xflip
			display.blit(currwindow, (0, 0))
			pygame.time.wait(50)
			display.blit(player_drill_left[xflip], (player_rect[0] - player_img.get_width()/2 - scroll[0], player_rect[1]-2 - scroll[1]))
			player_rect[0] = player_rect[0]-1
			gamewindow.blit(pygame.transform.scale(display,GAMEWINDOW_SIZE),(0,0))
			pygame.display.update()
			clock.tick(60)

#this function removes a specified tile from the map 2d array based on what tile the player is currently colliding with
def remove_tile(player_rect, collisions, collidingtiles, collidingtilesxy):
    curr_closest_tile = collidingtiles[0]
    curr_closest_int = grass[0].get_width()
    curr_closest_xy = collidingtilesxy[0]
    xy_count = 0

    for tile in collidingtiles:
        closecheck = abs(
            (tile[0] + (grass[0].get_width() / 2)) - (player_rect[0] + (player_img.get_width() / 2)))
        if (min(closecheck, curr_closest_int) == closecheck):
            curr_closest_int = closecheck
            curr_closest_tile = tile
            curr_closest_xy = collidingtilesxy[xy_count]
        xy_count += 1

    if down_pressed == True and collisions['bottom'] == True:
        if (curr_closest_xy[0] not in building_tiles_x) or (curr_closest_xy[1] != grasslevel):
        	drill_animation_loop('bottom', curr_closest_xy)
        	inventory[int(game_map[curr_closest_xy[1]][curr_closest_xy[0]])] += 1
        	game_map[curr_closest_xy[1]][curr_closest_xy[0]] = '0'
    elif right_pressed == True and collisions['right'] == True:
        if (curr_closest_xy[0]+1 not in building_tiles_x) or (curr_closest_xy[1]-1 != grasslevel):
       		drill_animation_loop('right', curr_closest_xy)
       		inventory[int(game_map[curr_closest_xy[1] - 1][curr_closest_xy[0] + 1])] += 1
        	game_map[curr_closest_xy[1] - 1][curr_closest_xy[0] + 1] = '0'
    elif left_pressed == True and collisions['left'] == True:
        if (curr_closest_xy[0]-1 not in building_tiles_x) or (curr_closest_xy[1]-1 != grasslevel):
        	drill_animation_loop('left', curr_closest_xy)
        	inventory[int(game_map[curr_closest_xy[1] - 1][curr_closest_xy[0] - 1])] += 1
        	game_map[curr_closest_xy[1] - 1][curr_closest_xy[0] - 1] = '0'

    if curr_closest_xy[1] >= len(seed_map)-10:
        gamechunk, seedchunk = generate_chunk(map_height_chunk, map_width)

        seed_map.extend(seedchunk)
        game_map.extend(gamechunk)

#changes velocity of player based on user input, this gets restrained more in the move() function
def movement(player_rect):
    player_movement = [0, 0]
    if right_pressed:
        velocity[0] += 0.3
    if left_pressed:
        velocity[0] -= 0.3
    if up_pressed:
        velocity[1] -= 0.1
    if down_pressed:
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

    player_rect, collisions, collidingtiles, collidingtilesxy = move(player_rect, player_movement, tile_rects, tile_xy)

    if collisions['top'] == True:
        velocity[1] = 0
    elif collisions['bottom'] == True:
        velocity[1] = 0
        if left_pressed == False and right_pressed == False:
            velocity[0] = 0
        remove_tile(player_rect, collisions, collidingtiles, collidingtilesxy)
    else:
        velocity[0] = velocity[0] * 0.95

    if player_rect.x > ((len(game_map[0]) * grass[0].get_width()) - player_img.get_width()) or player_rect[0] < 0: #limits player movement in X axis, 30 is map width in tiles, 35 is tile width in px
        velocity[0] = 0

#function that blits the player in the correct position taking velocity and the current/ last animation image into account
def blit_player(last_player_blit, velocity, animation_iter):
	if down_pressed == True:
		display.blit(player_drill_bottom[1],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
		#nose dive animation, same as drilling down
	elif up_pressed == True:
		if gameloopiter % 7 == 0:
			if animation_iter < 2:
				animation_iter += 1
			elif animation_iter >= 2:
				animation_iter = 0

		if (right_pressed == True):
			display.blit(player_fly_right[animation_iter],(player_rect.x-scroll[0]-6,player_rect.y-scroll[1]-2))
			last_player_blit = 'right'
		elif left_pressed == True:
			display.blit(player_fly_left[animation_iter],(player_rect.x-scroll[0]-6,player_rect.y-scroll[1]-2))
			last_player_blit = 'left'
		elif left_pressed == False and right_pressed == False:
			if last_player_blit == 'right':
				display.blit(player_fly_right[animation_iter],(player_rect.x-scroll[0]-6,player_rect.y-scroll[1]-2))
			elif last_player_blit == 'left':
				display.blit(player_fly_left[animation_iter],(player_rect.x-scroll[0]-6,player_rect.y-scroll[1]-2))
		#fly animation, left and right
	elif (right_pressed == True) or (last_player_blit == 'right' and left_pressed == False):
		if gameloopiter % 14 == 0 or animation_iter > 1:
			if animation_iter < 1:
				animation_iter += 1
			elif animation_iter >= 1:
				animation_iter = 0

		display.blit(player_drive_right[animation_iter],(player_rect.x-scroll[0]-6,player_rect.y-scroll[1]-2))
		last_player_blit = 'right'
		#drive left animation
	elif (left_pressed == True) or (last_player_blit == 'left' and right_pressed == False):
		if gameloopiter % 14 == 0 or animation_iter > 1:
			if animation_iter < 1:
				animation_iter += 1
			elif animation_iter >= 1:
				animation_iter = 0

		display.blit(player_drive_left[animation_iter],(player_rect.x-scroll[0]-6,player_rect.y-scroll[1]-2))
		last_player_blit = 'left'
		#drive right animation

	return last_player_blit, animation_iter

#function that blits the text on the screen with the defaultfont global variable
def blit_text():
	coppercounter = defaultfont.render('copper: ' + str(inventory[3]), False, (0,0,0))
	ironcounter = defaultfont.render('iron: ' + str(inventory[4]), False, (0,0,0))
	goldcounter = defaultfont.render('gold: ' + str(inventory[5]), False, (0,0,0))

	display.blit(coppercounter,(10,10))
	display.blit(ironcounter,(10,25))
	display.blit(goldcounter,(10,40))

#game loop
run = True
while run:
    display.fill((255,255,255))

    scroll = camera_movement()
    tile_rects, tile_xy = blit_sprites(scroll)
    blit_text()
    movement(player_rect)
    last_player_blit, animation_iter = blit_player(last_player_blit, velocity, animation_iter)

    #event listener for user input WASD
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
        if event.type == KEYUP:
            if event.key == 100: #D key
                right_pressed = False
            if event.key == 97: #A key
                left_pressed = False
            if event.key == 119: #W key
                up_pressed = False
            if event.key == 115: #S key
                down_pressed = False

    #updating display at the end of the gameloop
    gamewindow.blit(pygame.transform.scale(display,GAMEWINDOW_SIZE),(0,0))
    pygame.display.update()
    #setting frames per second
    clock.tick(60)

    #condition to prevent integer overflow by setting gameloopiter to 0 after it reaches 9999
    if gameloopiter > 9999: 
    	gameloopiter = 0
    else:
    	gameloopiter += 1

#generate_map('map.txt') #this will generated a new map although is unused in the current version of the game
#save_map('map.txt', game_map) #this will save the current map to map.txt although is unused in the current version of the game

#if run = False and gameloop is not run, pygame quits which closes the game
pygame.quit() 
sys.exit()