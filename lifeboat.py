import pygame
import random
from enemy import Enemy
import os
import time
from cannon_ball_enemy import CannonBallEnemy
from explosion import Explosion
from zombie import Zombie 

class Lifeboat(Enemy, pygame.sprite.Sprite):
    speed = 2
    width = 45
    height = 55

    def __init__(self, screen, vessels, speed, x, y):
        pygame.sprite.Sprite.__init__(self)
        lifeboat_image = pygame.image.load(os.path.join("images", "lifeboat.png")).convert_alpha()
        lifeboat_image = pygame.transform.scale(lifeboat_image, (45, 55))
        self.image = lifeboat_image
        self.rect = self.image.get_rect()
        self.screen = screen
        self.speed = speed
        self.vessels = vessels
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)                                                                    # Create a mask from the image to use for collision detection
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.hit_points = 200
        self.value = 100

    def move(self):
        self.rect.y += self.speed
        if self.rect.bottom >= 480:
            self.speed = 0
            self.spawn_zombie()

    def attack(self):
        if self.rect.y >=0:                                                                                                 # Check if the lifeboat is on the screen
            now = pygame.time.get_ticks()                                                                                   # Get the current time
            if now - self.last_shot > self.shoot_delay:                                                                     # Check if enough time has passed since the last shot
                self.shoot_delay = random.randint(500, 2000)                                                                # Generate a random delay between 500 and 2000 milliseconds
                bullet = CannonBallEnemy(self.rect.centerx, self.rect.bottom)                                               # Create a new bullet instance
                bullet.rect.centerx = self.rect.centerx                                                                     # Center the bullet horizontally
                bullet.rect.bottom = self.rect.bottom + 10                                                                  # Position the bullet at the bottom of the lifeboat
                self.vessels.add(bullet)                                                                                    # Add the bullet to the vessels group
                self.last_shot = now                                                                                        # Update the time of the last shot

    def update_hit_points(self, damage):                                                                                    # Method to update the hit points of the lifeboat        
        self.hit_points -= damage
        if self.hit_points <= 0:                                                                                            # Check if the hit points are less than or equal to zero        
            self.destroy()
            
    def destroy(self):                                                                                                      # Method to destroy the lifeboat      
        explosion = Explosion(self.rect.centerx, self.rect.centery)
        self.vessels.add(explosion)                                                                                         # Add explosion to vessels group
        self.hit_points = 0                                                                                                 # Set hit points to zero to prevent further damage
        self.kill()

    def spawn_zombie(self):
        # Spawn a Zombie at the position of the Lifeboat
        zombie = Zombie(self.rect.centerx, self.rect.bottom, self.vessels)
        self.vessels.add(zombie)