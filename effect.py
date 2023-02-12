import pygame
import math


def surf_circle(r: float, color: tuple | pygame.Color) -> pygame.Surface:
    surf = pygame.Surface((r * 2, r * 2)) if r > 0 else pygame.Surface((0, 0))
    pygame.draw.circle(surf, color, (r, r), r)
    surf.set_colorkey((0, 0, 0))

    return surf


def surf_rect(w: float, h: float, color: tuple | pygame.Color) -> pygame.Surface:
    surf = pygame.Surface((w, h)) if w > 0 and h > 0 else pygame.Surface((0, 0))
    surf.fill(color)

    return surf


class ShapeParticles:
    def __init__(self, shape_type: str, gravity: float = 0.0):
        self.shape_type = shape_type
        self.gravity = gravity
        self.objects = []

    def add(self, loc: list | pygame.Vector2, angle: float, speed: float, size: float, color: tuple | pygame.Color, dis_amount: float):
        vel = [math.cos(math.radians(angle)) * speed, math.sin(math.radians(angle)) * speed]
        self.objects.append([loc, vel, size, color, dis_amount])

    def use(self, surf: pygame.Surface, dt: float, operation=lambda x, dt: x):
        if self.shape_type == "circle":
            for i, p in sorted(enumerate(self.objects), reverse=True):
                p[0][0] += p[1][0] * dt
                p[0][1] += p[1][1] * dt
                p[2] -= p[4] * dt
                p[1][1] += self.gravity * dt
                operation(p, dt)
                pygame.draw.circle(surf, p[3], p[0], p[2])
                if p[2] <= 0:
                    self.objects.pop(i)

        elif self.shape_type == "rectangle":
            for i, p in sorted(enumerate(self.objects), reverse=True):
                p[0][0] += p[1][0] * dt
                p[0][1] += p[1][1] * dt
                p[2] -= p[4] * dt
                p[1][1] += self.gravity * dt
                operation(p, dt)
                pygame.draw.rect(surf, p[3], (p[0][0], p[0][1], p[2], p[2]))
                if p[2] <= 0:
                    self.objects.pop(i)
        else:
            raise TypeError(f"{self.shape_type} is an invalid shape type")

    def use_with_light(self, surf: pygame.Surface, dt: float, operation=lambda x, dt: x):
        if self.shape_type == "circle":
            for i, p in sorted(enumerate(self.objects), reverse=True):
                p[0][0] += p[1][0] * dt
                p[0][1] += p[1][1] * dt
                p[2] -= p[4] * dt
                p[1][1] += self.gravity * dt
                operation(p, dt)
                light_surf = surf_circle(p[2] * 2, (p[3][0] / 3, p[3][1] / 3, p[3][2] / 3))
                surf.blit(light_surf,
                          (p[0][0] - int(light_surf.get_width() / 2), p[0][1] - int(light_surf.get_height() / 2)),
                          special_flags=pygame.BLEND_RGB_ADD)
                pygame.draw.circle(surf, p[3], p[0], p[2])
                if p[2] <= 0:
                    self.objects.pop(i)

        elif self.shape_type == "rectangle":
            for i, p in sorted(enumerate(self.objects), reverse=True):
                p[0][0] += p[1][0] * dt
                p[0][1] += p[1][1] * dt
                p[2] -= p[4] * dt
                p[1][1] += self.gravity * dt
                operation(p, dt)
                light_surf = surf_rect(p[2] * 2, p[2] * 2, (p[3][0] / 3, p[3][1] / 3, p[3][2] / 3))
                surf.blit(light_surf,
                          (p[0][0] - int(light_surf.get_width() / 4), p[0][1] - int(light_surf.get_height() / 4)),
                          special_flags=pygame.BLEND_RGB_ADD)
                pygame.draw.rect(surf, p[3], (p[0][0], p[0][1], p[2], p[2]))
                if p[2] <= 0:
                    self.objects.pop(i)
        else:
            raise TypeError(f"{self.shape_type} is an invalid shape type")


class SparkParticles:
    def __init__(self, gravity: float = 0.0):
        self.gravity = gravity
        self.objects = []

    def add(self, loc: list | pygame.Vector2, angle: float, speed: float, scale: float, color: tuple | pygame.Color, dis_amount: float):
        self.objects.append(Spark(loc, angle, speed, color, scale, dis_amount))

    def use(self, surf: pygame.Surface, dt: float, operation=lambda x, dt: x):
        for i, s in sorted(enumerate(self.objects), reverse=True):
            s.move(dt, self.gravity)
            operation(s, dt)
            s.draw(surf)
            if not s.alive:
                self.objects.pop(i)


class ImgParticles:
    def __init__(self, img: pygame.Surface, gravity: float = 0.0, color_key: tuple | pygame.Color = (0, 0, 0)):
        self.img = img
        self.img.set_colorkey(color_key)
        self.gravity = gravity
        self.objects = []

    def add(self, loc: list | pygame.Vector2, angle: float, speed: float, size: float, color: tuple | pygame.Color, dis_amount: float):
        vel = [math.cos(math.radians(angle)) * speed, math.sin(math.radians(angle)) * speed]
        self.objects.append([loc, vel, size, color, dis_amount])

    def use(self, surf: pygame.Surface, dt: float, operation=lambda x, dt: x):
        for i, p in sorted(enumerate(self.objects), reverse=True):
            p[0][0] += p[1][0] * dt
            p[0][1] += p[1][1] * dt
            p[2] -= p[4] * dt
            p[1][1] += self.gravity * dt
            operation(p, dt)
            surf.blit(pygame.transform.scale(self.img, (p[2], p[2])), (p[0][0]-p[2]/2, p[0][1]-p[2]/2))
            if p[2] <= 0:
                self.objects.pop(i)


class Spark:
    def __init__(self, loc: list | tuple | pygame.Vector2, angle: float, speed: float, color: tuple = (255, 255, 255), scale: float = 1,
                 dis_amount: float = 0.25):
        self.loc = loc
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.dis_amount = dis_amount
        self.alive = True

    def calculate_movement(self, dt: float):
        return [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]

    def velocity_adjust(self, friction, force, terminal_velocity, dt):
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])

    def move(self, dt: float, gravity: float = 0.0):
        movement = self.calculate_movement(dt)
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]
        self.velocity_adjust(0.975, gravity, 8, dt)

        self.speed -= self.dis_amount * dt

        if self.speed <= 0:
            self.alive = False

    def draw(self, surf):
        if self.alive:
            points = [
                [self.loc[0] + math.cos(self.angle) * self.speed * self.scale,
                 self.loc[1] + math.sin(self.angle) * self.speed * self.scale],
                [self.loc[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3,
                 self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                [self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5,
                 self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
                [self.loc[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3,
                 self.loc[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
            ]
            pygame.draw.polygon(surf, self.color, points)
