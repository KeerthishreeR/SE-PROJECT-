# Breakout Lab

This project is a single-topic Breakout/Brick Breaker game using
**Pygame**. It introduces students to collision-triggered state
changes, a lives system, entity variety, and combo scoring, using a
small, readable object-oriented codebase.

---

## What's Provided

A working Breakout game with:

- A paddle moved with the arrow keys
- A ball that bounces off the walls and the paddle
- A grid of bricks that break on contact
- A live "bricks left" counter

It has **one deliberate bug** and **three features** left for you to
build. You are expected to **analyze**, **interact with an AI
assistant**, and **complete/fix** the game to make it fully functional
and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python main.py
```

**Controls:** Left/Right arrows to move the paddle.

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM
suggestions and your critical code review.

### Task 1: Fix ball–brick collision

> **What you'll see:** the ball bounces off bricks completely
> normally, but no matter how many times you hit a brick, it never
> breaks - the same bricks just stay there forever.
>
> **Why:** in `update()` (in `game/game_engine.py`), each hit does
> track a brick's remaining hits (`brick.hits_remaining -= 1`), but
> nothing ever checks that value to decide whether the brick should
> actually be destroyed and removed from play.
>
> **Fix it:** once a brick's hits are used up, it should actually be
> removed from the board.

### Task 2: Implement lives and game over

> Add a 3-life system. When the ball falls below the paddle, the
> player should lose one life and get another attempt (the ball
> resets to start). Display the remaining lives, end the game once
> all lives are used up, and provide a way to restart.

### Task 3: Add different brick types

> Introduce three brick types:
> - Normal: destroyed after one hit.
> - Strong: needs multiple hits before it's destroyed.
> - Unbreakable: never destroyed, no matter how many times it's hit.
>
> Give each type its own look so they're easy to tell apart, and make
> sure each behaves correctly when hit.

### Task 4: Implement combo scoring

> Add a score and combo multiplier. Destroying bricks back-to-back
> (without missing the ball in between) should raise the multiplier,
> making each further hit worth more. Missing the ball should reset
> the combo. Display both the score and the current multiplier.

---

## Expected Behavior

- Hitting a brick correctly reduces its remaining hits and actually
  removes it once those hits run out - a brick should never survive
  being hit more times than it's supposed to withstand.
- Losing all 3 lives ends the game with a clear message, and the game
  can be restarted.
- All three brick types are visually distinct, and each behaves
  correctly (one hit, multiple hits, or never destroyed).
- Consecutive brick hits build a combo that increases score per hit;
  missing the ball brings the combo back down.

---

## Folder Structure

```
breakout/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── paddle.py
│   ├── ball.py
│   ├── brick.py
│   ├── collision.py
│   └── renderer.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history
