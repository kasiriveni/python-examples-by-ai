"""
Game Development: Scene management and game loop architecture.
"""
import time
import collections
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable

# ═══════════════════════════════════════════
# 1. Events
# ═══════════════════════════════════════════
@dataclass
class Event:
    type: str
    data: dict = field(default_factory=dict)

class EventBus:
    """Simple publish-subscribe event bus."""
    def __init__(self):
        self._handlers: dict[str, list[Callable[[Event], None]]] = collections.defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        self._handlers[event_type].remove(handler)

    def post(self, event: Event) -> None:
        for handler in self._handlers[event.type]:
            handler(event)

    def post_type(self, event_type: str, **data) -> None:
        self.post(Event(event_type, data))

# ═══════════════════════════════════════════
# 2. Scene system
# ═══════════════════════════════════════════
class Scene(ABC):
    """Base class for all game scenes (screens)."""

    def __init__(self, name: str):
        self.name = name
        self.bus: EventBus | None = None

    def on_enter(self, data: dict | None = None) -> None:
        """Called when transitioning INTO this scene."""
        print(f"  [{self.name}] enter(data={data})")

    def on_exit(self) -> None:
        """Called when leaving this scene."""
        print(f"  [{self.name}] exit()")

    @abstractmethod
    def update(self, dt: float) -> None: ...

    @abstractmethod
    def render(self) -> None: ...

class MainMenuScene(Scene):
    def __init__(self): super().__init__("MainMenu")
    def update(self, dt): pass
    def render(self): print(f"  [{self.name}] RENDER: [New Game] [Load] [Quit]")

class GameScene(Scene):
    def __init__(self):
        super().__init__("Game")
        self.player_x = 0.0
        self.elapsed = 0.0

    def update(self, dt):
        self.player_x += 100 * dt   # pixels/sec
        self.elapsed += dt
        if self.elapsed >= 2.0 and self.bus:
            # Trigger a game-over after 2 seconds of play
            self.bus.post_type("game_over", score=int(self.player_x))

    def render(self):
        print(f"  [{self.name}] RENDER: player_x={self.player_x:.1f}")

class GameOverScene(Scene):
    def __init__(self):
        super().__init__("GameOver")
        self.score = 0

    def on_enter(self, data=None):
        super().on_enter(data)
        self.score = (data or {}).get("score", 0)

    def update(self, dt): pass
    def render(self): print(f"  [{self.name}] RENDER: GAME OVER — Score: {self.score}")

