
import pygame

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class Shape(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, x_speed, y_speed):
        super().__init__()

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = x_speed
        self.y_speed = y_speed

    def moveLeft(self, speed):
        self.x_speed = -1 * speed
        self.y_speed = 0

    def moveRight(self, speed):
        self.x_speed = speed
        self.y_speed = 0

    def moveUp(self, speed):
        self.y_speed = -1 * speed
        self.x_speed = 0

    def moveDown(self, speed):
        self.y_speed = speed
        self.x_speed = 0

    def moveDiag(self, xspeed, yspeed):
        self.x_speed = xspeed
        self.y_speed = yspeed

    def moveReverseSide(self):
        self.x_speed *= -1
        self.y_speed *= 1

    def moveReverseTop(self):
        self.x_speed *= 1
        self.y_speed *= -1

    def stop(self):
        self.x_speed = 0
        self.y_speed = 0


########### Block Class #################


class Block(Shape):

    def __init__(self, x_pos, y_pos, x_speed, y_speed, width, height, color):
        super().__init__(x_pos, y_pos, x_speed, y_speed)
        self.width = width
        self.height = height

        self.color = color
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()

        self.rect.x = self.x_pos
        self.rect.y = self.y_pos


############# Circle Class ###################


class Circle(Shape):

    def __init__(self, x_pos, y_pos, x_speed, y_speed, radius, color):
        super().__init__(x_pos, y_pos, x_speed, y_speed)
        self.radius = radius

        self.color = color
        self.image = pygame.Surface([2 * radius, 2 * radius])
        self.image.fill(white)
        self.image.set_colorkey(white)

        pygame.draw.circle(self.image, self.color, [self.radius, self.radius], self.radius)

        self.rect = self.image.get_rect()


############# eqTriangle Class ##################

class eqTriangle(Shape):

    def __init__(self, x_pos, y_pos, x_speed, y_speed, sideLength, color):
        super().__init__(x_pos, y_pos, x_speed, y_speed)
        self.sideLength = sideLength

        self.color = color
        self.image = pygame.Surface([self.sideLength, self.sideLength], pygame.SRCALPHA)
        self.image.fill(white)
        self.image.set_colorkey(white)
        self.imageMaster = self.image

        x1_pos = self.sideLength / 2
        y1_pos = 0

        x2_pos = x1_pos - (self.sideLength / 2)        # From calculation of Trignometric formulas for equilateral triangle
        y2_pos = y1_pos + (0.866 * self.sideLength)    # equilateral trangle remaining 2 points are calculated to be below given point

        x3_pos = x1_pos + (self.sideLength / 2)
        y3_pos = y2_pos

        pygame.draw.polygon(self.image, self.color, [[x1_pos, y1_pos], [x2_pos, y2_pos], [x3_pos, y3_pos]])

        self.rect = self.image.get_rect()

        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

    def rotateTriangle(self, angle):

        oldCenter = self.rect.center

        self.image = pygame.transform.rotate(self.imageMaster, angle)

        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
