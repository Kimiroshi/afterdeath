import sys

import pygame

r_anim = [pygame.image.load('data/walk1.png'), pygame.image.load('data/walk2.png'),
        pygame.image.load('data/walk3.png'),
        pygame.image.load('data/walk4.png'), pygame.image.load('data/walk5.png'),
        pygame.image.load('data/walk6.png'), ]

l_anim = [pygame.image.load('data/l_walk1.png'), pygame.image.load('data/l_walk2.png'),
        pygame.image.load('data/l_walk3.png'),
        pygame.image.load('data/l_walk4.png'), pygame.image.load('data/l_walk5.png'),
        pygame.image.load('data/l_walk6.png'), ]

atk = [pygame.image.load('data/attack0.png'), pygame.image.load('data/attack1.png'),
        pygame.image.load('data/attack2.png'),
        pygame.image.load('data/attack3.png')]

w_atk = [pygame.image.load('data/walk_attack1.png'), pygame.image.load('data/walk_attack2.png'),
        pygame.image.load('data/walk_attack3.png'),
        pygame.image.load('data/walk_attack4.png'), pygame.image.load('data/walk_attack5.png'),
        pygame.image.load('data/walk_attack6.png')]

l_atk = [pygame.image.load('data/l_attack0.png'), pygame.image.load('data/l_attack1.png'),
        pygame.image.load('data/l_attack2.png'),
        pygame.image.load('data/l_attack3.png')]

l_w_atk = [pygame.image.load('data/l_walk_attack1.png'), pygame.image.load('data/l_walk_attack2.png'),
        pygame.image.load('data/l_walk_attack3.png'),
        pygame.image.load('data/l_walk_attack4.png'), pygame.image.load('data/l_walk_attack5.png'),
        pygame.image.load('data/l_walk_attack6.png')]

for i in (r_anim, l_anim, atk, l_atk, w_atk, l_w_atk):
    for j in range(len(i)):
        i[j] = i[j] = pygame.transform.scale(i[j], (250, 250))


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, vel, scr, r_animation, l_animation, atk, l_atk, w_atk, l_w_atk, r_default, l_default):
        super().__init__()
        self.velocity = vel
        self.attacking = False

        self.r_animation = r_animation
        self.l_animation = l_animation
        self.l_default = l_default
        self.r_default = r_default
        self.atk = atk
        self.l_atk = l_atk
        self.w_atk = w_atk
        self.l_w_atk = l_w_atk

        self.img = pygame.image.load(r_default)
        self.img = pygame.transform.scale(self.img, (w, h))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        self.screen = scr

        self.step = 0
        self.attack_step = 0

        self.left = False
        self.right = False
        self.safe_l = False
        self.safe_r = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.velocity
            self.left = True
            self.right = False
            self.safe_l = True
            self.safe_r = False
        if keys[pygame.K_d]:
            self.rect.x += self.velocity
            self.left = False
            self.right = True
            self.safe_l = False
            self.safe_r = True
        if keys[pygame.K_s]:
            self.rect.y += self.velocity
            self.left = self.safe_l
            self.right = self.safe_r
        if keys[pygame.K_w]:
            self.rect.y -= self.velocity
            self.left = self.safe_l
            self.right = self.safe_r
        if not any((keys[pygame.K_a], keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_d])):
            self.step = 0
            self.left = False
            self.right = False
            if self.attacking:
                self.attack()

    def change(self):
        if self.attacking:
            if self.attack_step + 1 >= 30:
                self.attack_step = 0
                self.attacking = False
            if self.left is True:
                self.screen.blit(self.l_w_atk[self.attack_step // 5], (self.rect.x, self.rect.y))
                self.attack_step += 1
            elif self.right is True:
                self.screen.blit(self.w_atk[self.attack_step // 5], (self.rect.x, self.rect.y))
                self.attack_step += 1
        else:
            if self.step + 1 >= 30:
                self.step = 0
            if self.left is True:
                self.screen.blit(self.l_animation[self.step // 5], (self.rect.x, self.rect.y))
                self.step += 1
            elif self.right is True:
                self.screen.blit(self.r_animation[self.step // 5], (self.rect.x, self.rect.y))
                self.step += 1
            else:
                self.img = pygame.image.load(self.r_default if self.safe_r else self.l_default)
                self.img = pygame.transform.scale(self.img, (self.w, self.h))
                self.screen.blit(self.img, (self.rect.x, self.rect.y))

    def attack(self):
        if self.attack_step + 1 >= 20:
            self.attack_step = 0
            self.attacking = False
        if self.safe_l is True:
            self.screen.blit(self.l_atk[self.attack_step // 5], (self.rect.x, self.rect.y))
            self.attack_step += 1
        elif self.safe_r is True:
            self.screen.blit(self.atk[self.attack_step // 5], (self.rect.x, self.rect.y))
            self.attack_step += 1
        else:
            self.img = pygame.image.load(self.r_default if self.safe_r else self.l_default)
            self.img = pygame.transform.scale(self.img, (self.w, self.h))
            self.screen.blit(self.img, (self.rect.x, self.rect.y))


size = width, height = 1920, 1080
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen.fill((0, 0, 0))
clock = pygame.time.Clock()

running = True
hero = Hero(10, 10, 250, 250, 5, screen, r_anim, l_anim, atk, l_atk, w_atk, l_w_atk, 'data/knight.png', 'data/l_knight.png')
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                hero.attacking = True
    hero.change()
    hero.move()
    pygame.display.flip()
    clock.tick(60)
