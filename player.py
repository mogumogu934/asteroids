import pygame # type: ignore
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_MAX_SPEED, PLAYER_ACCELERATION, PLAYER_FRICTION, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y, shots):
        super().__init__(x, y, PLAYER_RADIUS)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.shots = shots
        self.shot_cooldown = 0
        self.shot_sound = pygame.mixer.Sound("./sounds/shot01.wav")
        self.shot_sound.set_volume(0.5)
        self.lives = 1
        self.invincible = False
        
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time % 200 < 100: # Player will flicker every 100 ms
                return
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)
    
    def move(self, dt, forward=True):
        forward_vector = pygame.Vector2(0, 1).rotate(self.rotation)
        if forward:
            self.velocity += forward_vector * PLAYER_ACCELERATION * dt
        else:
            self.velocity -= forward_vector * PLAYER_ACCELERATION * dt
        
    def rotate(self, dt, direction):
        self.rotation += PLAYER_TURN_SPEED * dt * direction
        
    def update(self, dt):
        self.shot_cooldown -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt,forward=True)
            
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(dt, forward=False)

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(dt, -1)

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt, 1)
            
        if keys[pygame.K_SPACE]:
            self.shoot()
            
        self.position += self.velocity * dt
        self.velocity *= PLAYER_FRICTION
        if self.velocity.length() < 0.1:
            self.velocity = pygame.Vector2(0,0)
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity = self.velocity.normalize() * PLAYER_MAX_SPEED
        
    def shoot(self):
        if self.shot_cooldown > 0:
            return
        
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shots.add(shot)
        self.shot_sound.play()
        
    def respawn(self):
        self.position = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.invincible = True
        self.velocity = pygame.Vector2(0, 0)
        pygame.time.set_timer(pygame.USEREVENT + 1, 3000)
        