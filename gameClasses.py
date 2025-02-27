import pygame
from gameConfig import SCREEN_HEIGHT, SCREEN_WIDTH, enemy_speed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed: int = 10

    def move(self):
        self.rect.top -= self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, p_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 
        for i in range(len(p_rect)):
            self.image.append(plane_img.subsurface(p_rect[i]).convert_alpha())
        self.rect = p_rect[0]                      
        self.rect.topleft = init_pos                    
        self.speed: int = 8                                  
        self.bullets = pygame.sprite.Group()            
        self.img_index: int = 0                              
        self.is_hit = False                             

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos, enemySpeed):
       pygame.sprite.Sprite.__init__(self)
       self.image = enemy_img
       self.rect = self.image.get_rect()
       self.rect.topleft = init_pos
       self.down_imgs = enemy_down_imgs
       self.speed: int = enemySpeed or enemy_speed
       self.down_index: int = 0

    def move(self):
        self.rect.top += self.speed
