# Core Python Concepts

## Core Themes
- Game loops, state management, and scene architecture.
- Rendering, animation, physics, and collision detection.
- Pathfinding and entity-component-style gameplay patterns.

## Core Theme Examples
- Example 1: Updating game state in a fixed-FPS loop.
- Example 2: AABB collision detection and sprite animation frames.
- Example 3: A* pathfinding and grid-based navigation.

## Files and Concepts
- collision_detection.py: AABB, circle collisions, SAT, spatial hashing
- game_basics.py: game loops, FPS control, delta time, state updates
- particle_system.py: particles, velocity, gravity, emitters, vector motion
- pathfinding.py: A star, Dijkstra, grid navigation, heuristics
- pygame_example.py: Pygame initialization, event loop, display updates, clock control
- scene_management.py: event buses, scenes, transitions, game architecture
- sprites_and_animation.py: sprite objects, animation frames, velocity, collisions
- state_machine_ecs.py: finite-state machines, ECS patterns, state transitions

## Core Example
This example updates a simple game state inside a short loop.

```python
state = {"x": 0, "velocity": 2}

for _ in range(3):
	state["x"] += state["velocity"]
	print(state["x"])

if state["x"] > 4:
	print("goal reached")
```
