"""
collision: ball-vs-brick collision handling.
"""


def handle_ball_brick_collision(ball, brick):
    """
    If the ball overlaps the brick, bounce it off and return True.
    """
    if ball.get_rect().colliderect(brick.get_rect()):
        ball.vy = -ball.vy
        return True
    return False
