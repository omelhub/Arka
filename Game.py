import sys
import pygame
from pygame.locals import *
import random
from Facade import Facade

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((360, 640))
        pygame.display.set_caption('Арканоид - Игра')
        self.counter = 0
        self.font1 = pygame.font.Font('big-shot.ttf', 24)
        self.return_button = pygame.Rect(121, 361, 118, 43)

        self.paddle_w = 80
        self.paddle_h = 15
        self.paddle_speed = 5
        self.paddle = pygame.Rect(360 // 2 - self.paddle_w // 2, 640 - self.paddle_h - 10, self.paddle_w, self.paddle_h)

        self.ball_radius = 10
        self.ball_speed = 2
        self.ball_rect = int(self.ball_radius * 2 ** 0.5)
        self.ball = pygame.Rect(random.randrange(self.ball_rect, 360 - self.ball_rect), 640 // 2, self.ball_rect, self.ball_rect)
        self.dx, self.dy = 1, -1

        self.color_list = [(0xFF, 0x1C, 0x1C), (0x6A, 0xC7, 0x20), (0x43, 0x61, 0xFF), (0xFF, 0xB2, 0x1C)]
        self.block_list = []
        self.color_blocks = []
        Facade().LoadLevels('level.txt', self.block_list, self.color_blocks, self.color_list)
        self.clock = pygame.time.Clock()

    def detect_collision(self, dx, dy, ball, rect):
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

    def end_of_game(self):
        pygame.draw.rect(self.screen, (0xFF, 0xA4, 0xDB), self.return_button)
        self.screen.blit(self.font1.render(str(self.counter), True, (0xF5, 0xF5, 0xF5)), (147, 369))
        Facade().UpdateRecords('Records.txt', user_name, 1, self.counter)

    def run(self):
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
                        if self.return_button.collidepoint(mouse_pos):
                            running = False
                            self.run()

            self.screen.fill((0x82, 0x14, 0x7D))

            [pygame.draw.rect(self.screen, self.color_blocks[index], block) for index, block in enumerate(self.block_list)]
            pygame.draw.rect(self.screen, (0xFF, 0xA4, 0xDB), self.paddle)
            pygame.draw.circle(self.screen, pygame.Color('white'), self.ball.center, self.ball_radius)

            self.ball.x += self