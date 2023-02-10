import pygame
import time
from pygame.locals import *

import entities

cpdef void main():
    pygame.init()

    # constants
    cdef float ZOOM = 1.0
    cdef list WS = [800, 608]
    cdef list DS = [WS[0]/ZOOM, WS[1]/ZOOM]

    # main pygame variables
    window = pygame.display.set_mode(WS)
    display = pygame.Surface(DS)
    clock = pygame.time.Clock()

    # logic primitives
    cdef float last_time = time.perf_counter()

    # entity Groups

    # entities and objects
    block = entities.Block(10,30,(0, 255, 0))


    cdef bint done = False
    while not done:

        # logic


        # drawing
        display.fill((0, 0, 0)) #  begin

        pygame.draw.rect(display, (255, 0, 0), (30,30, 50, 60))
        block.draw(display)

        pygame.display.update() #  end


        for  event in pygame.event.get():
            if event.type == QUIT:
                done = True

        surf = pygame.transform.scale(display, WS)
        window.blit(surf, (0, 0))
        clock.tick(999)

    pygame.quit()