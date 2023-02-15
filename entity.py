import pygame


def collision_test(rectangle: tuple[int, int, int, int] | pygame.Rect, tiles):
    hit_list = []

    for tile in tiles:
        if rectangle.colliderect(tile):
            hit_list.append(tile)

    return hit_list


def move(rect, pos, vel, tiles, dt):
    collision_types = {
        "right": False,
        "left": False,
        "top": False,
        "bottom": False
    }

    pos.x += vel.x
    rect.x = int(pos.x)
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if vel.x > 0:
            rect.right = tile.left
            pos.x = rect.x
            collision_types["right"] = True
        elif vel.x < 0:
            rect.left = tile.right
            pos.x = rect.x
            collision_types['left'] = True

    pos.y += vel.y
    rect.y = int(pos.y)
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if vel.y > 0:
            rect.bottom = tile.top
            pos.y = rect.y
            collision_types["bottom"] = True
        elif vel.y < 0:
            rect.top = tile.bottom
            pos.y = rect.y
            collision_types['top'] = True

    return rect, collision_types


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pygame.Vector2(100, 50)
        self.size = (6, 10)
        self.vel = pygame.Vector2(0, 0)
        self.force = 0
        self.jumped = False
        self.air_time = 0

        self.rect = pygame.Rect(self.pos, self.size)

        self.image = pygame.Surface(self.size)
        self.image.fill((255, 255, 255))

    def draw(self, surf: pygame.Surface):
        surf.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, dt, keys, tiles):

        self.vel = pygame.Vector2(0, 0)
        if keys[pygame.K_a]:
            self.vel.x -= 1.25
        if keys[pygame.K_d]:
            self.vel.x += 1.25

        if keys[pygame.K_SPACE]:
            if not self.jumped and self.air_time < 10:
                self.force = -2
                self.jumped = True

        self.vel.y += self.force
        if self.force < 0:
            self.force += 0.1
        else:
            self.force += 0.25
        if self.force > 7:
            self.force = 7

        self.rect, collision_types = move(self.rect, self.pos, self.vel,  tiles, dt)

        if collision_types['bottom']:
            self.force = 0
            self.jumped = False
            self.air_time = 0
        else:
            self.air_time += 1

        if collision_types['top']:
            self.force = 1
