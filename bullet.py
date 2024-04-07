import pygame
from pygame.sprite import Sprite
from explosion import Explosion
from lifeboat import Lifeboat
from sloop import Sloop
from ship import Ship
from cannon_ball_enemy import CannonBallEnemy

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vessels):
        pygame.sprite.Sprite.__init__(self)
        cannon_ball = pygame.image.load("images/cannon_ball.png")
        self.image = cannon_ball
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.vessels = vessels
        self.mask = pygame.mask.from_surface(self.image)
        self.damage = 100
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0 or self.rect.top > 1000:
            self.kill()

        collisions = pygame.sprite.spritecollide(self, self.vessels, False, pygame.sprite.collide_mask)                 # Check for collisions between the bullet and the vessels
        for collision in collisions:
            if isinstance(collision, CannonBallEnemy):
                collision.kill()                                                                                        # Destroy the enemy cannon ball
                self.kill()                                                                                             # Destroy the bullet as well

        collisions = pygame.sprite.spritecollide(self, self.vessels, False, pygame.sprite.collide_mask)                 # Check for collisions between the bullet and the vessels        
        if collisions:
            for collision in collisions:
                if isinstance(collision, (Lifeboat, Sloop, Ship)):                                                      # Check if the collision is with a lifeboat, sloop, or ship         
                    collision.update_hit_points(self.damage)
                    if collision.hit_points <= 0:
                        explosion = Explosion(collision.rect.centerx, collision.rect.centery)                               # Create an explosion at the center of the vessel       
                        self.vessels.add(explosion)
                        collision.kill()
                    self.kill()

    def set_damage(self, damage):
        self.damage = damage
