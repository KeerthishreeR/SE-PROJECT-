"""
Paddle: the player-controlled paddle at the bottom of the screen.
"""

import pygame


class Paddle:
    def __init__(self, x, y, width=90, height=16, speed=7):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self, dx, bounds_width):
        self.x += dx
        half = self.width / 2
        self.x = max(half, min(bounds_width - half, self.x))

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
