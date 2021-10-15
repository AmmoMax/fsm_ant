import math
import sys

import pygame
import random

from fsm import FSM


SIZE_SCREEN = {'x': 400, 'y': 400}
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 100, 0]
BROWN = [128, 0, 0]
GREEN_GRASS = [85, 107, 47]
ANT_SPEED = 10
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
    def __init__(self, *args, game):
        super().__init__(*args)
        self.__catch_leaf = False
        self.brain = FSM()
        self.brain.set_state(self.find_leaf)
        self.game = game

    def common_run(self, obj_x, obj_y):
        if self.x < obj_x:
            self.x += ANT_SPEED
        elif self.x > obj_x:
            self.x -= ANT_SPEED

        if self.y < obj_y:
            self.y += ANT_SPEED
        elif self.y > obj_y:
            self.y -= ANT_SPEED

    def find_leaf(self):
        leaf_x = self.game.leaf.x
        leaf_y = self.game.leaf.y
        self.common_run(leaf_x, leaf_y)
        if self.get_distance(leaf_x, leaf_y) < 5:
            self.brain.set_state(self.go_home)

    def go_home(self):
        anthill_x = self.game.anthill.x
        anthill_y = self.game.anthill.y
        self.common_run(anthill_x, anthill_y)
        if self.get_distance(anthill_x, anthill_y) < 5:
            self.brain.set_state(self.find_leaf)

    def get_distance(self, target_x, target_y):
        dist = math.sqrt((abs(target_x - self.x)) ^ 2 + abs((target_y - self.y) ^ 2))
        return dist

    def catch_leaf_switcher(self):
        if self.__catch_leaf:
            self.__catch_leaf = False
        else:
            self.__catch_leaf = True

    @property
    def catch_leaf(self):
        return self.__catch_leaf

    def update(self, *args, **kwargs):
        self.brain.update(*args, **kwargs)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = self.__get_screen()
        self.ant = self.__get_ant()
        self.leaf = self.__get_leaf()
        self.anthill = self.__get_anthill()

    def __get_screen(self):
        pygame.display.set_caption('Ant FSM')
        screen = pygame.display.set_mode([SIZE_SCREEN.get('x'), SIZE_SCREEN.get('y')])
        return screen

    def intersect(self, x1, y1, size1, x2, y2, size2):
        if x1 > x2 - size1 and x1 < x2 + size1 and y1 > y2 - size2 and y1 < y2 +size2:
            return True
        return False

    def __get_ant(self):
        ant = Ant(50, 50, 10, self.screen, BLACK, game=self)
        return ant

    def __get_leaf(self):
        leaf_x = random.randint(1, 400)
        leaf_y = random.randint(1, 400)
        leaf = Leaf(leaf_x, leaf_y, 10, self.screen, GREEN)
        return leaf

    def __get_anthill(self):
        anthill = AntHill(random.randint(1, 400), random.randint(1, 400), 10, self.screen, BROWN)
        return anthill

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def get_mouse_pos(self):
        pygame.mouse.set_visible(True)
        pointer = pygame.mouse.get_pos()
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        return pointer

    def run(self):
        while True:
            self.screen.fill(GREEN_GRASS)
            self.check_input()

            # if self.intersect(self.ant.x, self.ant.y, self.ant.size, self.leaf.x, self.leaf.y, self.leaf.size):
            #     self.ant.catch_leaf_switcher()
            #     self.leaf.hide_leaf()
            # if self.intersect(self.ant.x, self.ant.y, self.ant.size, self.anthill.x, self.anthill.y, self.anthill.size):
            #     self.ant.catch_leaf_switcher()
            #     self.leaf.generate_new_coords

            self.ant.render()
            self.leaf.render()
            self.anthill.render()

            self.ant.update()

            # if not self.ant.catch_leaf:
            #     self.ant.update(self.leaf.x, self.leaf.y, 10)
            pygame.display.update()
            pygame.time.delay(150)


if __name__ == '__main__':
    game = Game()
    game.run()
