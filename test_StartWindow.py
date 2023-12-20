import unittest
from StartWindow import detect_collision_t
import pygame
import random

ball_radius = 10
ball_speed = 2
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(0, 640 // 2, ball_rect, ball_rect)

rect = pygame.Rect(10 + 42 * 1, 10 + 42 * 1, 32, 32)

class TestDetectCollision(unittest.TestCase):

    def test_collision_dx_gt_0_dy_gt_0(self):
        dx, dy = detect_collision_t(1, 1, ball, rect)
        self.assertEqual(dx, -1)
        self.assertEqual(dy, -1)

    def test_collision_dx_gt_0_dy_lt_0(self):
        dx, dy = detect_collision_t(1, -1, ball, rect)
        self.assertEqual(dx, -1)
        self.assertEqual(dy, 1)

    def test_collision_dx_lt_0_dy_gt_0(self):
        dx, dy = detect_collision_t(-1, 1, ball, rect)
        self.assertEqual(dx, 1)
        self.assertEqual(dy, -1)

    def test_collision_dx_lt_0_dy_lt_0(self):
        dx, dy = detect_collision_t(-1, -1, ball, rect)
        self.assertEqual(dx, 1)
        self.assertEqual(dy, 1)

    def test_collision_dx_eq_0_dy_gt_0(self):
        dx, dy = detect_collision_t(0, 1, ball, rect)
        self.assertEqual(dx, 0)
        self.assertEqual(dy, -1)

    def test_collision_dx_eq_0_dy_lt_0(self):
        dx, dy = detect_collision_t(0, -1, ball, rect)
        self.assertEqual(dx, 0)
        self.assertEqual(dy, 1)

    def test_collision_dx_gt_0_dy_eq_0(self):
        dx, dy = detect_collision_t(1, 0, ball, rect)
        self.assertEqual(dx, -1)
        self.assertEqual(dy, 0)

    def test_collision_dx_lt_0_dy_eq_0(self):
        dx, dy = detect_collision_t(-1, 0, ball, rect)
        self.assertEqual(dx, 1)
        self.assertEqual(dy, 0)

    def test_collision_dx_eq_0_dy_eq_0(self):
        dx, dy = detect_collision_t(0, 0, ball, rect)
        self.assertEqual(dx, 0)
        self.assertEqual(dy, 0)


if __name__ == '__main__':
    unittest.main()