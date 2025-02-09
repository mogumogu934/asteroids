import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass
    
    def has_collided(self, other_circle):
        distance = pygame.math.Vector2.distance_to(self.position, other_circle.position)
        return distance <= self.radius + other_circle.radius

    def is_off_screen(self, SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT):
        return (self.position.x + self.radius < SCREEN_WIDTH * -1 or
                self.position.x - self.radius > SCREEN_WIDTH * 2 or
                self.position.y + self.radius < SCREEN_HEIGHT * -1 or
                self.position.y - self.radius > SCREEN_HEIGHT * 2 )