import pygame
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y, shots):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shots = shots
        self.shot_cooldown = 0
        
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)
    
    def move(self, dt, direction = 1):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt * direction
        
    def rotate(self, dt, direction = 1):
        self.rotation += PLAYER_TURN_SPEED * dt * direction
        
    def update(self, dt):
        self.shot_cooldown -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt, 1)
            
        if keys[pygame.K_s]:
            self.move(dt, -1)

        if keys[pygame.K_a]:
            self.rotate(dt, -1)

        if keys[pygame.K_d]:
            self.rotate(dt, 1)
            
        if keys[pygame.K_SPACE]:
            self.shoot()   
        
    def shoot(self):
        pygame.mixer.init()
        shot_sound = pygame.mixer.Sound("./sounds/shot01.wav")
        shot_sound.set_volume(0.5)
        
        if self.shot_cooldown > 0:
            return
        
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shots.add(shot)
        shot_sound.play()
        