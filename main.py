import pygame # type: ignore
import random
from constants import *
from circleshape import CircleShape
from player import Player
from asteroidfield import *
from shot import Shot
from high_score import get_high_score, save_high_score

def main():
    pygame.init()
    pygame.mixer.init()
    
    start_sound = pygame.mixer.Sound("./sounds/jingle01.wav")
    start_sound.set_volume(0.5)
    asteroid_kill_sounds = [
        pygame.mixer.Sound("./sounds/asteroidkill01.wav"),
        pygame.mixer.Sound("./sounds/asteroidkill02.wav"),
        pygame.mixer.Sound("./sounds/asteroidkill03.wav"),
    ]
    asteroid_kill_sounds[0].set_volume(0.25)
    asteroid_kill_sounds[1].set_volume(0.25)
    asteroid_kill_sounds[2].set_volume(0.25)
    death_sound = pygame.mixer.Sound("./sounds/death01.wav")
    death_sound.set_volume(0.5)
    
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting asteroids!")

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
    
    start_sound.play()
    font = pygame.font.SysFont(None, 36)
    score = 0
    high_score = get_high_score()
    
    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                player.invincible = False
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            if event.type == pygame.QUIT:
                return
            
        dt = clock.tick(120) / 1000
        
        for object in updatable:
            object.update(dt)
        
        for asteroid in asteroids:
            if asteroid.is_off_screen():
                asteroid.kill()
                continue
            if player.has_collided(asteroid) and not player.invincible:
                death_sound.play()
                if player.lives > 0:
                    player.lives -= 1
                    player.respawn()
                else:
                    print("Game over!")
                    if score > high_score:
                        save_high_score(score)
                        print(f"New high score of {score} pts!")
                    else:
                        print(f"Score: {score}")
                    exit()
                
        for asteroid in asteroids:
            for shot in shots:
                if shot.is_off_screen():
                    shot.kill()
                    continue
                if shot.has_collided(asteroid):
                    shot.kill()
                    asteroid.split()
                    random.choice(asteroid_kill_sounds).play()
                    score += 100
                    
        pygame.Surface.fill(screen, (0, 0, 0))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (16, 16))
        lives_text = font.render(f"Lives Remaining: {player.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (16, 48))
        
        for object in drawable:
            object.draw(screen)
            
        pygame.display.flip()


if __name__ == "__main__":
    main()
