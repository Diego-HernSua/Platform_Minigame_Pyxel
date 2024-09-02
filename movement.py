
import pyxel
import math

CHARA_WIDTH = 8
CHARA_HEIGHT = 8

TILE_SPACE = (0, 0)
TILE_BLOCK = (1, 0)
TILE_FLOOR = (2, 0)
TILE_SPAWN = (0, 1)
TILE_ENEMY = (0, 1)
TILE_Tortoise = (1, 1)
TILE_Flower = (2, 1)


character = None


def get_tilemap(x, y):
    return pyxel.tilemap(0).pget(x, y)


def check_tilemap_collision(x, y, dx, dy):
        x1 = x // 8
        y1 = y // 8
        x2 = (x + CHARA_WIDTH - 1) // 8
        y2 = (y + CHARA_HEIGHT - 1) // 8

        for i in range(y1, y2 + 1):
            for j in range(x1, x2 + 1):
                if get_tilemap(j, i) == TILE_BLOCK:
                    return True

        if dy > 0 and y % 8 == 1:
            for i in range(x1, x2 + 1):
                if get_tilemap(i, y1 + 1) == TILE_FLOOR:
                    return True

        return False




def react_on_collision(x, y, dx, dy):
    abs_dx = abs(dx)
    abs_dy = abs(dy)

    if abs_dx > abs_dy:
        sign = 1 if dx > 0 else -1
        for i in range(abs_dx):
            if check_tilemap_collision(x + sign, y, dx, dy):
                break
            x += sign

        sign = 1 if dy > 0 else -1
        for i in range(abs_dy):
            if check_tilemap_collision(x, y + sign, dx, dy):
                break
            y += sign
    else:
        sign = 1 if dy > 0 else -1
        for i in range(abs_dy):
            if check_tilemap_collision(x, y + sign, dx, dy):
                break
            y += sign

        sign = 1 if dx > 0 else -1
        for i in range(abs_dx):
            if check_tilemap_collision(x + sign, y, dx, dy):
                break
            x += sign

    return x, y, dx, dy


def check_floor(x, y):
    tile = get_tilemap(x // 8, y // 8)
    return tile == TILE_BLOCK or tile == TILE_FLOOR





def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
        else:
            i += 1


