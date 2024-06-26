from enemy import Enemy
import pygame
import random
from coin import Coin
from cannon_ball_enemy import CannonBallEnemy
from explosion import Explosion 

class Ship(Enemy, pygame.sprite.Sprite):
    speed = 2
    width = 110
    height = 150
    value = 500

    def __init__(self, screen, vessels,cannon_ball_enemy, explosions, speed, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((110, 150))
        ship_image = pygame.image.load("images/ship.png").convert_alpha()
        self.image = ship_image
        self.rect = self.image.get_rect()
        self.screen = screen
        self.speed = speed
        self.vessels = vessels
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)                                                                                    # Create a mask from the image to use for collision detection
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.hit_points = 600
        self.explosions = explosions
        self.cannon_ball_enemy = cannon_ball_enemy
        self.check_zombie_spawn = False
        self.cannon_sound = pygame.mixer.Sound("sounds/enemy_cannon.mp3")
        self.cannon_sound.set_volume(0.1)

    # Method to move the ship
    def move(self):
        self.rect.y += self.speed
        if self.rect.bottom >= 480:
            self.speed = 0
            self.check_zombie_spawn = True

    # Method to attack the player
    def attack(self, y_offsets=[-20, 15, -20]):
        if self.rect.y >= 0:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.shoot_delay = random.randint(500, 2000)
                for i, offset in enumerate([-25, 0, 25]):
                    bullet = CannonBallEnemy(self.rect.centerx + offset, self.rect.bottom)
                    bullet.rect.centerx = self.rect.centerx + offset
                    bullet.rect.bottom = self.rect.bottom + y_offsets[i]
                    self.cannon_ball_enemy.add(bullet)
                self.last_shot = now
                self.cannon_sound.play()

    # Method to update the hit points of the ship
    def update_hit_points(self, damage):                                                                                   
        self.hit_points -= damage
        if self.hit_points <= 0:                                                                                            # Check if the hit points are less than or equal to zero
            self.destroy()

    # Method to destroy the ship
    def destroy(self):                                                                                                      
        explosion = Explosion(self.rect.centerx, self.rect.centery, "ship")
        bonus_luck = random.randint(1, 4)
        if bonus_luck == 1:
            bonus = Coin(self.rect.centerx, self.rect.centery)                                                                 # Create a coin at the center of the lifeboat
            self.vessels.add(bonus) 
        self.explosions.add(explosion)                                                                                         # Add explosion to vessels group
        self.hit_points = 0                                                                                                 # Set hit points to zero to prevent further damage
        self.kill()

    # Method to get the spawn of the zombies on the ship
    def get_spawn_value(self):
        return self.check_zombie_spawn