import sys
import pygame
from pygame.locals import *
import random
from Facade import Facade



def main_menu():
    screen = pygame.display.set_mode((360, 640))
    pygame.display.set_caption('ARCANOID')
    pygame.display.set_icon(pygame.image.load('icon.png'))
    font1 = pygame.font.Font('big-shot.ttf', 24)
    text0 = pygame.image.load('NAME.svg')
    text2 = font1.render("PLAY", True, (0xF5, 0xF5, 0xF5))
    text3 = font1.render("RECORDS", True, (0xF5, 0xF5, 0xF5))

    start_button = pygame.Rect(121, 361, 118, 43)
    records_button = pygame.Rect(121, 410, 118, 43)

    # Input box
    input_box = pygame.Rect(300, 200, 140, 32)
    color_inactive = pygame.Color(0xF5, 0xF5, 0xF5)
    color_active = pygame.Color(0xFF, 0x5E, 0xBE)
    color = color_inactive
    active = False
    text = ''
    input_rect = pygame.Rect(70, 300, 140, 32)

    running = True
    while running:
        screen.fill((0x82, 0x14, 0x7D))
        screen.blit(text0, (67, 180))
        pygame.draw.rect(screen, (0xFF, 0xA4, 0xDB), start_button)
        screen.blit(text2, (147, 369))
        pygame.draw.rect(screen, (0xFF, 0xA4, 0xDB), records_button)
        screen.blit(text3, (127, 418))

        txt_surface = font1.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_rect.w = width
        screen.fill((0xFF, 0xA4, 0xDB), (70, 300, width, 32))
        screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.draw.rect(screen, color, input_rect, 2)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if start_button.collidepoint(mouse_pos):
                        running = False
                        game(text)
                        pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if records_button.collidepoint(mouse_pos):
                        running = False
                        records()
                        pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        pygame.display.flip()


def detect_collision_t(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


def game(user_name='anon'):
    screen = pygame.display.set_mode((360, 640))
    pygame.display.set_caption('Арканоид - Игра')
    counter = 0
    font1 = pygame.font.Font('big-shot.ttf', 24)
    return_button = pygame.Rect(121, 361, 118, 43)

    # paddle settings
    paddle_w = 80
    paddle_h = 15
    paddle_speed = 5
    paddle = pygame.Rect(360 // 2 - paddle_w // 2, 640 - paddle_h - 10, paddle_w, paddle_h)
    # ball settings
    ball_radius = 10
    ball_speed = 2
    ball_rect = int(ball_radius * 2 ** 0.5)
    ball = pygame.Rect(random.randrange(ball_rect, 360 - ball_rect), 640 // 2, ball_rect, ball_rect)
    dx, dy = 1, -1
    # blocks settings
    color_list = [(0xFF, 0x1C, 0x1C), (0x6A, 0xC7, 0x20), (0x43, 0x61, 0xFF),
                  (0xFF, 0xB2, 0x1C)]  # red, green, blue, yellow

    block_list = []
    color_blocks = []
    Facade().LoadLevels('level.txt', block_list, color_blocks, color_list)
    clock = pygame.time.Clock()

    def detect_collision(dx, dy, ball, rect):
        if dx > 0:
            delta_x = ball.right - rect.left
        else:
            delta_x = rect.right - ball.left
        if dy > 0:
            delta_y = ball.bottom - rect.top
        else:
            delta_y = rect.bottom - ball.top

        if abs(delta_x - delta_y) < 10:
            dx, dy = -dx, -dy
        elif delta_x > delta_y:
            dy = -dy
        elif delta_y > delta_x:
            dx = -dx
        return dx, dy

    def end_of_game():
        pygame.draw.rect(screen, (0xFF, 0xA4, 0xDB), return_button)
        screen.blit(font1.render(str(counter), True, (0xF5, 0xF5, 0xF5)), (147, 369))
        Facade().UpdateRecords('Records.txt', user_name, 1, counter)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if return_button.collidepoint(mouse_pos):
                        running = False
                        game()

        screen.fill((0x82, 0x14, 0x7D))
        # drawing world
        [pygame.draw.rect(screen, color_blocks[index], block) for index, block in enumerate(block_list)]
        pygame.draw.rect(screen, (0xFF, 0xA4, 0xDB), paddle)
        pygame.draw.circle(screen, pygame.Color('white'), ball.center, ball_radius)
        # ball movement
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy
        # collision left right
        if ball.centerx < ball_radius or ball.centerx > 360 - ball_radius:
            dx = -dx
        # collision top
        if ball.centery < ball_radius:
            dy = -dy
        # collision paddle
        if ball.colliderect(paddle) and dy > 0:
            dx, dy = detect_collision(dx, dy, ball, paddle)
            # if dx > 0:
            #     dx, dy = (-dx, -dy) if ball.centerx < paddle.centerx else (dx, -dy)
            # else:
            #     dx, dy = (-dx, -dy) if ball.centerx >= paddle.centerx else (dx, -dy)
        # collision blocks
        hit_index = ball.collidelist(block_list)
        if hit_index != -1:
            counter += 1
            hit_rect = block_list.pop(hit_index)
            hit_color = color_blocks.pop(hit_index)
            dx, dy = detect_collision(dx, dy, ball, hit_rect)
            # special effect
            hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
            pygame.draw.rect(screen, hit_color, hit_rect)
            # fps += 2
            print(counter)
        # win, game over
        if ball.bottom > 640:
            end_of_game()
        elif not len(block_list):
            end_of_game()
        # control
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if key[pygame.K_RIGHT] and paddle.right < 360:
            paddle.right += paddle_speed
        # update screen
        pygame.display.flip()
        clock.tick(60)

def records():
    screen = pygame.display.set_mode((360, 640))
    pygame.display.set_caption('Арканоид - Рекорды')
    font1 = pygame.font.Font('big-shot.ttf', 20)
    return_button = pygame.Rect(121, 361, 118, 43)
    textBack = font1.render("Repeat", True, (0xF5, 0xF5, 0xF5))
    text = []
    Facade().LoadRecords('Records.txt', text, font1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if return_button.collidepoint(mouse_pos):
                        running = False
                        main_menu()

        screen.fill((0x82, 0x14, 0x7D))
        [screen.blit(raw, (10, 10 + i * 20)) for i, raw in enumerate(text)]
        pygame.draw.rect(screen, (0xFF, 0xA4, 0xDB), return_button)
        screen.blit(textBack, (127, 364))

        # update screen
        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    main_menu()
