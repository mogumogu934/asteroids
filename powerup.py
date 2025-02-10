import pygame # type: ignore
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, POWERUP_SPAWN_RATE, POWERUP_LIFETIME
from circleshape import CircleShape


class PowerUp(CircleShape):
    def __init__(self, x, y):
        original_color = getattr(self, 'color', (255, 255, 255))
        original_effect = getattr(self, 'effect', None)
        super().__init__(x, y, 16)
        self.color = original_color
        self.effect = original_effect
        self.lifetime = 0
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
        
    def update(self, dt):
        self.lifetime += dt
        if self.lifetime > POWERUP_LIFETIME:
            self.kill()
            
class Shield(PowerUp):
    def __init__(self, x, y):
        self.color = (92, 145, 238)
        self.effect = "SHIELD"
        super().__init__(x, y)
        
class DecreasedShotCooldown(PowerUp):
    def __init__(self, x, y):
        self.color = (196, 44, 44)
        self.effect = "DECREASED SHOT COOLDOWN"
        super().__init__(x, y)

class PowerUpField(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0
        self.powerup_types = [Shield, DecreasedShotCooldown]
    
    def update(self,dt):
        self.spawn_timer += dt
        if self.spawn_timer > POWERUP_SPAWN_RATE:
            self.spawn_timer = 0
            powerup_type = random.choice(self.powerup_types)
            position_x = random.randrange(SCREEN_WIDTH - 32)
            position_y = random.randrange(SCREEN_HEIGHT - 32)
            powerup_type(position_x, position_y)
            