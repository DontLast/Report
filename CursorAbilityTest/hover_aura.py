import sys
import math
import time
import random
import pygame

# === ПАРАМЕТРЫ ЭКРАНА ===
WIDTH, HEIGHT = 900, 600
FPS = 60

# === ЦВЕТА ===
BG_COLOR = (60, 60, 60)
CIRCLE_COLOR = (10, 10, 10)
PARTICLE_COLOR = (255, 255, 255)
TRIANGLE_COLOR = (120, 0, 0)
TEXT_COLOR = (255, 255, 255)

# === ЭФФЕКТ АУРЫ ===
BASE_RADIUS = 14
AURA_LAYERS = 10
AURA_SPACING = 3
PULSE_FREQ = 2.0
PULSE_DEPTH = 0.25

# === ПАРАМЕТРЫ ===
PARTICLE_SPEED = 200
TRIANGLE_MIN_SPEED = 80
TRIANGLE_MAX_SPEED = 250
MAX_TRIANGLES = 30
SPAWN_DELAY = 0.2  # интервал между спавном новых врагов

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aura Defense (Optimized)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)


# === КЛАССЫ ===

class Particle:
    def __init__(self, x, y, target, color=PARTICLE_COLOR, outwards=False):
        self.x = x
        self.y = y
        self.color = color
        self.outwards = outwards
        self.target = target
        self.speed = random.uniform(150, 250)
        self.radius = 4

        if outwards:
            dx = x - target[0]
            dy = y - target[1]
        else:
            dx = target[0] - x
            dy = target[1] - y

        dist = math.hypot(dx, dy) + 0.001
        self.vx = (dx / dist) * self.speed
        self.vy = (dy / dist) * self.speed

    def update(self, dt):
        # Пересчёт направления для самонаведения
        if not self.outwards:
            dx = self.target[0] - self.x
            dy = self.target[1] - self.y
            dist = math.hypot(dx, dy) + 0.0001
            self.vx = (dx / dist) * self.speed
            self.vy = (dy / dist) * self.speed
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def reached_target(self, target_radius):
        return math.hypot(self.x - self.target[0], self.y - self.target[1]) < target_radius


class Triangle:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.size = random.randint(16, 26)
        self.target = target
        self.speed = random.uniform(TRIANGLE_MIN_SPEED, TRIANGLE_MAX_SPEED)
        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(60, 180)
        self.hp = random.randint(1, 3)
        self.color = TRIANGLE_COLOR

    def update(self, dt):
        dx = self.target[0] - self.x
        dy = self.target[1] - self.y
        dist = math.hypot(dx, dy) + 0.0001
        self.x += (dx / dist) * self.speed * dt
        self.y += (dy / dist) * self.speed * dt
        self.angle = (self.angle + self.rotation_speed * dt) % 360

    def draw(self, surface):
        points = []
        for i in range(3):
            ang = math.radians(self.angle + i * 120)
            px = self.x + math.cos(ang) * self.size
            py = self.y + math.sin(ang) * self.size
            points.append((px, py))
        pygame.draw.polygon(surface, self.color, points)

    def reached_target(self, target_radius):
        return math.hypot(self.x - self.target[0], self.y - self.target[1]) < target_radius


# === ВСПОМОГАТЕЛЬНЫЕ ===

def draw_smooth_aura(surface, pos, t):
    mx, my = int(pos[0]), int(pos[1])
    pulse = 1.0 + PULSE_DEPTH * math.sin(2 * math.pi * PULSE_FREQ * t)
    aura_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    for layer in range(AURA_LAYERS, 0, -1):
        r = int(BASE_RADIUS + layer * AURA_SPACING * pulse * 0.5)
        dark_factor = (AURA_LAYERS - layer) / AURA_LAYERS
        alpha = int(255 * (0.3 + 0.7 * dark_factor))
        alpha = max(5, min(100, alpha))
        col = (0, 0, 0, alpha)
        pygame.draw.circle(aura_surface, col, (mx, my), r)

    surface.blit(aura_surface, (0, 0))


def random_edge_position():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        return random.randint(0, WIDTH), 0
    elif side == "bottom":
        return random.randint(0, WIDTH), HEIGHT
    elif side == "left":
        return 0, random.randint(0, HEIGHT)
    else:
        return WIDTH, random.randint(0, HEIGHT)


# === ОСНОВНАЯ ФУНКЦИЯ ===

def main():
    running = True
    particles = []
    triangles = []
    score = 0

    left_held = False
    right_held = False
    last_spawn_time = 0
    start_t = time.time()

    while running:
        dt = clock.tick(FPS) / 1000.0
        t = time.time() - start_t

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    left_held = True
                elif ev.button == 3:
                    right_held = True
            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    left_held = False
                elif ev.button == 3:
                    right_held = False

        mx, my = pygame.mouse.get_pos()
        target = (mx, my)

        # === Спавн врагов и частиц с задержкой ===
        if left_held and time.time() - last_spawn_time > SPAWN_DELAY:
            last_spawn_time = time.time()
            for _ in range(random.randint(5, 10)):
                x, y = random_edge_position()
                particles.append(Particle(x, y, target))
            if len(triangles) < MAX_TRIANGLES:
                for _ in range(random.randint(1, 2)):
                    x, y = random_edge_position()
                    triangles.append(Triangle(x, y, target))

        if right_held and score > 0:
            for _ in range(random.randint(1, 3)):
                if score > 0:
                    particles.append(Particle(mx, my, random_edge_position(), outwards=True))
                    score -= 1

        # === Обновление ===
        for p in particles[:]:
            p.target = target
            p.update(dt)
            if not p.outwards and p.reached_target(BASE_RADIUS):
                particles.remove(p)
                score += 1
            elif p.outwards and (p.x < 0 or p.x > WIDTH or p.y < 0 or p.y > HEIGHT):
                particles.remove(p)

        for tr in triangles[:]:
            tr.target = target
            tr.update(dt)

            for p in particles[:]:
                if p.outwards and math.hypot(tr.x - p.x, tr.y - p.y) < tr.size:
                    tr.hp -= 1
                    particles.remove(p)
                    if tr.hp <= 0:
                        if tr in triangles:
                            triangles.remove(tr)
                    break

            if tr.reached_target(BASE_RADIUS):
                if tr in triangles:
                    triangles.remove(tr)
                score = max(0, score - random.randint(10, 50))

        # === РЕНДЕР ===
        screen.fill(BG_COLOR)
        draw_smooth_aura(screen, target, t)
        pygame.draw.circle(screen, CIRCLE_COLOR, (int(mx), int(my)), BASE_RADIUS)

        for p in particles:
            p.draw(screen)
        for tr in triangles:
            tr.draw(screen)

        text = font.render(f"Particles: {score}", True, TEXT_COLOR)
        screen.blit(text, (5, 10))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
