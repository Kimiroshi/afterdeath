import os
import sys
import pygame
from button import Button

FPS = 60
SIZE = WIDTH, HEIGHT = 1920, 1080
bg = pygame.image.load('data/bg.jpg')
mouse = pygame.image.load('data/mouse.png')
hover = pygame.image.load('data/mouse2.png')

pygame.init()
screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
start_button = Button(1200, 700, 250, 53, 'Начать игру', 'data/button.png', 'data/hover_button.png',
                      'data/button_sound3.wav')

running = True
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.display.flip()
center = (-200, -200)
screen.blit(bg, center)

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEMOTION:
            delta = (center[0] - event.pos[0]) // 3, (center[1] - event.pos[1]) // 3
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 400, 400), 0)
            screen.blit(bg, delta)
        if event.type == pygame.USEREVENT and event.button == start_button:
            pass
        start_button.handle_event(event)
    start_button.check_hover(pygame.mouse.get_pos())
    start_button.draw(screen)
    if start_button.is_hovered:
        screen.blit(hover, pygame.mouse.get_pos())
    else:
        screen.blit(mouse, pygame.mouse.get_pos())
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()