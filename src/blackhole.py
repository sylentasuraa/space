"""
Black Hole Particle Simulator
------------------------------
Click anywhere on screen to spawn ~100 particles at that location.
They get pulled toward the black hole in the middle with real
Newtonian gravity + inertia, so you get nice parabolic / slingshot /
orbit-like paths depending on how fast/tangential they enter.

Particles:
  - live for a random 10-20 seconds, then fade out and disappear
  - get absorbed (disappear instantly) if they fall past the event horizon
  - are capped in total count so performance stays smooth even if you spam-click

Controls:
  - Left click: spawn ~100 particles at cursor
  - Hold left click + drag: spawn a stream of particles
  - R: clear all particles
  - ESC / close window: quit
"""

import pygame
import numpy as np

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 1000, 700
BLACK_HOLE_POS = np.array([WIDTH / 2, HEIGHT / 2], dtype=np.float64)

G = 999999.0           # gravitational strength (very strong -> tight, chaotic threading orbits)
BH_MASS = 1.0          # folded into G above, kept separate for clarity/tuning
EVENT_HORIZON_R = 14   # px - particles crossing this radius get absorbed
SOFTENING = 1.0        # very small -> sharp direction flips on close passes
MAX_SPEED = 4000.0     # speed cap so close slingshots don't numerically blow up

PARTICLES_PER_CLICK = 160
MAX_PARTICLES = 9000    # hard cap so nothing can bog down / crash

MIN_LIFETIME = 10.0     # seconds
MAX_LIFETIME = 20.0     # seconds

FPS = 60

TRAIL_FADE_ALPHA = 18   # lower = longer-lasting trails, higher = shorter trails

# ---------------------------------------------------------------------------
# Particle system stored as flat numpy arrays (vectorized = fast)
# ---------------------------------------------------------------------------
class ParticleSystem:
    def __init__(self, max_particles):
        self.max_particles = max_particles
        self.pos = np.zeros((0, 2), dtype=np.float64)
        self.prev_pos = np.zeros((0, 2), dtype=np.float64)  # for streak/motion-blur rendering
        self.vel = np.zeros((0, 2), dtype=np.float64)
        self.age = np.zeros((0,), dtype=np.float64)
        self.lifetime = np.zeros((0,), dtype=np.float64)
        self.hue = np.zeros((0,), dtype=np.float64)  # for slight color variation

    def spawn(self, x, y, count):
        if count <= 0:
            return
        # small random spread around the click point so it looks like a burst
        spread = 6.0
        new_pos = np.column_stack([
            np.random.normal(x, spread, count),
            np.random.normal(y, spread, count),
        ])

        # small random initial velocity in random directions (gives varied
        # parabola / slingshot paths once gravity takes over)
        speed = np.random.uniform(10, 90, count)
        angle = np.random.uniform(0, 2 * np.pi, count)
        new_vel = np.column_stack([np.cos(angle) * speed, np.sin(angle) * speed])

        new_age = np.zeros(count)
        new_lifetime = np.random.uniform(MIN_LIFETIME, MAX_LIFETIME, count)
        new_hue = np.random.uniform(0, 1, count)

        self.pos = np.vstack([self.pos, new_pos])
        self.prev_pos = np.vstack([self.prev_pos, new_pos])  # no motion yet on spawn frame
        self.vel = np.vstack([self.vel, new_vel])
        self.age = np.concatenate([self.age, new_age])
        self.lifetime = np.concatenate([self.lifetime, new_lifetime])
        self.hue = np.concatenate([self.hue, new_hue])

        # enforce cap: drop oldest particles first if over the limit
        if len(self.pos) > self.max_particles:
            excess = len(self.pos) - self.max_particles
            self.pos = self.pos[excess:]
            self.prev_pos = self.prev_pos[excess:]
            self.vel = self.vel[excess:]
            self.age = self.age[excess:]
            self.lifetime = self.lifetime[excess:]
            self.hue = self.hue[excess:]

    def clear(self):
        self.__init__(self.max_particles)

    def update(self, dt):
        if len(self.pos) == 0:
            return

        # --- gravity toward the black hole (vectorized over all particles) ---
        r_vec = BLACK_HOLE_POS - self.pos                   # (N, 2)
        dist2 = np.sum(r_vec ** 2, axis=1) + SOFTENING ** 2
        dist = np.sqrt(dist2)
        accel_mag = (G * BH_MASS) / dist2                   # (N,)
        accel = r_vec / dist[:, None] * accel_mag[:, None]  # direction * magnitude

        # inertia: velocity accumulates acceleration, position accumulates velocity
        self.vel += accel * dt

        # clamp extreme speeds (can happen on very close passes) so particles
        # stay numerically stable instead of teleporting off into nowhere
        speed = np.sqrt(np.sum(self.vel ** 2, axis=1))
        too_fast = speed > MAX_SPEED
        if np.any(too_fast):
            self.vel[too_fast] *= (MAX_SPEED / speed[too_fast])[:, None]

        self.prev_pos = self.pos.copy()
        self.pos = self.pos + self.vel * dt

        self.age += dt

        # --- removal conditions ---
        real_dist = np.sqrt(np.sum((self.pos - BLACK_HOLE_POS) ** 2, axis=1))
        alive = (self.age < self.lifetime) & (real_dist > EVENT_HORIZON_R)

        # also drop particles that somehow fly way off screen (cleanup)
        margin = 300
        on_screen = (
            (self.pos[:, 0] > -margin) & (self.pos[:, 0] < WIDTH + margin) &
            (self.pos[:, 1] > -margin) & (self.pos[:, 1] < HEIGHT + margin)
        )
        alive &= on_screen

        self.pos = self.pos[alive]
        self.prev_pos = self.prev_pos[alive]
        self.vel = self.vel[alive]
        self.age = self.age[alive]
        self.lifetime = self.lifetime[alive]
        self.hue = self.hue[alive]

    def draw(self, surface):
        if len(self.pos) == 0:
            return

        life_frac = 1.0 - (self.age / self.lifetime)  # 1 = fresh, 0 = about to die
        life_frac = np.clip(life_frac, 0, 1)

        # speed-based brightness boost (faster = whiter/hotter, like accretion glow)
        speed = np.sqrt(np.sum(self.vel ** 2, axis=1))
        speed_norm = np.clip(speed / 1200.0, 0, 1)

        for i in range(len(self.pos)):
            alpha = int(255 * life_frac[i])
            if alpha <= 0:
                continue
            hue = self.hue[i]
            heat = speed_norm[i]

            # base cool bluish color, shifting toward white/orange when fast
            r = int(120 + 135 * heat)
            g = int(140 + 80 * (1 - heat) * (0.5 + 0.5 * hue))
            b = int(255 - 60 * heat)
            color = (min(r, 255), min(g, 255), min(b, 255), alpha)

            px, py = self.pos[i]
            ppx, ppy = self.prev_pos[i]

            # stretch the streak length with speed -> fast = long thread,
            # slow = short dash. This is what gives the hairy/threaded look
            # around the black hole instead of plain dots.
            dx, dy = px - ppx, py - ppy
            seg_len = (dx * dx + dy * dy) ** 0.5
            stretch = min(4.0, 1.0 + heat * 3.0)
            end_x = px - dx * (stretch - 1.0)
            end_y = py - dy * (stretch - 1.0)

            width = 1 if heat < 0.6 else 2

            if seg_len < 0.5:
                # essentially stationary - draw a tiny dot instead of a line
                pygame.draw.circle(surface, color[:3], (int(px), int(py)), 1)
            else:
                line_surf_rect = pygame.Rect(
                    min(int(px), int(end_x)) - 2, min(int(py), int(end_y)) - 2,
                    abs(int(px) - int(end_x)) + 4, abs(int(py) - int(end_y)) + 4
                )
                line_surf = pygame.Surface(line_surf_rect.size, pygame.SRCALPHA)
                offset = (line_surf_rect.x, line_surf_rect.y)
                pygame.draw.line(
                    line_surf, color,
                    (px - offset[0], py - offset[1]),
                    (end_x - offset[0], end_y - offset[1]),
                    width
                )
                surface.blit(line_surf, offset)


