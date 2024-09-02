import math

import pyxel
from movement import *
SCROLL_BORDER_X = 80


enemy_list = []
scroll_x = 0
character = None

def spawn_enemy(scroll_left, scroll_right):
    scroll_left = math.ceil(scroll_left / 8)
    scroll_right = math.floor(scroll_right / 8)

    for x in range(scroll_left, scroll_right + 1):
        for y in range(16):
            val = get_tilemap(x, y)
            if val == TILE_ENEMY:
                enemy_list.append(Enemy(x * 8, y * 8))
            elif val == TILE_Tortoise:
                 enemy_list.append(EnemyTortoise(x * 8, y * 8))
            elif val == TILE_Flower:
                enemy_list.append(EnemyFlower(x * 8, y * 8))


class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

    def update(self):
        global scroll_x

        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx = -2

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.dx = 2

        self.dy = min(self.dy + 1, 3)


        if pyxel.btnp(pyxel.KEY_UP):
            if self.y ==  112 or self.y ==  88:
                self.dy = -9

        self.x, self.y, self.dx, self.dy = react_on_collision(
            self.x, self.y, self.dx, self.dy
        )

        if self.x < scroll_x:
            self.x = scroll_x

        if self.y < 0:
            self.y = 0

        self.dx = int(self.dx * 0.8)

        if self.x > scroll_x + SCROLL_BORDER_X:
            last_scroll_x = scroll_x
            scroll_x = min(self.x - SCROLL_BORDER_X, 240 * 8)

            spawn_enemy(last_scroll_x + 128, scroll_x + 127)

    def draw(self):
        pyxel.blt(self.x - scroll_x, self.y-8, 0, 0, 16, 16, 16, 12)
    def draw_small(self):
        pyxel.blt(self.x- scroll_x, self.y, 0, 24, 8, 8, 8, 12)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.direction = 1
        self.alive = True

    def update(self):
        self.dx = self.direction
        self.dy = min(self.dy + 1, 3)

        if check_floor(self.x, self.y + 8) or check_floor(self.x + 7, self.y + 8):
            if self.direction < 0 and (
                check_floor(self.x - 1, self.y + 4)
                or not check_floor(self.x - 1, self.y + 8)
            ):
                self.direction = 1
            elif self.direction > 0 and (
                check_floor(self.x + 8, self.y + 4)
                or not check_floor(self.x + 7, self.y + 8)
            ):
                self.direction = -1

        self.x, self.y, self.dx, self.dy = react_on_collision(
            self.x, self.y, self.dx, self.dy
        )

    def draw(self):
        if self.direction < 0:
            pyxel.blt(self.x - scroll_x, self.y, 0, 24, 0, 8, 8, 0)
        else:
            pyxel.blt(self.x - scroll_x, self.y, 0, 32, 0, 8, 8, 0)


class EnemyTortoise:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.direction = 1
        self.is_falling = True
        self.alive = True

    def update(self):
        self.dx = self.direction
        self.dy = min(self.dy + 1, 3)

        if check_floor(self.x, self.y + 8) or check_floor(self.x + 7, self.y + 8):
            if self.is_falling:
                self.is_falling = False
                if character.x < self.x:
                    self.direction = -1
                else:
                    self.direction = 1
            elif self.direction < 0 and check_floor(self.x - 1, self.y + 4):
                self.direction = 1
            elif self.direction > 0 and check_floor(self.x + 8, self.y + 4):
                self.direction = -1
        else:
            self.is_falling = True

        self.x, self.y, self.dx, self.dy = react_on_collision(
            self.x, self.y, self.dx, self.dy
        )

        if self.y > 128:
            self.x = 64
            self.y = -8

    def draw(self):
        if self.direction < 0:
            pyxel.blt(self.x - 4, self.y, 0, 40, 0, 8, 8, 0)
        else:
            pyxel.blt(self.x - 4, self.y, 0, 48, 0, 8, 8, 0)

class EnemyFlower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rest_time = 0
        self.alive = True

    def update(self):
        if self.rest_time > 0:
            self.rest_time -= 1

        if self.rest_time == 0:
            dx = character.x - self.x
            dy = character.y - self.y
            sq_dist = dx * dx + dy * dy

            if sq_dist < 60 * 60 and sq_dist > 0:
                dist = math.sqrt(sq_dist)
                enemy_list.append(FlowerBullet(self.x, self.y, dx / dist, dy / dist))
                self.rest_time = 60

    def draw(self):
        pyxel.blt(self.x - scroll_x, self.y, 0, 56, 0, 8, 8, 0)


class FlowerBullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.alive = True

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pyxel.blt(self.x - scroll_x, self.y, 0, 64, 0, 8, 8, 0)

flag = 1
class App:
    def __init__(self):


        pyxel.init(128, 128, title="Platform Adventure")

        pyxel.load("assets/design.pyxres")

        pyxel.image(0).rect(0, 8, 24, 8, 12)

        global character
        character = Character(0, 110)

        spawn_enemy(0, 127)

        pyxel.run(self.update, self.draw)



    def update(self):
        global flag
        character.update()

        for enemy in enemy_list:
            if abs(character.x - enemy.x) < 6 and abs(character.y - enemy.y) < 6:
                if flag == 1:
                    flag = 0
                    pyxel.run(self.update, self.draw)
                else:

                    game_over()
                    return

            enemy.update()

            if enemy.x < scroll_x - 8 or enemy.x > scroll_x + 160 or enemy.y > 160:
                enemy.alive = False

        cleanup_list(enemy_list)

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(-(scroll_x % 8), 0, 0, scroll_x // 8, 0, 17, 16)
        if flag == 1:
            character.draw()
        else:
            character.draw_small()
        for enemy in enemy_list:
            enemy.draw()

def game_over():
    scroll_x = 0
    character.x = 0
    character.y = 0
    character.dx = 0
    character.dy = 0

    enemy_list = []
    spawn_enemy(0, 127)

App()
