"""
Game Development: Particle system and simple physics simulation.
"""
import math
import random
from dataclasses import dataclass, field
from typing import Iterator

# ═══════════════════════════════════════════
# 1. 2D Vector
# ═══════════════════════════════════════════
@dataclass
class Vec2:
    x: float = 0.0
    y: float = 0.0

    def __add__(self, o): return Vec2(self.x + o.x, self.y + o.y)
    def __sub__(self, o): return Vec2(self.x - o.x, self.y - o.y)
    def __mul__(self, s): return Vec2(self.x * s,   self.y * s)
    def __iadd__(self, o): self.x += o.x; self.y += o.y; return self
    def length(self): return math.hypot(self.x, self.y)
    def normalized(self):
        l = self.length()
        return Vec2(self.x/l, self.y/l) if l else Vec2(0, 0)
    def __repr__(self): return f"({self.x:.2f}, {self.y:.2f})"

# ═══════════════════════════════════════════
# 2. Particle
# ═══════════════════════════════════════════
@dataclass
class Particle:
    pos:      Vec2 = field(default_factory=Vec2)
    vel:      Vec2 = field(default_factory=Vec2)
    life:     float = 1.0   # seconds remaining
    max_life: float = 1.0
    mass:     float = 1.0
    color:    str   = "white"
    size:     float = 4.0

    @property
    def alive(self) -> bool:
        return self.life > 0

    @property
    def alpha(self) -> float:
        """0.0 (dead) → 1.0 (fresh)."""
        return max(0.0, self.life / self.max_life)

    def update(self, dt: float, gravity: Vec2) -> None:
        if not self.alive:
            return
        self.vel += gravity * dt
        self.pos += self.vel * dt
        self.life -= dt

# ═══════════════════════════════════════════
# 3. Particle Emitter
# ═══════════════════════════════════════════
class ParticleEmitter:
    def __init__(
        self,
        pos: Vec2,
        *,
        rate: float = 30,          # particles/second
        lifetime: float = 2.0,
        lifetime_variance: float = 0.5,
        speed: float = 60,
        speed_variance: float = 20,
        spread: float = math.pi,   # full circle
        direction: float = -math.pi/2,  # upward
        colors: list[str] = None,
        gravity: Vec2 = None,
    ):
        self.pos = pos
        self.rate = rate
        self.lifetime = lifetime
        self.lifetime_variance = lifetime_variance
        self.speed = speed
        self.speed_variance = speed_variance
        self.spread = spread
        self.direction = direction
        self.colors = colors or ["white"]
        self.gravity = gravity or Vec2(0, 0)
        self._particles: list[Particle] = []
        self._accumulator: float = 0.0
        self.active = True

    def _spawn(self) -> Particle:
        angle = self.direction + random.uniform(-self.spread/2, self.spread/2)
        spd   = self.speed + random.uniform(-self.speed_variance, self.speed_variance)
        life  = self.lifetime + random.uniform(-self.lifetime_variance, self.lifetime_variance)
        life  = max(0.1, life)
        return Particle(
            pos=Vec2(self.pos.x + random.uniform(-2, 2),
                     self.pos.y + random.uniform(-2, 2)),
            vel=Vec2(math.cos(angle) * spd, math.sin(angle) * spd),
            life=life, max_life=life,
            color=random.choice(self.colors),
            size=random.uniform(2, 6),
        )

    def update(self, dt: float) -> None:
        # Update existing particles
        self._particles = [p for p in self._particles if p.alive]
        for p in self._particles:
            p.update(dt, self.gravity)

        # Spawn new particles
        if self.active:
            self._accumulator += dt * self.rate
            n = int(self._accumulator)
            self._accumulator -= n
            for _ in range(n):
                self._particles.append(self._spawn())

    @property
    def particles(self) -> list[Particle]:
        return self._particles

    @property
    def count(self) -> int:
        return len(self._particles)

# ═══════════════════════════════════════════
# 4. Preset emitter types
# ═══════════════════════════════════════════
def fire_emitter(pos: Vec2) -> ParticleEmitter:
    return ParticleEmitter(
        pos, rate=50, lifetime=1.2, lifetime_variance=0.4,
        speed=80, speed_variance=30, spread=0.6,
        direction=-math.pi/2,
        colors=["red", "orange", "yellow", "white"],
        gravity=Vec2(0, -20),
    )

