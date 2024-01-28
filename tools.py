import pygame

"""==================Класс кнопки=================="""


class Button:
    def __init__(self, x, y, w, h, text, img, hover_img, sound):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.hover_image = pygame.image.load(hover_img)
        self.hover_image = pygame.transform.scale(self.hover_image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = pygame.mixer.Sound(sound)
        self.is_hovered = False

    def draw(self, screen):
        cur_img = self.hover_image if self.is_hovered else self.image
        screen.blit(cur_img, self.rect.topleft)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


"""==================Класс героя=================="""


class Hero(pygame.sprite.Sprite):
    def __init__(self, hp, x, y, w, h, vel, scr, r_animation, l_animation, atk, l_atk, w_atk, l_w_atk, r_default, l_default, max_x, min_x, max_y, min_y):
        super().__init__()
        self.velocity = vel
        self.attacking = False
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = min_x
        self.min_y = min_y
        self.hp = hp

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
        if keys[pygame.K_a] and self.rect.x >= self.min_x:
            self.rect.x -= self.velocity
            self.left = True
            self.right = False
            self.safe_l = True
            self.safe_r = False
        if keys[pygame.K_d] and self.rect.x <= self.max_x:
            self.rect.x += self.velocity
            self.left = False
            self.right = True
            self.safe_l = False
            self.safe_r = True
        if keys[pygame.K_s] and self.rect.y <= self.max_y:
            self.rect.y += self.velocity
            self.left = self.safe_l
            self.right = self.safe_r
        if keys[pygame.K_w] and self.rect.y >= self.min_y:
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
            if self.attack_step + 1 >= 18:
                self.attack_step = 0
                self.attacking = False
            if self.left is True:
                self.screen.blit(self.l_w_atk[self.attack_step // 3], (self.rect.x, self.rect.y))
                self.attack_step += 1
            elif self.right is True:
                self.screen.blit(self.w_atk[self.attack_step // 3], (self.rect.x, self.rect.y))
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