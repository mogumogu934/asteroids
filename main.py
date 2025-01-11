import pygame
from constants import *
from circleshape import CircleShape
from player import Player
from asteroidfield import *
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    clock = pygame.time.Clock()
    dt = 0
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (updatable, drawable)
    
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y, shots)
    asteroid_field = AsteroidField()
    
    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        dt = clock.tick(60) / 1000
        
        for object in updatable:
            object.update(dt)
            
        for asteroid in asteroids:
            if player.has_collided(asteroid):
                print("Game over!")
                exit()
            
        pygame.Surface.fill(screen, (0, 0, 0))
        
        for object in drawable:
            object.draw(screen)
            
        pygame.display.flip()


if __name__ == "__main__":
    main()
