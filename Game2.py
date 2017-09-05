import pygame
import Shapes
from random import randint

pygame.init()

############### COLOR CONSTANTS ######################################

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

dullRed = (237, 49, 74)
coolBlue = (49, 205, 237)
darkBlue = (0, 39, 158)
purple1 = (91, 61, 211)

#####################################################################


######## METHOD TO GENERATE RANDOM ENEMY TRIANGLES ##############

def generateEnemies(number):

    for x in range(1, number):
        # eqTriangle(xpos,y,pos,xspeed,yspeed,width, color)
        new_enemy = Shapes.eqTriangle(randint(1, resolution_x), randint(1, resolution_y), randint(-10, 10), randint(-10, 10), randint(20, 50), green)
        enemy_list.append(new_enemy)


###########################################################

####################  VARIABLES #########################

direction = ""
gameExit = False
game_Ended = False

resolution_x = 1280
resolution_y = 720


player_Block = Shapes.Block(300, 300, 0, 0, 30, 30, blue)

enemy_list = []
bullet_list = []

enemy_collide_chk = []
block_collide_chk = []

rotAngle = 0
gameOver = False

score = 0
font = pygame.font.SysFont("comicsansms", 32)   # font for displaying score


generateEnemies(10)     # Concept is to generate 10 enemies when the game starts then keep on adding more every few seconds


all_sprites_list = pygame.sprite.Group()       # player block and bullets in this list
all_sprites_enemy_list = pygame.sprite.Group()  # Enemy triangles in this list


gameDisplay = pygame.display.set_mode((resolution_x, resolution_y))
pygame.display.set_caption('Game1')
time1 = pygame.time.Clock()


for i in enemy_list:
    all_sprites_enemy_list.add(i)

all_sprites_list.add(player_Block)


##################### METHODS ######################################

def fire(circle, block, dir):  # fire bullets from the block

    if dir == 'right':
        circle.rect.x = block.rect.x + (block.width) - circle.radius
        circle.rect.y = block.rect.y + int(block.height / 2) - circle.radius
        circle.moveRight(20)

    elif dir == 'left':
        circle.rect.x = block.rect.x - circle.radius
        circle.rect.y = block.rect.y + int(block.height / 2) - circle.radius
        circle.moveLeft(20)

    elif dir == 'up':
        circle.rect.x = block.rect.x + int(block.width / 2) - circle.radius
        circle.rect.y = block.rect.y - circle.radius
        circle.moveUp(20)

    elif dir == 'down':
        circle.rect.x = block.rect.x + int(block.width / 2) - circle.radius
        circle.rect.y = block.rect.y + (block.height) - circle.radius
        circle.moveDown(20)


def moveShape(shape):

    shape.rect.x += shape.x_speed
    shape.rect.y += shape.y_speed


def boundryCheckBlock(shape):
    if (shape.rect.x + shape.width) >= resolution_x:
        shape.rect.x = resolution_x - shape.width

    elif (shape.rect.x) <= 0:
        shape.rect.x = 0

    if (shape.rect.y + shape.height) >= resolution_y:
        shape.rect.y = resolution_y - shape.height

    elif (shape.rect.y) <= 0:
        shape.rect.y = 0


def BoundryCheckTri(shape):
    if (shape.rect.x >= resolution_x) or (shape.rect.x <= 0 - shape.sideLength):
        shape.moveReverseSide()

    if (shape.rect.y >= resolution_y) or (shape.rect.y <= 0 - shape.sideLength):
        shape.moveReverseTop()


def stopEverything():
    for i in enemy_list:
        i.x_speed = 0
        i.y_speed = 0

    player_Block.x_speed = 0
    player_Block.y_speed = 0

    global game_Ended
    game_Ended = True


def getFontSurfandRect(fontType, size, text, color):

    font = pygame.font.SysFont(fontType, size)
    fontSurface = font.render((text), True, color)
    fontRect = fontSurface.get_rect()

    return fontSurface, fontRect


def playAgain():

    global game_Ended
    global gameOver
    global enemy_list

    game_Ended = False
    gameOver = False

    player_Block.rect.x = 200
    player_Block.rect.y = 200

    for i in enemy_list:
        i.x_speed = randint(-10, 10)
        i.y_speed = randint(-10, 10)

        if (150 < i.rect.x < 270):         # check if enemy does not spawn in the same place as the block
            i.rect.x = 300


