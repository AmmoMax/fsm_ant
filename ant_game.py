import math
import sys
from typing import Tuple

import pygame
import random

from fsm import FSM


SIZE_SCREEN = {'x': 400, 'y': 400}
SIZE_STATUS_BAR = [SIZE_SCREEN.get('x'), 50]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 100, 0]
BROWN = [128, 0, 0]
GREEN_GRASS = [85, 107, 47]
BLOCK_SIZE = 10
MOUSE_THREAT_DISTANCE = 6

# TODO: исправить логику движения муравья т.к. сейчас из за примитивного расчета движения
# попадаются случаи когда муравей и дошел до цели и не дошел
CATCH_DISTANCE = 4
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
            self.x += BLOCK_SIZE
        elif self.x > obj_x:
            self.x -= BLOCK_SIZE

        if self.y < obj_y:
            self.y += BLOCK_SIZE
        elif self.y > obj_y:
            self.y -= BLOCK_SIZE

    def find_leaf(self):
        leaf_x = self.game.leaf.x
        leaf_y = self.game.leaf.y
        self.common_run(leaf_x, leaf_y)
        print(f'dist to leaf: {self.get_distance(leaf_x, leaf_y)}')
        if self.get_distance_mouse() < MOUSE_THREAT_DISTANCE:
            self.brain.set_state(self.run_away)
        if int(self.get_distance(leaf_x, leaf_y)) < CATCH_DISTANCE:
            self.catch_leaf_switcher()
            self.brain.set_state(self.go_home)

        # mouse_pos: Tuple = self.game.get_mouse_pos()
        # mouse_x = mouse_pos[0]
        # mouse_y = mouse_pos[1]
        # distance = self.get_distance(mouse_x, mouse_y)

    def go_home(self):
        anthill_x = self.game.anthill.x
        anthill_y = self.game.anthill.y
        self.common_run(anthill_x, anthill_y)
        if int(self.get_distance(anthill_x, anthill_y)) < CATCH_DISTANCE:
            self.brain.set_state(self.find_leaf)

    def run_away(self):
        self.common_run(0, 0)
        if self.get_distance_mouse() > MOUSE_THREAT_DISTANCE:
            self.brain.set_state(self.find_leaf)

    def get_distance(self, target_x, target_y):
        dist = math.sqrt((abs(target_x - self.x)) ^ 2 + abs((target_y - self.y) ^ 2))
        return dist

    def get_distance_mouse(self):
        mouse_pos: Tuple = self.game.get_mouse_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        distance = self.get_distance(mouse_x, mouse_y)
        print(int(distance))
        return int(distance)

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
        self.window = self.__get_window()
        self.screen = self.__get_screen()
        self.ant = self.__get_ant()
        self.leaf = self.__get_leaf()
        self.anthill = self.__get_anthill()
        self.status_bar = self.__get_status_bar()

    def __get_screen(self) -> pygame.Surface:
        screen = pygame.Surface([SIZE_SCREEN['x'], SIZE_SCREEN['y']])
        return screen

    # def intersect(self, x1, y1, size1, x2, y2, size2):
    #     if x1 > x2 - size1 and x1 < x2 + size1 and y1 > y2 - size2 and y1 < y2 +size2:
    #         return True
    #     return False

    def __get_ant(self):
        ant = Ant(50, 50, 10, self.screen, BLACK, game=self)
        return ant

    def __get_leaf(self):
        leaf_x = random.randint(1, 400)
        leaf_y = random.randint(1, 400)
        leaf = Leaf(leaf_x, leaf_y, 10, self.screen, GREEN)
        return leaf

    def __get_anthill(self):
        anthill = AntHill(random.randint(1, SIZE_SCREEN.get('x')),
                          random.randint(1, SIZE_SCREEN.get('y')), 10, self.screen, BROWN)
        return anthill

    def __get_status_bar(self):
        status_bar = pygame.Surface((SIZE_SCREEN['x'], 50))
        status_bar.fill(WHITE)
        return status_bar

    def __get_window(self):
        pygame.display.set_caption('Ant FSM')
        window = pygame.display.set_mode([SIZE_SCREEN.get('x'), SIZE_SCREEN.get('y') + SIZE_STATUS_BAR[1]])
        return window

    @staticmethod
    def check_input():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    @staticmethod
    def get_mouse_pos():
        pygame.mouse.set_visible(True)
        pointer = pygame.mouse.get_pos()
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        return pointer

    def draw_mouse_circle(self, color=WHITE, radius=30, width=1):
        pygame.draw.circle(self.screen, color, self.get_mouse_pos(), radius, width)

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

            self.draw_mouse_circle()

            self.ant.update()
            if self.ant.catch_leaf:
                self.leaf.generate_new_coords
                self.ant.catch_leaf_switcher()

            self.window.blit(self.status_bar, [0, 0])
            self.window.blit(self.screen, [0, 50])
            pygame.display.update()
            pygame.time.delay(100)


if __name__ == '__main__':
    game = Game()
    game.run()