class LoadingScene(Scene):
    def __init__(self, target_scene: str, assets: list[str]):
        super().__init__("Loading")
        self._target = target_scene
        self._assets = list(assets)
        self._loaded = 0
        self._done = False

    def update(self, dt):
        if self._loaded < len(self._assets):
            print(f"  [{self.name}] Loading: {self._assets[self._loaded]}")
            self._loaded += 1
        else:
            self._done = True
            if self.bus:
                self.bus.post_type("loading_done", target=self._target)

    def render(self):
        pct = int(100 * self._loaded / max(1, len(self._assets)))
        bar = "#" * (pct // 10) + "." * (10 - pct // 10)
        print(f"  [{self.name}] RENDER: [{bar}] {pct}%")

# ═══════════════════════════════════════════
# 3. Scene manager (stack-based)
# ═══════════════════════════════════════════
class SceneManager:
    """
    Manages a stack of scenes.
    - push_scene: overlay a new scene (e.g. pause menu) without destroying current
    - pop_scene:  return to previous scene
    - switch_scene: replace top of stack
    """

    def __init__(self, bus: EventBus):
        self._stack: list[Scene] = []
        self._bus = bus
        self._pending: list[tuple[str, Scene | None, dict | None]] = []

        # Wire events to transitions
        bus.subscribe("switch_scene", self._on_switch)
        bus.subscribe("push_scene",   self._on_push)
        bus.subscribe("pop_scene",    self._on_pop)
        bus.subscribe("quit",         self._on_quit)

    # ── Public API ──────────────────────────
    def push_scene(self, scene: Scene, data: dict | None = None) -> None:
        scene.bus = self._bus
        if self._stack:
            self._stack[-1].on_exit()
        self._stack.append(scene)
        scene.on_enter(data)

    def pop_scene(self) -> Scene | None:
        if not self._stack:
            return None
        exiting = self._stack.pop()
        exiting.on_exit()
        if self._stack:
            self._stack[-1].on_enter(None)
        return exiting

    def switch_scene(self, scene: Scene, data: dict | None = None) -> None:
        self.pop_scene()
        self.push_scene(scene, data)

    @property
    def current(self) -> Scene | None:
        return self._stack[-1] if self._stack else None

    @property
    def depth(self) -> int:
        return len(self._stack)

    # ── Event handlers ──────────────────────
    def _on_switch(self, ev: Event) -> None:
        self._pending.append(("switch", ev.data.get("scene"), ev.data.get("data")))

    def _on_push(self, ev: Event) -> None:
        self._pending.append(("push", ev.data.get("scene"), ev.data.get("data")))

    def _on_pop(self, ev: Event) -> None:
        self._pending.append(("pop", None, None))

    def _on_quit(self, ev: Event) -> None:
        self._pending.append(("quit", None, None))

    def flush_pending(self) -> bool:
        """Apply deferred transitions. Returns False if a quit was requested."""
        for action, scene, data in self._pending:
            if action == "switch" and scene: self.switch_scene(scene, data)
            elif action == "push" and scene:  self.push_scene(scene, data)
            elif action == "pop":             self.pop_scene()
            elif action == "quit":
                self._pending.clear()
                return False
        self._pending.clear()
        return True

# ═══════════════════════════════════════════
# 4. Game loop with fixed timestep
# ═══════════════════════════════════════════
class GameLoop:
    """Fixed-timestep game loop (prevents spiral of death)."""

    def __init__(self, scene_manager: SceneManager, target_fps: int = 60):
        self._sm = scene_manager
        self._target_fps = target_fps
        self._fixed_dt = 1.0 / target_fps
        self._running = False
        self.frame_count = 0

    def run(self, max_frames: int | None = None) -> None:
        self._running = True
        accumulator = 0.0
        last_time = time.monotonic()

        while self._running:
            now = time.monotonic()
            frame_time = min(now - last_time, 0.25)   # cap at 250ms
            last_time = now
            accumulator += frame_time

            # Fixed-step updates
            while accumulator >= self._fixed_dt:
                if self._sm.current:
                    self._sm.current.update(self._fixed_dt)
                if not self._sm.flush_pending():
                    self._running = False
                    break
                accumulator -= self._fixed_dt

            # Render at display rate
            if self._sm.current:
                self._sm.current.render()

            self.frame_count += 1
            if max_frames and self.frame_count >= max_frames:
                break

        print(f"\n  [GameLoop] Stopped after {self.frame_count} frames")

# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    bus = EventBus()
    sm  = SceneManager(bus)
    loop = GameLoop(sm, target_fps=30)

    print("=== Boot into Main Menu ===")
    sm.push_scene(MainMenuScene())
    sm.current.render()

    print("\n=== Switch to Loading Screen ===")
    assets = ["player.png", "tileset.png", "music.ogg"]
    loading = LoadingScene(target_scene="game", assets=assets)

    def on_loading_done(ev: Event):
        print(f"\n  Event 'loading_done' → target={ev.data['target']}")
        game = GameScene()
        sm.switch_scene(game)

    bus.subscribe("loading_done", on_loading_done)

    def on_game_over(ev: Event):
        score = ev.data["score"]
        sm.switch_scene(GameOverScene(), {"score": score})
        loop._running = False  # stop demo after game over

    bus.subscribe("game_over", on_game_over)

    sm.switch_scene(loading)
    print(f"\n=== Running game loop (max 20 frames) ===")
    loop.run(max_frames=20)

    print(f"\n=== Final scene: {sm.current.name if sm.current else None} ===")
    if sm.current:
        sm.current.render()

    print("\n=== EventBus demo ===")
    log: list[str] = []
    bus2 = EventBus()
    bus2.subscribe("attack", lambda e: log.append(f"system1: {e.data}"))
    bus2.subscribe("attack", lambda e: log.append(f"system2: {e.data}"))
    bus2.post_type("attack", target="enemy", damage=25)
    for entry in log:
        print(f"  {entry}")
