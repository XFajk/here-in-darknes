import pygame
import time
import random as rnd
import math
import sys
from csv import reader
from os import path
from pygame.locals import *

from effect import surf_circle


def read_csv_file(filepath: str):
    level = []
    with open(path.join(filepath)) as data:
        data = reader(data, delimiter=',')
        for row in data:
            level.append(list(row))

    return level


def combine_list2d(list1: list, list2: list):
    lis = []
    for i, row in enumerate(list1):
        lis.append([])
        for j, element in enumerate(row):
            lis[i].append([list1[i][j], list2[i][j]])

    return lis


def get_tile(sprite_sheet: pygame.Surface, tile_w: int, tile_h: int, tile_x: int, tile_y: int):
    tile = pygame.transform.chop(sprite_sheet, (
        int(tile_x + 1) * tile_w,
        int(tile_y + 1) * tile_h,
        sprite_sheet.get_width() - tile_w,
        sprite_sheet.get_height() - tile_h
    ))

    tile = pygame.transform.chop(tile, (
        -1,
        -1,
        1+tile_w + (tile.get_width()-(tile.get_width()-(tile_x-1)*8)),
        1+tile_h + (tile.get_height()-(tile.get_height()-(tile_y-1)*8))
    ))

    return tile


def main():
    pygame.init()

    # constants
    ZOOM = 4.0
    WS = [800, 608]
    DS = [WS[0] / ZOOM, WS[1] / ZOOM]

    # main pygame variables
    window = pygame.display.set_mode(WS)
    display = pygame.Surface(DS)
    clock = pygame.time.Clock()

    # logic primitives
    last_time = time.perf_counter()
    light_index = [15, 0.1]

    # sprites
    fist_world_sheet = pygame.image.load("assets/sprite_sheets/first_world.png").convert()
    fist_world_sheet.set_colorkey((255, 255, 255))
    tiles = []
    for y in range(5):
        for x in range(8):
            tiles.append(get_tile(fist_world_sheet, 8, 8, x, y))

    # entity groups

    # entities and objects
    pl = pygame.image.load("assets/sprites/player/idle/player_sprite.png").convert()
    pl.set_colorkey((255, 255, 255))
    level = combine_list2d(read_csv_file("assets/map_csvs/first_world_cave_0.csv"),
                           read_csv_file("assets/map_csvs/first_world_cave_1.csv"))

    done = False
    while not done:
        # calculate the delta time
        dt = time.perf_counter() - last_time
        dt *= 60
        last_time = time.perf_counter()

        # logic
        light_index[0] += light_index[1]*dt
        if int(light_index[0]) <= 15:
            light_index[1] = 0.1
        elif int(light_index[0]) >= 20:
            light_index[1] = -0.1

        # drawing
        display.fill((0, 0, 0))  # begin

        # drawing the level
        rects = []
        slopes = []
        lights = []
        ends = []
        for y, row in enumerate(level):
            for x, tile in enumerate(row):
                display.blit(tiles[int(tile[0])], (x*8, y*8))
                match tile[1]:
                    case '0':
                        ...
                    case _:
                        ...
                match tile[0]:
                    case '0':
                        rects.append(pygame.Rect(x*8, y*8, 8, 8))
                    case '1':
                        rects.append(pygame.Rect(x*8, y*8, 8, 8))
                    case '2':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '3':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '4':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '5':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '6':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '7':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '8':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '9':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '10':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '11':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '14':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '15':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '16':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '17':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '18':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '19':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '22':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '23':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '24':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '25':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '26':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '27':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '28':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '29':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '31':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case '32':
                        lights.append([[x*8+4, y*8+4], (25, 15, 1), 25, light_index[0]])
                    case '39':
                        rects.append(pygame.Rect(x * 8, y * 8, 8, 8))
                    case _:
                        ...

        display.blit(pl, (60, 125))

        for light in lights:
            light_surf = surf_circle(light[2], light[1])
            light_surf2 = surf_circle(light[3], light[1])

            display.blit(light_surf, (
                light[0][0] - int(light_surf.get_width()/2),
                light[0][1] - int(light_surf.get_height()/2)
            ), special_flags=BLEND_RGB_ADD)
            display.blit(light_surf2, (
                light[0][0] - int(light_surf2.get_width() / 2),
                light[0][1] - int(light_surf2.get_height() / 2)
            ), special_flags=BLEND_RGB_ADD)

        pygame.display.update()  # end

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

        surf = pygame.transform.scale(display, WS)
        window.blit(surf, (0, 0))

        pygame.display.set_caption(f"here in darkness FPS:{round(clock.get_fps(), 1)}")
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
    sys.exit()
