import pygame
pygame.init()

window = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Version 1")

run = True

playerx = 50
playery = 50
speed = 5

while run:
    mousex, mousey = pygame.mouse.get_pos()
    #Fancy one liner for:
    #mousepos = pygame.mouse.get_pos()
    #mousex = mousepos[0]
    #mousey = mousepos[1]

    window.fill((0,0,0))

    #for (int i = 0; i < PASKDPOASKD; i++) {}
    #for i in PASKDPOASKD:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed();

    if keys[pygame.K_LEFT]:
        playerx = playerx - speed
    if keys[pygame.K_RIGHT]:
        playerx = playerx + speed
    if keys[pygame.K_UP]:
        playery = playery - speed
    if keys[pygame.K_DOWN]:
        playery = playery + speed

    pygame.draw.rect(window, (255, 0, 0), (playerx, playery, 30, 30))
        #first param: surface/ window
        #second param: color, in  a tuple (255, 0, 0)
        #third param: rectangle which is an object represented as a tuple like so: (x, y, width, height)

    pygame.display.update()
    #NO CODE IN between update and delay
    pygame.time.delay(16)