def draw_black_hole(surface):
    # soft glowing accretion ring (a few translucent circles), then solid core
    for radius, alpha in [(40, 25), (30, 40), (22, 60)]:
        glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 170, 60, alpha), (radius, radius), radius)
        surface.blit(glow, (BLACK_HOLE_POS[0] - radius, BLACK_HOLE_POS[1] - radius))

    center = BLACK_HOLE_POS.astype(int)
    pygame.draw.circle(surface, (0, 0, 0), center, EVENT_HORIZON_R)
    pygame.draw.circle(surface, (255, 120, 40), center, EVENT_HORIZON_R, width=1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Black Hole Particle Simulator")
    clock = pygame.time.Clock()

    particles = ParticleSystem(MAX_PARTICLES)
    font = pygame.font.SysFont("consolas", 16)

    # persistent surface that we fade slightly each frame instead of clearing,
    # so particle streaks accumulate into long glowing trails/threads
    trail_surface = pygame.Surface((WIDTH, HEIGHT)).convert()
    trail_surface.fill((5, 5, 15))

    mouse_held = False
    spawn_timer = 0.0
    spawn_interval = 0.05  # seconds between bursts while holding click

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    particles.clear()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_held = True
                x, y = pygame.mouse.get_pos()
                particles.spawn(x, y, PARTICLES_PER_CLICK)
                spawn_timer = 0.0
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_held = False

        if mouse_held:
            spawn_timer += dt
            if spawn_timer >= spawn_interval:
                spawn_timer = 0.0
                x, y = pygame.mouse.get_pos()
                particles.spawn(x, y, PARTICLES_PER_CLICK // 4)

        particles.update(dt)

        # fade the trail surface slightly instead of clearing it -> old
        # particle streaks linger and slowly dim, building up into long
        # glowing threads rather than disappearing every frame
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((5, 5, 15))
        fade.set_alpha(TRAIL_FADE_ALPHA)
        trail_surface.blit(fade, (0, 0))

        particles.draw(trail_surface)

        screen.blit(trail_surface, (0, 0))
        draw_black_hole(screen)  # drawn fresh on top every frame so it stays crisp

        info = f"particles: {len(particles.pos)}   FPS: {int(clock.get_fps())}   (R = clear, click = spawn)"
        text_surf = font.render(info, True, (200, 200, 200))
        screen.blit(text_surf, (10, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
