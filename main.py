import pygame # type: ignore
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WRAP_AROUND
from circleshape import CircleShape
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot
from powerup import PowerUpField, PowerUp
from high_score import get_high_score, save_high_score

def main():
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 8192)
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = pygame.image.load("./images/bg.png").convert()
    print("Starting asteroids!")
    
    bgm = pygame.mixer.Sound("./sounds/Startide.wav")
    bgm.play(-1)
    asteroid_kill_sounds = [
        pygame.mixer.Sound("./sounds/asteroidkill01.wav"),
        pygame.mixer.Sound("./sounds/asteroidkill02.wav"),
        pygame.mixer.Sound("./sounds/asteroidkill03.wav"),
    ]
    death_sound = pygame.mixer.Sound("./sounds/death01.wav")
    next_life_sound = pygame.mixer.Sound("./sounds/jingle03.wav")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    Player.containers = (updatable, drawable,)
    Asteroid.containers = (asteroids, updatable, drawable,)
    AsteroidField.containers = (updatable,)
    Shot.containers = (updatable, drawable,)
    PowerUp.containers = (updatable, drawable, powerups,)
    PowerUpField.containers = (updatable,)
    
    # Spawn player and other entities
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    player = Player(center_x, center_y, shots)
    asteroid_field = AsteroidField()
    powerup_field = PowerUpField()
    
    font = pygame.font.SysFont(None, 36)
    score = 0
    next_life_threshold = 10000
    high_score = get_high_score()
    
    clock = pygame.time.Clock()
    dt = 0
    
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
            if not WRAP_AROUND:
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
                if not WRAP_AROUND:
                    if shot.is_off_screen():
                        shot.kill()
                        continue
                if shot.has_collided(asteroid):
                    shot.kill()
                    asteroid.split()
                    random.choice(asteroid_kill_sounds).play()
                    score += 100
                    if score >= next_life_threshold:
                        player.lives += 1
                        next_life_threshold += 10000
                        next_life_sound.play()
                         
        for powerup in powerups:
            if powerup.has_collided(player):
                player.active_powerup = powerup.effect
                player.powerup_timer = 0
                if powerup.effect == "SHIELD":
                    player.invincible = True
                elif powerup.effect == "DECREASED SHOT COOLDOWN":
                    player.shot_cooldown *= 0.05
                powerup.kill()
                    
        screen.blit(background, [0, 0])
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (16, 16))
        lives_text = font.render(f"Lives Remaining: {player.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (16, 48))
        
        for object in drawable:
            object.draw(screen)
            
        pygame.display.flip()


if __name__ == "__main__":
    main()
