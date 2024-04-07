from enemy import Enemy
import pygame
import random
import os
import time
from cannon_ball_enemy import CannonBallEnemy
from explosion import Explosion 


class Sloop(Enemy, pygame.sprite.Sprite):
    speed = 1
    width = 45
    height = 65

    def __init__(self, screen, vessels, speed, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((45, 65))
        sloop_image = pygame.image.load(os.path.join("images", "sloop.png")).convert_alpha()
        self.image = sloop_image
        self.rect = self.image.get_rect()
        self.screen = screen
        self.speed = speed
        self.vessels = vessels
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)                                                                                    # Create a mask from the image to use for collision detection
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.hit_points = 400


    def move(self):
        self.rect.y += self.speed

    def attack(self):
        if self.rect.y >= 0:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.shoot_delay = random.randint(500, 2000)
                for offset in [-10, 10]:  # Offsets for the three cannons
                    bullet = CannonBallEnemy(self.rect.centerx + offset, self.rect.bottom)
                    bullet.rect.centerx = self.rect.centerx + offset
                    bullet.rect.bottom = self.rect.bottom + 15
                    self.vessels.add(bullet)
                self.last_shot = now

    def update_hit_points(self, damage):                                                                                    # Method to update the hit points of the sloop
        self.hit_points -= damage
        if self.hit_points <= 0:                                                                                            # Check if the hit points are less than or equal to zero
            self.destroy()

    def destroy(self):                                                                                                      # Method to destroy the sloop
        explosion = Explosion(self.rect.centerx, self.rect.centery)
        self.vessels.add(explosion)                                                                                         # Add explosion to vessels group
        self.hit_points = 0                                                                                                 # Set hit points to zero to prevent further damage
        self.kill()