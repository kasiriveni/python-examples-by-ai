"""
Game Development: Sprites and Animation (without pygame for portability).
Demonstrates sprite data structures, animation frames, and game object management.
"""
import time
import math
from dataclasses import dataclass, field
from typing import Optional

# === Vector2D ===
@dataclass
class Vector2:
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other): return Vector2(self.x + other.x, self.y + other.y)
    def __sub__(self, other): return Vector2(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar): return Vector2(self.x * scalar, self.y * scalar)
    def magnitude(self): return math.sqrt(self.x**2 + self.y**2)
    def normalize(self):
        m = self.magnitude()
        return Vector2(self.x / m, self.y / m) if m > 0 else Vector2()
    def __repr__(self): return f"({self.x:.1f}, {self.y:.1f})"

# === Sprite ===
@dataclass
class Sprite:
    name: str
    position: Vector2 = field(default_factory=Vector2)
    velocity: Vector2 = field(default_factory=Vector2)
    width: int = 32
    height: int = 32
    visible: bool = True
    alive: bool = True
    tag: str = "default"

    # Animation
    frames: list[str] = field(default_factory=list)
    frame_index: int = 0
    frame_duration: float = 0.1   # seconds per frame
    _frame_timer: float = field(default=0.0, init=False, repr=False)
    loop: bool = True

    def current_frame(self) -> str:
        if not self.frames:
            return "[empty]"
        return self.frames[self.frame_index]

    def update(self, dt: float) -> None:
        # Move
        self.position = self.position + self.velocity * dt
        # Animate
        if len(self.frames) > 1:
            self._frame_timer += dt
            if self._frame_timer >= self.frame_duration:
                self._frame_timer = 0
                self.frame_index += 1
                if self.frame_index >= len(self.frames):
                    if self.loop:
                        self.frame_index = 0
                    else:
                        self.frame_index = len(self.frames) - 1
                        self.alive = False

    @property
    def rect(self):
        return (self.position.x, self.position.y,
                self.position.x + self.width, self.position.y + self.height)

    def collides_with(self, other: "Sprite") -> bool:
        ax1, ay1, ax2, ay2 = self.rect
        bx1, by1, bx2, by2 = other.rect
        return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1

# === AnimationController ===
class AnimationController:
    """Manages multiple animation states for a sprite."""

    def __init__(self):
        self.animations: dict[str, list[str]] = {}
        self.current: str = ""
        self.index: int = 0
        self.timer: float = 0.0
        self.fps: float = 8.0

    def add(self, name: str, frames: list[str]) -> "AnimationController":
        self.animations[name] = frames
        if not self.current:
            self.current = name
        return self

    def play(self, name: str) -> None:
        if name != self.current and name in self.animations:
            self.current = name
            self.index = 0
            self.timer = 0.0

    def update(self, dt: float) -> str:
        frames = self.animations.get(self.current, [])
        if not frames:
            return "no_frame"
        self.timer += dt
        if self.timer >= 1.0 / self.fps:
            self.timer = 0.0
            self.index = (self.index + 1) % len(frames)
        return frames[self.index]

# === SpriteGroup ===
class SpriteGroup:
    def __init__(self):
        self._sprites: list[Sprite] = []

    def add(self, sprite: Sprite) -> None:
        self._sprites.append(sprite)

    def remove_dead(self) -> int:
        before = len(self._sprites)
        self._sprites = [s for s in self._sprites if s.alive]
        return before - len(self._sprites)

    def update(self, dt: float) -> None:
        for s in self._sprites:
            if s.alive:
                s.update(dt)

    def get_by_tag(self, tag: str) -> list[Sprite]:
        return [s for s in self._sprites if s.tag == tag]

    def check_collisions(self, a_tag: str, b_tag: str) -> list[tuple]:
        pairs = []
        group_a = self.get_by_tag(a_tag)
        group_b = self.get_by_tag(b_tag)
        for a in group_a:
            for b in group_b:
                if a.collides_with(b):
                    pairs.append((a, b))
        return pairs

    def __len__(self): return len(self._sprites)
    def __iter__(self): return iter(self._sprites)

if __name__ == "__main__":
    print("=== Sprite System Demo ===\n")

    # Player with walking animation
    player = Sprite(
        name="player",
        position=Vector2(100, 200),
        velocity=Vector2(60, 0),
        tag="player",
        frames=["[idle]", "[walk1]", "[walk2]", "[walk3]"],
        frame_duration=0.125,
    )

    # Enemies
    enemies = [
        Sprite(name=f"enemy_{i}", position=Vector2(300 + i*50, 200),
               velocity=Vector2(-30, 0), tag="enemy",
               frames=["(E1)", "(E2)"], frame_duration=0.2)
        for i in range(3)
    ]

    group = SpriteGroup()
    group.add(player)
    for e in enemies:
        group.add(e)

    print(f"Sprites: {len(group)}")
    print(f"Player frame: {player.current_frame()}")

    # Simulate 1 second at 10 fps
    dt = 0.1
    for tick in range(10):
        group.update(dt)
        print(f"  t={tick*dt:.1f}s | player={player.position} | frame={player.current_frame()}")

    # Check collisions
    print(f"\n=== Collision Check ===")
    player.position = Vector2(300, 200)
    hits = group.check_collisions("player", "enemy")
    print(f"Player pos {player.position}, collisions: {len(hits)}")

    # Animation controller
    print("\n=== Animation Controller ===")
    anim = AnimationController()
    anim.add("idle", ["[i1]", "[i2]"])
    anim.add("run", ["[r1]", "[r2]", "[r3]", "[r4]"])
    anim.add("jump", ["[j1]", "[j2]", "[j3]"])

    anim.play("run")
    frames_seen = []
    for _ in range(12):
        frames_seen.append(anim.update(0.1))
    print(f"Run frames: {frames_seen}")

    anim.play("jump")
    jump_frames = [anim.update(0.1) for _ in range(6)]
    print(f"Jump frames: {jump_frames}")
