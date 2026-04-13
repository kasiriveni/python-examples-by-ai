"""
Game Development: Game state machine and entity component system.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Type

# ═══════════════════════════════════════════
# 1. Finite State Machine
# ═══════════════════════════════════════════
class State(ABC):
    """Base class for all game states."""

    def __init__(self, machine: "StateMachine"):
        self.machine = machine

    def enter(self) -> None:
        """Called when transitioning INTO this state."""
        pass

    def exit(self) -> None:
        """Called when transitioning OUT of this state."""
        pass

    @abstractmethod
    def update(self, dt: float, events: list[str]) -> None:
        pass

    def __repr__(self):
        return self.__class__.__name__

class StateMachine:
    def __init__(self):
        self._states: dict[str, State] = {}
        self._current: State | None = None
        self._history: list[str] = []

    def add_state(self, name: str, state: State) -> "StateMachine":
        self._states[name] = state
        return self

    def change_to(self, name: str) -> None:
        if name not in self._states:
            raise KeyError(f"Unknown state: {name}")
        if self._current:
            self._current.exit()
            self._history.append(type(self._current).__name__)
        self._current = self._states[name]
        self._current.enter()
        print(f"  → {name}")

    def update(self, dt: float, events: list[str] = None) -> None:
        if self._current:
            self._current.update(dt, events or [])

    @property
    def current(self) -> str:
        return type(self._current).__name__ if self._current else "None"

# --- Game states ---
class MenuState(State):
    def enter(self): print("    [Menu] Showing main menu")
    def exit(self):  print("    [Menu] Leaving menu")
    def update(self, dt, events):
        if "START" in events:
            self.machine.change_to("playing")

class PlayingState(State):
    def __init__(self, machine):
        super().__init__(machine)
        self.score = 0
        self.time = 0.0

    def enter(self): print("    [Playing] Game started!")
    def exit(self):  print(f"    [Playing] Final score: {self.score}")

    def update(self, dt, events):
        self.time += dt
        self.score += int(dt * 10)
        if "PAUSE" in events:
            self.machine.change_to("paused")
        if "DIED" in events:
            self.machine.change_to("game_over")

class PausedState(State):
    def enter(self): print("    [Paused] Game paused")
    def update(self, dt, events):
        if "RESUME" in events:
            self.machine.change_to("playing")
        if "QUIT" in events:
            self.machine.change_to("menu")

class GameOverState(State):
    def enter(self): print("    [GameOver] You died!")
    def update(self, dt, events):
        if "RESTART" in events:
            self.machine.change_to("playing")
        if "QUIT" in events:
            self.machine.change_to("menu")

# ═══════════════════════════════════════════
# 2. Entity Component System (ECS)
# ═══════════════════════════════════════════
@dataclass
class Component:
    """Base component — just a data container."""
    pass

@dataclass
class Transform(Component):
    x: float = 0.0
    y: float = 0.0
    rotation: float = 0.0

@dataclass
class Velocity(Component):
    vx: float = 0.0
    vy: float = 0.0

@dataclass
class Health(Component):
    hp: int = 100
    max_hp: int = 100

    @property
    def alive(self): return self.hp > 0
    @property
    def pct(self): return self.hp / self.max_hp

@dataclass
class Renderable(Component):
    sprite: str = "?"
    layer: int = 0
    visible: bool = True

@dataclass
class Tag(Component):
    value: str = ""

class Entity:
    _next_id = 0

    def __init__(self):
        Entity._next_id += 1
        self.id = Entity._next_id
        self._components: dict[type, Component] = {}

    def add(self, component: Component) -> "Entity":
        self._components[type(component)] = component
        return self

    def get(self, comp_type: Type[Component]) -> Component | None:
        return self._components.get(comp_type)

    def has(self, *comp_types: type) -> bool:
        return all(t in self._components for t in comp_types)

    def remove(self, comp_type: type) -> "Entity":
        self._components.pop(comp_type, None)
        return self

    def __repr__(self):
        comps = [type(c).__name__ for c in self._components.values()]
        return f"Entity({self.id} [{', '.join(comps)}])"

class World:
    def __init__(self):
        self._entities: list[Entity] = []
        self._systems: list["System"] = []

    def create_entity(self, *components: Component) -> Entity:
        e = Entity()
        for c in components:
            e.add(c)
        self._entities.append(e)
        return e

    def destroy(self, entity: Entity) -> None:
        self._entities.remove(entity)

    def query(self, *comp_types: type) -> list[Entity]:
        return [e for e in self._entities if e.has(*comp_types)]

    def add_system(self, system: "System") -> "World":
        self._systems.append(system)
        return self

    def update(self, dt: float) -> None:
        for system in self._systems:
            system.process(self, dt)

class System(ABC):
    @abstractmethod
    def process(self, world: World, dt: float) -> None: pass

class MovementSystem(System):
    def process(self, world: World, dt: float) -> None:
        for entity in world.query(Transform, Velocity):
            t = entity.get(Transform)
            v = entity.get(Velocity)
            t.x += v.vx * dt
            t.y += v.vy * dt

class BoundarySystem(System):
    def __init__(self, width: float, height: float):
        self.w, self.h = width, height

    def process(self, world: World, dt: float) -> None:
        for entity in world.query(Transform, Velocity):
            t = entity.get(Transform)
            v = entity.get(Velocity)
            if t.x < 0 or t.x > self.w: v.vx *= -1
            if t.y < 0 or t.y > self.h: v.vy *= -1

class RenderSystem(System):
    def process(self, world: World, dt: float) -> None:
        renderables = world.query(Transform, Renderable)
        renderables.sort(key=lambda e: e.get(Renderable).layer)
        for entity in renderables:
            t = entity.get(Transform)
            r = entity.get(Renderable)
            if r.visible:
                tag = entity.get(Tag)
                name = tag.value if tag else f"entity{entity.id}"
                print(f"  Render '{name}' [{r.sprite}] @ ({t.x:.1f}, {t.y:.1f})")

if __name__ == "__main__":
    print("=== State Machine ===")
    sm = StateMachine()
    playing = PlayingState(sm)
    sm.add_state("menu",      MenuState(sm))
    sm.add_state("playing",   playing)
    sm.add_state("paused",    PausedState(sm))
    sm.add_state("game_over", GameOverState(sm))

    sm.change_to("menu")
    sm.update(0.1, ["START"])
    sm.update(0.5, [])         # score accumulates
    sm.update(0.5, ["PAUSE"])
    sm.update(0.1, ["RESUME"])
    sm.update(0.3, ["DIED"])
    sm.update(0.1, ["RESTART"])
    print(f"\nHistory: {sm._history}")
    print(f"Score: {playing.score}")

    print("\n=== ECS ===")
    world = World()
    world.add_system(MovementSystem())
    world.add_system(BoundarySystem(100, 100))
    world.add_system(RenderSystem())

    player = world.create_entity(
        Transform(50, 50),
        Velocity(20, 15),
        Health(100),
        Renderable("[P]", layer=1),
        Tag("player"),
    )

    for i in range(3):
        world.create_entity(
            Transform(10 + i*20, 10 + i*15),
            Velocity(-5, 3),
            Health(30),
            Renderable("(E)", layer=0),
            Tag(f"enemy{i}"),
        )

    print(f"Entities: {len(world._entities)}")
    print(f"\n--- Frame 1 (dt=0.5s) ---")
    world.update(0.5)
