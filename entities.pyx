import pygame

cdef class Block:
    cdef tuple rect
    cdef tuple color

    def __init__(self, float w, float h, tuple color):
        self.rect = (30, 80, w, h)
        self.color = color


    cpdef void draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
