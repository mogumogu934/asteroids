import pygame # type: ignore
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WRAP_AROUND, SHOT_RADIUS, SHOT_LIFETIME
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.lifetime = 0
    
    def draw (self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, SHOT_RADIUS, 2)
    
    def update(self, dt):
        self.lifetime += dt
        if self.lifetime > SHOT_LIFETIME:
            self.kill()
            
        self.position += self.velocity * dt
        if WRAP_AROUND:
            self.wrap_around(SCREEN_WIDTH, SCREEN_HEIGHT)
        