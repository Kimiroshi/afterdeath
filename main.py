import sys
import pygame
from tools import Button
from tools import Hero

pygame.init()
FPS = 60
SIZE = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)


def main_menu():
    running = True
    bg = pygame.image.load('data/bg.jpg')
    mouse = pygame.image.load('data/mouse.png')
    hover = pygame.image.load('data/mouse2.png')
    start_button = Button(1200, 700, 250, 53, 'Начать игру', 'data/button.png', 'data/hover_button.png',
                          'data/button_sound3.wav')
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
                first_scene()
            start_button.handle_event(event)
        start_button.check_hover(pygame.mouse.get_pos())
        start_button.draw(screen)
        if start_button.is_hovered:
            screen.blit(hover, pygame.mouse.get_pos())
        else:
            screen.blit(mouse, pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


def first_scene():
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

    screen.fill((0, 0, 0))
    running = True
    bg = pygame.image.load('data/lvl1.png')
    bg = pygame.transform.scale(bg, (1920, 1080))
    running = True
    hero = Hero(20,10, 500, 250, 250, 10, screen, r_anim, l_anim, atk, l_atk, w_atk, l_w_atk, 'data/knight.png',
                'data/l_knight.png', 1400, -120, 640, 500)
    _ = 0

    while running:
        screen.blit(bg, (-160, -100))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and _ != 0:
                    hero.attacking = True
        hero.change()
        hero.move()
        pygame.display.flip()
        clock.tick(60)
        _ += 1


if __name__ == "__main__":
    main_menu()