import pygame
import random
from constants import ASTEROID_MIN_RADIUS
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    
    
    def draw (self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, width = 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
        
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        random_angle = random.uniform(20, 50)
        new_vector1 = self.velocity.rotate(random_angle)
        new_vector2 = self.velocity.rotate(-random_angle)
        self.radius -= ASTEROID_MIN_RADIUS
        new_asteroid1 = Asteroid(self.position.x, self.position.y, self.radius)
        new_asteroid2 = Asteroid(self.position.x, self.position.y, self.radius)
        new_asteroid1.velocity = new_vector1 * 1.2
        new_asteroid2.velocity = new_vector2 * 1.2
        