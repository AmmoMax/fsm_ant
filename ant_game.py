import pygame
import random


pygame.init()

SIZE_SCREEN = {'x': 400, 'y': 400}
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
BROWN = [128, 0, 0]
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

    def hide_leaf(self):
        self.x = -100
        self.y = -100

class AntHill(BaseGameObject):
    def __init__(self, *args):
        super().__init__(*args)
        self.leaf_counter = 0

    def leaf_counter(self):
        self.leaf_counter += 1


class Ant(BaseGameObject):
    def __init__(self, *args):
        super().__init__(*args)
        self.__catch_leaf = False

    def run(self, dest_x, dest_y, speed):
        if self.x < dest_x:
            self.x += speed
        elif self.x > dest_x:
            self.x -= speed

        if self.y < dest_y:
            self.y += speed
        elif self.y > dest_y:
            self.y -= speed

    def catch_leaf_switcher(self):
        if self.__catch_leaf:
            self.__catch_leaf = False
        else:
            self.__catch_leaf = True

    @property
    def catch_leaf(self):
        return self.__catch_leaf

def intersect(x1, y1, size1, x2, y2, size2):
    if x1 > x2 - size1 and x1 < x2 + size1 and y1 > y2 - size2 and y1 < y2 +size2:
        return True
    return False


screen = pygame.display.set_mode([SIZE_SCREEN.get('x'), SIZE_SCREEN.get('y')])

ant = Ant(50, 50, 10, screen, BLACK)
leaf_x = random.randint(1, 400)
leaf_y = random.randint(1, 400)
leaf = Leaf(leaf_x, leaf_y, 10, screen, GREEN)
anthill = AntHill(random.randint(1, 400), random.randint(1, 400), 10, screen, BROWN)


while not game_exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True

    pygame.mouse.set_visible(True)
    pointer = pygame.mouse.get_pos()
    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
    screen.fill(WHITE)

    if intersect(ant.x, ant.y, ant.size, leaf.x, leaf.y, leaf.size):
        ant.catch_leaf_switcher()
        leaf.hide_leaf()
    if intersect(ant.x, ant.y, ant.size, anthill.x, anthill.y, anthill.size):
        ant.catch_leaf_switcher()
        leaf.generate_new_coords

    ant.render()
    leaf.render()
    anthill.render()

    if not ant.catch_leaf:
        ant.run(leaf.x, leaf.y, 10)
    else:
        ant.run(anthill.x, anthill.y, 10)

    pygame.display.update()
    pygame.time.delay(150)

pygame.quit()
