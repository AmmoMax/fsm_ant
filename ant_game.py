import pygame
import random


pygame.init()

SIZE_SCREEN = {'x': 400, 'y': 400}
black = [0, 0, 0]
white = [255, 255, 255]
green = [0, 255, 0]
game_exit = False

class BaseGameObject:
    def __init__(self, x, y, size, screen, color):
        self.x = x
        self.y = y
        self.size = size
        self.screen = screen
        self.color = color

    def render(self):
        pygame.draw.rect(self.screen, self.color, [self.x, self.y, self.size, self.size])

class Leaf(BaseGameObject):
    @property
    def generate_new_coords(self):
        self.x = random.randint(1, SIZE_SCREEN.get('x') - self.size)
        self.y = random.randint(1, SIZE_SCREEN.get('y') - self.size)

class Ant(BaseGameObject):
    def run(self, leaf_x, leaf_y, speed):
        if self.x < leaf_x:
            self.x += speed
        elif self.x > leaf_x:
            self.x -= speed

        if self.y < leaf_y:
            self.y += speed
        elif self.y > leaf_y:
            self.y -= speed

def intersect(x1, y1, size1, x2, y2, size2):
    if x1 > x2 - size1 and x1 < x2 + size1 and y1 > y2 - size2 and y1 < y2 +size2:
        return True
    return False

screen = pygame.display.set_mode([SIZE_SCREEN.get('x'), SIZE_SCREEN.get('y')])

ant = Ant(50, 50, 10, screen, black)
leaf_x = random.randint(1, 400)
leaf_y = random.randint(1, 400)
leaf = Leaf(leaf_x, leaf_y, 10, screen, green)

while not game_exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True

    screen.fill(white)

    if intersect(ant.x, ant.y, ant.size, leaf.x, leaf.y, leaf.size):
        leaf.generate_new_coords

    ant.render()
    leaf.render()
    ant.run(leaf.x, leaf.y, 10)
    print(f'ant coords:{ant.x} {ant.y}')
    print(f'leaf coords:{leaf.x} {leaf.y}')

    pygame.display.update()
    pygame.time.delay(150)

pygame.quit()
