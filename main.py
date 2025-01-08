import pygame
import sys
from pygame.locals import *
import random
import time
from gameConfig import * 
from gameClasses import Bullet, Enemy, Player

TYPE_SMALL:int = 1
TYPE_MIDDLE:int = 2
TYPE_BIG:int = 3

shoot_frequency: int = 0
enemy_frequency: int = 0
player_down_index: int = 16

score: int = 0
end: bool = False 
win: bool = False 

score: int = 0


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Plane shooter remake')

bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)


background = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')
win_screen = pygame.image.load('resources/image/winscreen.png') 

plane_img = pygame.image.load('resources/image/shoot.png')


p_rect = []
p_rect.append(pygame.Rect(0, 99, 102, 126))
p_rect.append(pygame.Rect(165, 360, 102, 126))
p_rect.append(pygame.Rect(165, 234, 102, 126)) 
p_rect.append(pygame.Rect(330, 624, 102, 126))
p_rect.append(pygame.Rect(330, 498, 102, 126))
p_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
player = Player(plane_img, p_rect, player_pos)


bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)


enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies1 = pygame.sprite.Group()
enemies_down = pygame.sprite.Group()
clock=pygame.time.Clock()


while True:
    clock.tick(60)
    if score in WIN_SCORE: 
        WIN_SCORE.remove(score)
        enemy_speed *= enemy_speed_mp
        for enemy in enemies1:
            enemy.speed *= enemy_speed_mp

    if not player.is_hit:
        if shoot_frequency % 15 == 0:
            bullet_sound.play()
            player.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0

    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos, enemy_speed)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0
    
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    for enemy in enemies1:
        enemy.move()
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies1.remove(enemy)

    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)
   
    screen.fill(0)
    screen.blit(background, (0, 0))

    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
       
        player.img_index = shoot_frequency // 8
    else:
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47: #
            end = True
            win = False

    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += ADDED_SCORE
            if score >= WIN_SCORE[-1]: 
                end = True
                win = True
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    player.bullets.draw(screen)
    enemies1.draw(screen)
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_ESCAPE]: # Toegevoegd
         pygame.quit()

    if not player.is_hit:
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()
     
    if end and not win:
        font = pygame.font.Font(None, 48)
        text = font.render(str(score), True, (50, 0, 0))  # Veranderd
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery - 24
        screen.blit(game_over, (0, 0))
        screen.blit(text, text_rect)
        pygame.display.update()
        time.sleep(2)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        pygame.quit()
                        sys.exit()

    if end and win:
        font = pygame.font.Font(None, 48)
        text = font.render(str("Score: "+str(score)), True, (50, 0, 0))  # Veranderd
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery + 24
        screen.blit(win_screen, (0, 0))
        screen.blit(text, text_rect)
        pygame.display.update()
        time.sleep(2)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  
                        pygame.quit()
                        sys.exit()

    pygame.display.update()