def gameOverMessage():     # All the functionality of the game over screen here

    grey_rect_width = resolution_x - 50           # gameover transparent grey background is a little shorter from the borders on all 4 sides
    grey_rect_height = resolution_y - 50

    s = pygame.Surface((grey_rect_width, grey_rect_height))

    s.set_alpha(60)
    gameDisplay.blit(s, (25, 25))

    gameOverText, textRect = getFontSurfandRect("Bauhaus 93", 90, "Game Over", dullRed)

    text_x_pos = (grey_rect_width - textRect.width) / 2
    text_y_pos = (grey_rect_height - textRect.height) / 2

    button_x_pos = text_x_pos + 50
    button_y_pos = text_y_pos + textRect.height
    button_width = textRect.width - 100
    button_height = 50

    # -----------------

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if (button_x_pos < mouse[0] < button_x_pos + button_width) and (button_y_pos < mouse[1] < button_y_pos + button_height):
        pygame.draw.rect(gameDisplay, coolBlue, [button_x_pos, button_y_pos, button_width, button_height])
        button_text = getFontSurfandRect("Bauhaus 93", 37, "Play Again", white)

        if click[0]:
            playAgain()

    else:
        pygame.draw.rect(gameDisplay, purple1, [button_x_pos, button_y_pos, button_width, button_height])
        button_text = getFontSurfandRect("Bauhaus 93", 37, "Play Again", black)

    gameDisplay.blit(button_text[0], (button_x_pos + button_width / 4.2, button_y_pos + 2))
    gameDisplay.blit(gameOverText, (text_x_pos, text_y_pos))


############### EVENT LOOP ####################

while not gameExit:

    for event in pygame.event.get():
        # print(event)

        if event.type == pygame.QUIT:
            gameExit = True

        if not game_Ended:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_Block.moveLeft(15)
                    direction = 'left'

                if event.key == pygame.K_RIGHT:
                    player_Block.moveRight(15)
                    direction = 'right'

                if event.key == pygame.K_UP:
                    player_Block.moveUp(15)
                    direction = 'up'

                if event.key == pygame.K_DOWN:
                    player_Block.moveDown(15)
                    direction = 'down'

                if event.key == pygame.K_SPACE:

                    if direction:      # direction string is set i.e user has not pressed space before moving to prevent drawing bullet at 0,0
                        x = Shapes.Circle(0, 0, 0, 0, 10, red)
                        all_sprites_list.add(x)

                        bullet_list.append(x)
                        fire(x, player_Block, direction)

            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT) or (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
                    player_Block.stop()


####################### COLLISION DETECTION  #############################

    for i in bullet_list:
        moveShape(i)

        enemy_collide_chk = pygame.sprite.spritecollide(i, all_sprites_enemy_list, True)

        for j in enemy_collide_chk:
            enemy_list.remove(j)
            score += 1

        if i.rect.x > resolution_x or (i.rect.x + i.radius * 2) < 0 or i.rect.y > resolution_y or (i.rect.y + i.radius * 2) < 0:
            bullet_list.remove(i)               # Destroy the bullet object once it goes offscreen
            all_sprites_list.remove(i)

    block_collide_chk = pygame.sprite.spritecollide(player_Block, all_sprites_enemy_list, False)

    if block_collide_chk:
        stopEverything()
        gameOver = True
        # score = 0


######################### MOVEMENT ########################################

    moveShape(player_Block)

    boundryCheckBlock(player_Block)

    for i in enemy_list:
        i.rotateTriangle(rotAngle)
        moveShape(i)
        BoundryCheckTri(i)

    if rotAngle <= 360:
        rotAngle += 4
    else:
        rotAngle = 0


#####################  GRAPHICS RENDERING (DRAWING IN EVERY FRAME) ##############################

    gameDisplay.fill(white)

    all_sprites_enemy_list.update()
    all_sprites_enemy_list.draw(gameDisplay)  # draw all the sprites in the list at once

    all_sprites_list.update()
    all_sprites_list.draw(gameDisplay)  # draw all the sprites in the list at once

    score_surface = font.render('Score: ' + '{}'.format(score), True, black)
    gameDisplay.blit(score_surface, (resolution_x - score_surface.get_width() - 20, 0))

    if gameOver:
        gameOverMessage()

    pygame.display.update()

    time1.tick(60)        # Framerate

########################################################################

pygame.quit()

quit()
