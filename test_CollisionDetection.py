import pygame
import unittest

class CollisionDetectionTests(unittest.TestCase):
    def test_collision_from_right(self):
        dx, dy = detect_collision(1, 0, pygame.Rect(0, 0, 10, 10), pygame.Rect(5, 5, 10, 10))  # ball, rect
        self.assertEqual(dx, -1)
        self.assertEqual(dy, 0)

    def test_collision_from_left(self):
        dx, dy = detect_collision(-1, 0, pygame.Rect(0, 0, 10, 10), pygame.Rect(5, 5, 10, 10))
        self.assertEqual(dx, 1)
        self.assertEqual(dy, 0)

    def test_collision_from_bottom(self):
        dx, dy = detect_collision(0, 1, pygame.Rect(0, 0, 10, 10), pygame.Rect(5, 5, 10, 10))
        self.assertEqual(dx, 0)
        self.assertEqual(dy, -1)

    def test_collision_from_top(self):
        dx, dy = detect_collision(0, -1, pygame.Rect(0, 0, 10, 10), pygame.Rect(5, 5, 10, 10))
        self.assertEqual(dx, 0)
        self.assertEqual(dy, 1)

    def test_collision_diagonal(self):
        dx, dy = detect_collision(1, 1, pygame.Rect(0, 0, 10, 10), pygame.Rect(5, 5, 10, 10))
        self.assertEqual(dx, -1)
        self.assertEqual(dy, -1)


if __name__ == '__main__':
    unittest.main()
























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