def explosion_emitter(pos: Vec2) -> ParticleEmitter:
    e = ParticleEmitter(
        pos, rate=200, lifetime=0.8, lifetime_variance=0.2,
        speed=150, speed_variance=80, spread=math.tau,
        colors=["red", "orange", "white"],
        gravity=Vec2(0, 50),
    )
    e.active = False  # burst-only
    return e

def snow_emitter(pos: Vec2) -> ParticleEmitter:
    return ParticleEmitter(
        pos, rate=20, lifetime=4.0, lifetime_variance=1.0,
        speed=30, speed_variance=10, spread=0.3,
        direction=math.pi/2,  # downward
        colors=["white", "lightblue"],
        gravity=Vec2(5, 100),  # slight wind + gravity
    )

# ═══════════════════════════════════════════
# 5. Simple physics body
# ═══════════════════════════════════════════
@dataclass
class PhysicsBody:
    pos:   Vec2 = field(default_factory=Vec2)
    vel:   Vec2 = field(default_factory=Vec2)
    accel: Vec2 = field(default_factory=Vec2)
    mass:  float = 1.0
    restitution: float = 0.7   # bounciness 0-1

    def apply_force(self, force: Vec2) -> None:
        self.accel += force * (1.0 / self.mass)

    def update(self, dt: float) -> None:
        self.vel += self.accel * dt
        self.pos += self.vel * dt
        self.accel = Vec2(0, 0)  # reset each frame

    def apply_friction(self, coeff: float) -> None:
        self.vel *= max(0, 1.0 - coeff)

def simulate_projectile(
    pos: Vec2, vel: Vec2, gravity: float = 9.81,
    dt: float = 0.05, max_t: float = 5.0
) -> list[Vec2]:
    """Simulate a projectile; stop when y <= 0."""
    body = PhysicsBody(pos=Vec2(pos.x, pos.y), vel=Vec2(vel.x, vel.y))
    path: list[Vec2] = [Vec2(body.pos.x, body.pos.y)]
    t = 0.0
    while body.pos.y >= 0 and t < max_t:
        body.apply_force(Vec2(0, gravity * body.mass))
        body.update(dt)
        path.append(Vec2(body.pos.x, body.pos.y))
        t += dt
    return path

if __name__ == "__main__":
    print("=== Particle Emitter Simulation ===\n")

    # Simulate fire emitter for 3 frames
    fire = fire_emitter(Vec2(200, 400))
    for frame in range(3):
        fire.update(0.05)  # 50ms per frame
        print(f"Frame {frame+1}: {fire.count} particles alive")

    # Sample a few live particles
    print("\nSample particles:")
    for p in fire.particles[:3]:
        print(f"  pos={p.pos} vel={p.vel} alpha={p.alpha:.2f}")

    print("\n=== Explosion Burst ===")
    exp = explosion_emitter(Vec2(300, 300))
    # Manually spawn a burst
    exp.active = True
    exp.rate = 500
    exp.update(0.05)          # one frame burst
    exp.active = False
    pre = exp.count
    exp.update(0.5)           # let them die
    print(f"After burst: {pre} → {exp.count} particles")

    print("\n=== Projectile Trajectory ===")
    # 45° launch at 40 m/s
    import math as _math
    angle = _math.radians(45)
    path = simulate_projectile(
        pos=Vec2(0, 0),
        vel=Vec2(_math.cos(angle)*40, -_math.sin(angle)*40),  # negative y = up
        gravity=9.81, dt=0.1,
    )
    peak_y = min(p.y for p in path)
    landing = path[-1]
    print(f"  Launch angle: 45°, speed: 40 m/s")
    print(f"  Points: {len(path)}, peak height: {abs(peak_y):.1f}m")
    print(f"  Landing: x={landing.x:.1f}m, y={landing.y:.1f}m")

    print("\n=== Physics Body ===")
    body = PhysicsBody(pos=Vec2(0, 10), mass=2.0, restitution=0.7)
    body.vel = Vec2(5, 0)
    print(f"Initial: pos={body.pos}, vel={body.vel}")
    body.apply_force(Vec2(0, 9.81 * body.mass))  # gravity
    body.update(0.1)
    print(f"After 0.1s with gravity: pos={body.pos}, vel={body.vel}")
