"""
Ball: bounces around the play area and breaks bricks on contact.
"""

import pygame


class Ball:
    def __init__(self, x, y, radius=8, speed=5):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = speed * 0.6
        self.vy = -speed

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def bounce_off_walls(self, width):
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx
        elif self.x + self.radius > width:
            self.x = width - self.radius
            self.vx = -self.vx
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy

    def bounce_off_paddle(self, paddle_rect):
        self.vy = -abs(self.vy)
        self.y = paddle_rect.top - self.radius
        # Slight angle change based on where the ball hit the paddle,
        # so it doesn't just bounce straight up and down forever.
        offset = (self.x - paddle_rect.centerx) / (paddle_rect.width / 2)
        self.vx = offset * abs(self.vy) * 0.75

    def is_below(self, height):
        return self.y - self.radius > height

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )
