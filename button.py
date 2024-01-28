import pygame


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