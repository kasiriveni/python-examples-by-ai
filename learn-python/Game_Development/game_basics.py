"""
Game Development: Pygame basics - sprites, movement, and simple game loop.
"""

# NOTE: Requires `pip install pygame`
# This file demonstrates game development concepts

# === Game Loop Pattern (pure Python) ===
import time

class SimpleGameLoop:
    """Demonstrates the core game loop pattern without pygame."""

    def __init__(self, target_fps=60):
        self.target_fps = target_fps
        self.frame_time = 1.0 / target_fps
        self.running = False
        self.frame_count = 0

    def update(self, dt):
        """Update game state."""
        pass

    def render(self):
        """Render game state."""
        pass

    def handle_input(self):
        """Handle user input."""
        pass

    def run(self, max_frames=10):
        """Main game loop."""
        self.running = True
        last_time = time.perf_counter()

        while self.running and self.frame_count < max_frames:
            current_time = time.perf_counter()
            dt = current_time - last_time
            last_time = current_time

            self.handle_input()
            self.update(dt)
            self.render()

            self.frame_count += 1
            sleep_time = self.frame_time - (time.perf_counter() - current_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

# === Entity Component System (simple) ===
class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __repr__(self):
        return f"({self.x:.1f}, {self.y:.1f})"

class Entity:
    _next_id = 0

    def __init__(self, name, position=None):
        Entity._next_id += 1
        self.id = Entity._next_id
        self.name = name
        self.position = position or Vector2()
        self.velocity = Vector2()
        self.active = True

    def update(self, dt):
        self.position = self.position + self.velocity * dt

    def __repr__(self):
        return f"{self.name}(pos={self.position})"

# === Tile Map ===
class TileMap:
    TILES = {0: '.', 1: '#', 2: '~', 3: 'T', 4: 'D'}

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0] * width for _ in range(height)]

    def set_tile(self, x, y, tile_id):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = tile_id

    def render(self):
        for row in self.grid:
            print(' '.join(self.TILES.get(t, '?') for t in row))

# === Collision Detection ===
class AABB:
    """Axis-Aligned Bounding Box."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersects(self, other):
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)

# === State Machine for game states ===
class GameState:
    def enter(self): pass
    def exit(self): pass
    def update(self, dt): pass
    def render(self): pass

class MenuState(GameState):
    def enter(self):
        print("  [Menu] Press ENTER to start")

class PlayState(GameState):
    def enter(self):
        print("  [Playing] Game started!")

    def update(self, dt):
        print(f"  [Playing] Updating... dt={dt:.4f}")

class GameOverState(GameState):
    def enter(self):
        print("  [Game Over] Final score displayed")

class StateMachine:
    def __init__(self):
        self.current_state = None
        self.states = {}

    def add_state(self, name, state):
        self.states[name] = state

    def change_state(self, name):
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[name]
        self.current_state.enter()

if __name__ == "__main__":
    # Game loop demo
    print("=== Game Loop ===")
    game = SimpleGameLoop(target_fps=30)
    game.run(max_frames=3)
    print(f"Ran {game.frame_count} frames")

    # Entity system
    print("\n=== Entities ===")
    player = Entity("Player", Vector2(100, 100))
    player.velocity = Vector2(50, 0)
    for i in range(5):
        player.update(0.1)
        print(f"  Frame {i}: {player}")

    # Tile map
    print("\n=== Tile Map ===")
    tilemap = TileMap(8, 5)
    for x in range(8):
        tilemap.set_tile(x, 0, 1)
        tilemap.set_tile(x, 4, 1)
    tilemap.set_tile(3, 2, 3)
    tilemap.set_tile(5, 2, 4)
    tilemap.set_tile(1, 3, 2)
    tilemap.set_tile(2, 3, 2)
    tilemap.render()

    # Collision
    print("\n=== Collision ===")
    a = AABB(0, 0, 50, 50)
    b = AABB(30, 30, 50, 50)
    c = AABB(100, 100, 50, 50)
    print(f"A overlaps B: {a.intersects(b)}")
    print(f"A overlaps C: {a.intersects(c)}")

    # State machine
    print("\n=== State Machine ===")
    sm = StateMachine()
    sm.add_state("menu", MenuState())
    sm.add_state("play", PlayState())
    sm.add_state("gameover", GameOverState())
    sm.change_state("menu")
    sm.change_state("play")
    sm.current_state.update(0.016)
    sm.change_state("gameover")
