import pygame
import time
import random as rnd
import math
import sys
from pygame.locals import *

from effect import ShapeParticles, SparkParticles, ImgParticles


def main():
    pygame.init()

    # constants
    ZOOM = 1.0
    WS = [800, 608]
    DS = [WS[0] / ZOOM, WS[1] / ZOOM]

    # main pygame variables
    window = pygame.display.set_mode(WS)
    display = pygame.Surface(DS)
    clock = pygame.time.Clock()

    # logic primitives
    last_time = time.perf_counter()

    # entity groups

    # entities and objects

    done = False
    while not done:
        # calculate the delta time
        dt = time.perf_counter() - last_time
        dt *= 60
        last_time = time.perf_counter()

        # logic

        # drawing
        display.fill((0, 0, 0))  # begin

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
