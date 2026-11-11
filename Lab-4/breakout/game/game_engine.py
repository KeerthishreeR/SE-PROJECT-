"""
GameEngine: owns the paddle, ball, and bricks.

Features: brick removal on last hit (Task 1), 3 lives + game over +
restart with R (Task 2), normal/strong/unbreakable bricks (Task 3),
and a score with a combo multiplier (Task 4).
"""

import pygame

from game.paddle import Paddle
from game.ball import Ball
from game.brick import Brick, NORMAL, STRONG, UNBREAKABLE
from game.collision import handle_ball_brick_collision
from game.renderer import WIDTH, HEIGHT

BRICK_ROWS = 4
BRICK_COLS = 8
BRICK_WIDTH = 68
BRICK_HEIGHT = 22
BRICK_GAP = 6
BRICK_TOP_MARGIN = 50


STARTING_LIVES = 3

POINTS_PER_HIT = 10
MAX_MULTIPLIER = 8

STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_WON = "won"


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """(Re)start a fresh game: full lives, new bricks, ball at start."""
        self.paddle = Paddle(x=WIDTH / 2, y=HEIGHT - 30)
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)
        self.bricks = self._build_bricks()
        self.lives = STARTING_LIVES
        self.score = 0
        self.combo = 0          # consecutive brick hits since the last miss
        self.state = STATE_PLAYING

    @property
    def multiplier(self):
        """Score multiplier: x1 to start, +1 per consecutive hit, capped."""
        return max(1, min(MAX_MULTIPLIER, self.combo))

    def _build_bricks(self):
        bricks = []
        total_width = BRICK_COLS * (BRICK_WIDTH + BRICK_GAP) - BRICK_GAP
        start_x = (WIDTH - total_width) / 2
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y = BRICK_TOP_MARGIN + row * (BRICK_HEIGHT + BRICK_GAP)
                bricks.append(Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, self._brick_kind(row, col)))
        return bricks

    @staticmethod
    def _brick_kind(row, col):
        """Layout: strong top row, unbreakable bricks on the edges of row 1."""
        if row == 1 and col in (0, BRICK_COLS - 1):
            return UNBREAKABLE
        if row == 0:
            return STRONG
        return NORMAL

    def _breakable_left(self):
        return sum(1 for b in self.bricks if b.breakable)

    def _reset_ball(self):
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)

    def handle_input(self, keys_pressed):
        if self.state != STATE_PLAYING:
            return
        dx = 0
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.paddle.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.paddle.speed
        self.paddle.move(dx, WIDTH)

    def handle_keydown(self, key):
        # Press R after the game ends to restart.
        if self.state in (STATE_GAME_OVER, STATE_WON) and key == pygame.K_r:
            self.reset()

    def _lose_life(self):
        self.lives -= 1
        self.combo = 0          # missing the ball resets the combo
        if self.lives <= 0:
            self.state = STATE_GAME_OVER
        else:
            self._reset_ball()

    def update(self):
        if self.state != STATE_PLAYING:
            return

        self.ball.update()
        self.ball.bounce_off_walls(WIDTH)

        if self.ball.get_rect().colliderect(self.paddle.get_rect()) and self.ball.vy > 0:
            self.ball.bounce_off_paddle(self.paddle.get_rect())

        for brick in self.bricks:
            if handle_ball_brick_collision(self.ball, brick):
                # Task 4: every hit on a breakable brick builds the combo
                # and scores points x the current multiplier. Hitting an
                # unbreakable brick neither scores nor breaks the combo.
                if brick.breakable:
                    self.combo += 1
                    self.score += POINTS_PER_HIT * self.multiplier
                # Task 1 fix: a brick whose hits run out is removed.
                # Unbreakable bricks never report destroyed.
                if brick.hit():
                    self.bricks.remove(brick)
                break

        if self._breakable_left() == 0:
            self.state = STATE_WON
            return

        if self.ball.is_below(HEIGHT):
            self._lose_life()

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.paddle, self.ball, self.bricks)
        renderer.draw_text(surface, font, f"Bricks left: {self._breakable_left()}", (10, 10))
        renderer.draw_text(surface, font, f"Score: {self.score}  x{self.multiplier}", (200, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (WIDTH - 110, 10))
        if self.state == STATE_GAME_OVER:
            renderer.draw_banner(surface, font, "GAME OVER - press R to restart")
        elif self.state == STATE_WON:
            renderer.draw_banner(surface, font, "YOU WIN! - press R to restart")
