import pygame
from constants import SHOT_RADIUS
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, position):
        super().__init__(position.x, position.y, SHOT_RADIUS)
    
    def draw (self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, SHOT_RADIUS, width = 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
