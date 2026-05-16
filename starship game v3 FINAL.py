import pygame
import random
import sys
import json
import os
import math
from pygame import mixer
from pathlib import Path

# Initialize pygame
pygame.init()
mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 1400, 830
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Space Explorer")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
DARK_PURPLE = (75, 0, 130)
SPIKE_GOLD = (255, 215, 0)
BLOOD_RED = (139, 0, 0)
HEAL_GREEN = (50, 255, 50)
IRON_RED = (255, 50, 50)
BRIGHT_RED = (255, 0, 0)
DARK_GREEN = (0, 100, 40)
STEEL_BLUE = (70, 130, 180)
ROSE_GOLD = (183, 110, 121)
NEBULA_PURPLE = (102, 51, 153)
PHANTOM_GRAY = (80, 80, 100)
PORTAL_BLUE = (50, 100, 200)
PORTAL_PURPLE = (150, 50, 200)

# Fonts
try:
    font_large = pygame.font.SysFont('freesansbold', 70, bold=True)
    font_medium = pygame.font.SysFont('freesansbold', 45, bold=False)
    font_small = pygame.font.SysFont('freesansbold', 28, bold=False)
    font_tiny = pygame.font.SysFont('freesansbold', 22, bold=False)
except:
    font_large = pygame.font.SysFont('arial', 70)
    font_medium = pygame.font.SysFont('arial', 45)
    font_small = pygame.font.SysFont('arial', 28)
    font_tiny = pygame.font.SysFont('arial', 22)

# Load sounds
try:
    laser_sound = mixer.Sound('biu.wav')
    laser_sound.set_volume(0.15)
    explosion_sound = mixer.Sound('boom2.wav')
    explosion_sound.set_volume(0.2)
    powerup_sound = mixer.Sound('mariocoin.wav')
    death_sound = mixer.Sound('mariodie.wav')
    death_sound.set_volume(0.5)
except:
    print("Sound files missing - continuing without audio")

# ---- Storage files ----
BASE_DIR = Path(__file__).parent
SETTINGS_FILE = BASE_DIR / "starship_settings.json"
HIGHSCORE_FILE = BASE_DIR / "starship_highscore.json"

# ---- Skins for starship ----
SKINS = [
    {"name": "Classic Blue", "unlock": 0, "color": BLUE, "accent": WHITE, "laser_color": (0, 100, 255), "booster_color": (0, 150, 255)},
    {"name": "Red Phoenix", "unlock": 5, "color": RED, "accent": YELLOW, "laser_color": (255, 50, 50), "booster_color": (255, 80, 0)},
    {"name": "Golden Eagle", "unlock": 10, "color": (255, 215, 0), "accent": (255, 100, 0), "laser_color": (255, 200, 0), "booster_color": (255, 150, 0)},
    {"name": "Purple Nebula", "unlock": 15, "color": PURPLE, "accent": (200, 100, 255), "laser_color": (160, 50, 255), "booster_color": (180, 0, 255)},
    {"name": "Cyan Storm", "unlock": 20, "color": (0, 255, 255), "accent": WHITE, "laser_color": (0, 200, 200), "booster_color": (0, 100, 200)},
    {"name": "Lava Core", "unlock": 30, "color": (255, 60, 0), "accent": (255, 200, 0), "laser_color": (255, 80, 0), "booster_color": (255, 30, 0)},
    {"name": "Emerald", "unlock": 40, "color": DARK_GREEN, "accent": (0, 255, 100), "laser_color": (0, 200, 80), "booster_color": (0, 150, 50)},
    {"name": "Arctic Ice", "unlock": 50, "color": (200, 230, 255), "accent": WHITE, "laser_color": (150, 200, 255), "booster_color": (100, 150, 200)},
    {"name": "Dark Matter", "unlock": 60, "color": (50, 50, 80), "accent": (150, 150, 200), "laser_color": (100, 100, 150), "booster_color": (200, 50, 200)},
    {"name": "Solar Flare", "unlock": 75, "color": (255, 140, 0), "accent": (255, 255, 100), "laser_color": (255, 120, 0), "booster_color": (255, 200, 0)},
    {"name": "Cosmic Pink", "unlock": 90, "color": (255, 100, 200), "accent": (255, 200, 255), "laser_color": (255, 80, 180), "booster_color": (255, 50, 150)},
    {"name": "Platinum", "unlock": 110, "color": (192, 192, 192), "accent": WHITE, "laser_color": (180, 180, 180), "booster_color": (100, 100, 100)},
    {"name": "Steel Phantom", "unlock": 125, "color": STEEL_BLUE, "accent": (150, 150, 150), "laser_color": (100, 150, 200), "booster_color": (50, 100, 150)},
    {"name": "Rose Gold", "unlock": 140, "color": ROSE_GOLD, "accent": GOLD, "laser_color": (200, 100, 120), "booster_color": (150, 80, 90)},
    {"name": "Nebula Core", "unlock": 160, "color": NEBULA_PURPLE, "accent": MAGENTA, "laser_color": (150, 50, 200), "booster_color": (200, 50, 150)},
    {"name": "Phantom", "unlock": 180, "color": PHANTOM_GRAY, "accent": CYAN, "laser_color": (100, 150, 200), "booster_color": (60, 80, 100)},
    {"name": "Midnight Sun", "unlock": 200, "color": (30, 30, 40), "accent": ORANGE, "laser_color": (255, 100, 0), "booster_color": (200, 80, 0)},
]

# ---- High score functions ----
def load_highscore():
    try:
        if HIGHSCORE_FILE.exists():
            data = json.loads(HIGHSCORE_FILE.read_text(encoding="utf-8"))
            return data.get("highscore", 0)
    except:
        pass
    return 0

def save_highscore(score):
    try:
        current_high = load_highscore()
        if score > current_high:
            HIGHSCORE_FILE.write_text(json.dumps({"highscore": score}, indent=2), encoding="utf-8")
            return True
    except:
        pass
    return False

# ---- Default settings ----
DEFAULT_SETTINGS = {"skin": "Classic Blue"}

def load_settings():
    try:
        if SETTINGS_FILE.exists():
            return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except:
        pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    try:
        SETTINGS_FILE.write_text(json.dumps(settings, indent=2), encoding="utf-8")
    except:
        pass

# Load saved skin and high score
settings = load_settings()
saved_skin_name = settings.get("skin", "Classic Blue")
high_score = load_highscore()

# Find the saved skin or default to first
selected_skin = next((s for s in SKINS if s["name"] == saved_skin_name), SKINS[0])
current_skin_index = SKINS.index(selected_skin)

# ========== MUSIC MANAGEMENT ==========
def play_menu_music():
    try:
        mixer.music.stop()
        mixer.music.load('plantzombie.mp3')
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)
    except Exception as e:
        print(f"Could not play menu music: {e}")

def play_game_music():
    try:
        mixer.music.stop()
        mixer.music.load('missionimpossible.mp3')
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)
    except Exception as e:
        print(f"Could not play game music: {e}")

def play_godmode_music():
    try:
        mixer.music.stop()
        mixer.music.load('music.mp3')
        mixer.music.set_volume(0.7)
        mixer.music.play(-1)
    except Exception as e:
        print(f"Could not play godmode music: {e}")

def stop_music():
    try:
        mixer.music.stop()
    except:
        pass

# Start with menu music
play_menu_music()

# ========== HELPER FUNCTIONS ==========
def draw_text(text, font, color, x, y, center=True):
    text_surface = font.render(text, True, color)
    if center:
        screen.blit(text_surface, (x - text_surface.get_width()//2, y - text_surface.get_height()//2))
    else:
        screen.blit(text_surface, (x, y))

def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    button_rect = pygame.Rect(x - width//2, y - height//2, width, height)
    is_hover = button_rect.collidepoint(mouse)
    
    if is_hover:
        pygame.draw.rect(screen, active_color, button_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_rect, 3, border_radius=10)
        draw_text(text, font_medium, BLACK, x, y)
        if click[0] == 1:
            return action
    else:
        pygame.draw.rect(screen, inactive_color, button_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_rect, 3, border_radius=10)
        draw_text(text, font_medium, BLACK, x, y)
    
    return None

def draw_starfield():
    for _ in range(12):
        pygame.draw.circle(screen, WHITE, 
                         (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 
                         random.randint(1, 2))

def get_rainbow_color(frame):
    colors = [
        (255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0),
        (0, 255, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255)
    ]
    return colors[frame % len(colors)]

def draw_high_tech_border():
    """Thicker HUD-style border with HALO feel"""
    for i in range(1, 6):
        alpha = max(0, 60 - i * 10)
        glow_rect = pygame.Rect(i-1, i-1, WIDTH - (i-1)*2, HEIGHT - (i-1)*2)
        pygame.draw.rect(screen, (0, 150, 255, alpha), glow_rect, 2)
    
    pygame.draw.rect(screen, CYAN, (3, 3, WIDTH - 6, HEIGHT - 6), 4)
    pygame.draw.rect(screen, (100, 200, 255, 100), (8, 8, WIDTH - 16, HEIGHT - 16), 2)
    
    corner_size = 25
    bracket_thick = 4
    corners = [(4, 4), (WIDTH - 4, 4), (4, HEIGHT - 4), (WIDTH - 4, HEIGHT - 4)]
    for x, y in corners:
        if x == 4:
            pygame.draw.line(screen, CYAN, (x, y), (x + corner_size, y), bracket_thick)
            pygame.draw.line(screen, CYAN, (x, y), (x, y + corner_size), bracket_thick)
            pygame.draw.line(screen, (0, 200, 255), (x + 3, y + 3), (x + corner_size - 3, y + 3), 2)
            pygame.draw.line(screen, (0, 200, 255), (x + 3, y + 3), (x + 3, y + corner_size - 3), 2)
        else:
            pygame.draw.line(screen, CYAN, (x - corner_size, y), (x, y), bracket_thick)
            pygame.draw.line(screen, CYAN, (x, y), (x, y + corner_size), bracket_thick)
            pygame.draw.line(screen, (0, 200, 255), (x - corner_size + 3, y + 3), (x - 3, y + 3), 2)
            pygame.draw.line(screen, (0, 200, 255), (x - 3, y + 3), (x - 3, y + corner_size - 3), 2)

# ========== PHIGROS PORTAL CLASS ==========
class PhigrosPortal:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 50, y - 50, 100, 100)
        self.x = x
        self.y = y
        self.angle = 0
        self.active = True
        self.pulse = 0
        self.pulse_direction = 1
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 15000
    
    def update(self):
        self.angle += 8
        self.pulse += self.pulse_direction * 3
        if self.pulse > 30:
            self.pulse_direction = -1
        elif self.pulse < 0:
            self.pulse_direction = 1
        
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            return False
        return self.active
    
    def draw(self, screen):
        # Outer glow
        for i in range(5):
            radius = 50 + i * 2 + self.pulse // 3
            alpha = max(0, 70 - i * 12)
            pygame.draw.circle(screen, (PORTAL_BLUE[0], PORTAL_BLUE[1], PORTAL_BLUE[2]), 
                             (int(self.x), int(self.y)), radius, 3)
        
        # Main rings
        for ring in range(3):
            radius = 42 - ring * 4
            pygame.draw.circle(screen, PORTAL_BLUE, (int(self.x), int(self.y)), radius, 3)
            pygame.draw.circle(screen, PORTAL_PURPLE, (int(self.x), int(self.y)), radius - 4, 2)
        
        # Rotating outer orbs
        for i in range(8):
            rad = math.radians(self.angle + i * 45)
            px = self.x + math.cos(rad) * 48
            py = self.y + math.sin(rad) * 48
            pygame.draw.circle(screen, CYAN, (int(px), int(py)), 4)
            pygame.draw.circle(screen, WHITE, (int(px), int(py)), 2)
        
        # Rotating inner orbs
        for i in range(6):
            rad = math.radians(-self.angle * 1.5 + i * 60)
            px = self.x + math.cos(rad) * 28
            py = self.y + math.sin(rad) * 28
            pygame.draw.circle(screen, MAGENTA, (int(px), int(py)), 3)
        
        # Bright core
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 20)
        pygame.draw.circle(screen, (200, 200, 255), (int(self.x), int(self.y)), 12)
        pygame.draw.circle(screen, PORTAL_BLUE, (int(self.x), int(self.y)), 6)
        
        # Core pulse
        core_glow = 12 + self.pulse // 3
        pygame.draw.circle(screen, (255, 255, 200), (int(self.x), int(self.y)), core_glow, 2)
        
        # Text
        draw_text("PORTAL", font_small, GOLD, self.x, self.y - 50)
        draw_text("PRESS SPACE", font_tiny, CYAN, self.x, self.y + 58)
        
        # Timer bar
        time_left = max(0, (self.lifetime - (pygame.time.get_ticks() - self.spawn_time)) // 1000)
        bar_width = 70
        bar_height = 5
        progress_width = bar_width * (time_left / 15)
        pygame.draw.rect(screen, (50, 50, 80), (self.x - bar_width//2, self.y + 72, bar_width, bar_height))
        pygame.draw.rect(screen, CYAN, (self.x - bar_width//2, self.y + 72, progress_width, bar_height))
    
    def draw_minimap_indicator(self, screen):
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        dx = self.x - center_x
        dy = self.y - center_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            dx /= distance
            dy /= distance
        
        margin = 60
        indicator_x = center_x + dx * (WIDTH//2 - margin)
        indicator_y = center_y + dy * (HEIGHT//2 - margin)
        
        indicator_x = max(margin, min(WIDTH - margin, indicator_x))
        indicator_y = max(margin, min(HEIGHT - margin, indicator_y))
        
        arrow_size = 12 + self.pulse // 6
        points = [
            (indicator_x, indicator_y - arrow_size),
            (indicator_x - arrow_size//2, indicator_y + arrow_size//2),
            (indicator_x - arrow_size//4, indicator_y + arrow_size//4),
            (indicator_x - arrow_size//4, indicator_y + arrow_size),
            (indicator_x, indicator_y + arrow_size - 3),
            (indicator_x + arrow_size//4, indicator_y + arrow_size),
            (indicator_x + arrow_size//4, indicator_y + arrow_size//4),
            (indicator_x + arrow_size//2, indicator_y + arrow_size//2),
        ]
        pygame.draw.polygon(screen, MAGENTA, points)
        pygame.draw.polygon(screen, CYAN, points, 2)

class PhigrosNote:
    def __init__(self, x, target_y, lane):
        self.x = x
        self.y = -40
        self.target_y = target_y
        self.speed = 6.5
        self.hit = False
        self.missed = False
        self.lane = lane
        self.size = 14
        self.glow = 0
        self.glow_dir = 1
    
    def update(self):
        self.y += self.speed
        self.glow += self.glow_dir * 0.5
        if self.glow > 6:
            self.glow_dir = -1
        elif self.glow < 0:
            self.glow_dir = 1
        return self.y > HEIGHT + 60
    
    def draw(self, screen):
        if not self.hit and not self.missed:
            for i in range(3):
                alpha = 100 - i * 25
                pygame.draw.circle(screen, (255, 200, 0), (int(self.x), int(self.y)), self.size + i*2 + int(self.glow))
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.size)
            pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.size - 3)
            pygame.draw.line(screen, WHITE, (self.x - 6, self.y), (self.x + 6, self.y), 3)
            pygame.draw.line(screen, WHITE, (self.x, self.y - 6), (self.x, self.y + 6), 3)

def phigros_minigame(player, portal):
    clock = pygame.time.Clock()
    notes = []
    score_gain = 0
    health_loss = 0
    beat_interval = 40
    next_beat = beat_interval
    judgement_line_y = HEIGHT // 2 + 100
    note_positions = [WIDTH//4, WIDTH//2, 3*WIDTH//4]
    combo = 0
    max_combo = 0
    perfect_count = 0
    good_count = 0
    miss_count = 0
    
    original_pos = player.rect.center
    player.rect.center = (WIDTH//2, HEIGHT//2)
    
    start_time = pygame.time.get_ticks()
    duration = 30000
    
    # Pause game music
    mixer.music.pause()
    
    while (pygame.time.get_ticks() - start_time) < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    hit = False
                    for note in notes[:]:
                        if not note.hit and not note.missed:
                            distance = abs(note.y - judgement_line_y)
                            if distance < 45:
                                note.hit = True
                                if distance < 15:
                                    score_gain += 100
                                    combo += 1
                                    perfect_count += 1
                                elif distance < 30:
                                    score_gain += 60
                                    combo += 1
                                    good_count += 1
                                else:
                                    score_gain += 30
                                    combo += 1
                                if combo > max_combo:
                                    max_combo = combo
                                try:
                                    powerup_sound.play()
                                except:
                                    pass
                                notes.remove(note)
                                hit = True
                                break
                    if not hit:
                        combo = 0
        
        next_beat -= 1
        if next_beat <= 0:
            lane = random.randint(0, 2)
            pos_x = note_positions[lane]
            notes.append(PhigrosNote(pos_x, judgement_line_y, lane))
            next_beat = beat_interval
            beat_interval = max(20, beat_interval - 0.5)
        
        for note in notes[:]:
            if note.update():
                if not note.hit and not note.missed:
                    note.missed = True
                    health_loss += 5
                    miss_count += 1
                    combo = 0
                notes.remove(note)
        
        # Draw rhythm game
        screen.fill((5, 5, 20))
        
        for i in range(3):
            alpha = 100 - i * 30
            pygame.draw.line(screen, (0, 255, 255), 
                           (0, judgement_line_y + i*2), (WIDTH, judgement_line_y + i*2), 3)
        pygame.draw.line(screen, CYAN, (0, judgement_line_y), (WIDTH, judgement_line_y), 4)
        pygame.draw.line(screen, WHITE, (0, judgement_line_y - 3), (WIDTH, judgement_line_y - 3), 2)
        pygame.draw.line(screen, WHITE, (0, judgement_line_y + 3), (WIDTH, judgement_line_y + 3), 2)
        
        for i, x in enumerate(note_positions):
            pygame.draw.line(screen, (50, 50, 100), (x, 0), (x, HEIGHT), 3)
        
        for note in notes:
            note.draw(screen)
        
        draw_text("PHIGROS PORTAL", font_medium, GOLD, WIDTH//2, 50)
        draw_text("Press SPACE or UP when notes hit the line", font_small, WHITE, WIDTH//2, 100)
        
        stats_y = 150
        draw_text(f"Score: +{score_gain}", font_small, GREEN, WIDTH//2 - 200, stats_y, False)
        draw_text(f"Combo: x{combo}", font_small, YELLOW, WIDTH//2, stats_y, False)
        draw_text(f"Max Combo: x{max_combo}", font_small, ORANGE, WIDTH//2 + 200, stats_y, False)
        
        draw_text(f"Perfect: {perfect_count}", font_small, GREEN, WIDTH//2 - 200, stats_y + 35, False)
        draw_text(f"Good: {good_count}", font_small, YELLOW, WIDTH//2, stats_y + 35, False)
        draw_text(f"Miss: {miss_count}", font_small, RED, WIDTH//2 + 200, stats_y + 35, False)
        draw_text(f"Miss Penalty: -{health_loss} HP", font_small, BLOOD_RED, WIDTH//2, stats_y + 70)
        
        time_left = max(0, (duration - (pygame.time.get_ticks() - start_time)) // 1000)
        draw_text(f"Time left: {time_left}s", font_small, MAGENTA, WIDTH//2, stats_y + 110)
        
        player.draw(screen)
        draw_high_tech_border()
        
        pygame.display.flip()
        clock.tick(60)
    
    # Resume game music
    mixer.music.unpause()
    
    player.score += score_gain
    player.health -= health_loss
    player.rect.center = original_pos
    return score_gain, health_loss

# ========== LASER CLASSES ==========
class AutoAimLaser:
    def __init__(self, x, y, target_enemy, target_boss, skin_color):
        self.x = x
        self.y = y
        self.target_enemy = target_enemy
        self.target_boss = target_boss
        self.speed = 18
        self.color = IRON_RED
        self.alive = True
        self.rect = pygame.Rect(x - 3, y - 3, 6, 6)
        self.trail = [(x, y)]
        self.trail_length = 5
        self.life_frames = 0
    
    def get_target_position(self):
        if self.target_enemy is not None:
            try:
                if hasattr(self.target_enemy, 'rect') and self.target_enemy.rect is not None:
                    return (self.target_enemy.rect.centerx, self.target_enemy.rect.centery)
            except:
                pass
        
        if self.target_boss is not None:
            try:
                if hasattr(self.target_boss, 'rect') and self.target_boss.rect is not None:
                    return (self.target_boss.rect.centerx, self.target_boss.rect.centery)
            except:
                pass
        return None
    
    def update(self):
        self.life_frames += 1
        if self.life_frames > 90:
            return True
        
        target_pos = self.get_target_position()
        if target_pos is None:
            return True
        
        dx = target_pos[0] - self.x
        dy = target_pos[1] - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
        
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)
        
        self.rect.x = int(self.x - 3)
        self.rect.y = int(self.y - 3)
        
        return (self.rect.bottom < 0 or self.rect.top > HEIGHT or 
                self.rect.right < 0 or self.rect.left > WIDTH)
    
    def draw(self, screen):
        for i, pos in enumerate(self.trail):
            trail_color = (min(255, self.color[0] + 50), self.color[1], self.color[2])
            pygame.draw.circle(screen, trail_color, (int(pos[0]), int(pos[1])), 2)
        
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 4)
        if self.target_enemy:
            dx = self.target_enemy.rect.centerx - self.x
            dy = self.target_enemy.rect.centery - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                tip_x = self.x + (dx / dist) * 6
                tip_y = self.y + (dy / dist) * 6
                pygame.draw.circle(screen, BRIGHT_RED, (int(tip_x), int(tip_y)), 2)

class Laser:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x - 3, y, 6, 20)
        self.speed = 12
        self.color = color
        self.trail = [(x, y)]
        self.life_frames = 0
    
    def update(self):
        self.life_frames += 1
        old_y = self.rect.y
        self.rect.y -= self.speed
        self.trail.append((self.rect.centerx, old_y))
        if len(self.trail) > 3:
            self.trail.pop(0)
        if self.life_frames > 100:
            return True
        return self.rect.bottom < 0
    
    def draw(self, screen):
        for i, pos in enumerate(self.trail):
            trail_color = (min(255, self.color[0] + 50), self.color[1], self.color[2])
            pygame.draw.circle(screen, trail_color, (int(pos[0]), int(pos[1])), 2)
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BRIGHT_RED, (self.rect.x, self.rect.y - 2, self.rect.width, 3))

class GodModeLaser:
    def __init__(self, x, y, angle, frame):
        self.rect = pygame.Rect(x - 2, y - 10, 4, 15)
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 16
        self.frame = frame
        self.color = get_rainbow_color(frame + angle)
        rad = math.radians(angle)
        self.vx = math.sin(rad) * self.speed
        self.vy = -math.cos(rad) * self.speed
        self.trail = [(x, y)]
        self.life_frames = 0
    
    def update(self):
        self.life_frames += 1
        old_x, old_y = self.x, self.y
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x - 2)
        self.rect.y = int(self.y - 10)
        self.color = get_rainbow_color(self.frame)
        self.frame += 1
        self.trail.append((old_x, old_y))
        if len(self.trail) > 3:
            self.trail.pop(0)
        if self.life_frames > 120:
            return True
        return (self.rect.bottom < 0 or self.rect.top > HEIGHT or 
                self.rect.right < 0 or self.rect.left > WIDTH)
    
    def draw(self, screen):
        for i, pos in enumerate(self.trail):
            trail_color = get_rainbow_color(self.frame - i)
            pygame.draw.circle(screen, trail_color, (int(pos[0]), int(pos[1])), 2)
        pygame.draw.rect(screen, self.color, self.rect)

# ========== ENEMY CLASSES ==========
class BossEnemy:
    def __init__(self):
        self.img = pygame.Surface((70, 70), pygame.SRCALPHA)
        pygame.draw.polygon(self.img, DARK_PURPLE, [(35, 0), (0, 70), (70, 70)])
        for i in range(3):
            spike_x = 10 + i * 25
            pygame.draw.polygon(self.img, SPIKE_GOLD, [(spike_x, 20), (spike_x - 5, 35), (spike_x + 5, 35)])
        pygame.draw.circle(self.img, BLOOD_RED, (35, 45), 12)
        pygame.draw.circle(self.img, BLOOD_RED, (20, 30), 8)
        pygame.draw.circle(self.img, BLOOD_RED, (50, 30), 8)
        pygame.draw.circle(self.img, RED, (25, 25), 5)
        pygame.draw.circle(self.img, RED, (45, 25), 5)
        pygame.draw.circle(self.img, WHITE, (25, 25), 2)
        pygame.draw.circle(self.img, WHITE, (45, 25), 2)
        
        x = random.randint(70, WIDTH - 70)
        self.rect = self.img.get_rect(center=(x, -70))
        self.speed = random.uniform(0.8, 1.5)
        self.health = 9
        self.max_health = 9
        self.shoot_cooldown = 0
        self.lasers = []
        self.score_value = 500
    
    def update(self, player_pos):
        self.rect.y += self.speed
        
        if self.shoot_cooldown <= 0:
            self.shoot(player_pos)
            self.shoot_cooldown = 45
        else:
            self.shoot_cooldown -= 1
        
        for laser in self.lasers[:]:
            if laser.update():
                self.lasers.remove(laser)
        
        return self.rect.top > HEIGHT
    
    def shoot(self, player_pos):
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 0:
            dx /= distance
            dy /= distance
        self.lasers.append(BossLaser(self.rect.centerx, self.rect.centery, dx, dy))
    
    def draw(self, screen):
        screen.blit(self.img, self.rect)
        bar_width = 70
        bar_height = 8
        health_width = bar_width * (self.health / self.max_health)
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 12, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 12, health_width, bar_height))
        for laser in self.lasers:
            laser.draw(screen)

class BossLaser:
    def __init__(self, x, y, dx, dy):
        self.rect = pygame.Rect(x - 4, y - 4, 8, 8)
        self.x = x
        self.y = y
        self.dx = dx * 10
        self.dy = dy * 10
        self.color = BLOOD_RED
    
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.x = int(self.x - 4)
        self.rect.y = int(self.y - 4)
        return (self.rect.bottom < 0 or self.rect.top > HEIGHT or 
                self.rect.right < 0 or self.rect.left > WIDTH)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, GOLD, self.rect, 2)

class Enemy:
    def __init__(self, x=None):
        self.img = pygame.Surface((40, 40))
        self.img.fill(RED)
        pygame.draw.polygon(self.img, WHITE, [(20, 40), (5, 5), (35, 5)])
        pygame.draw.circle(self.img, YELLOW, (20, 35), 3)
        if x is None:
            x = random.randint(40, WIDTH - 40)
        self.rect = self.img.get_rect(center=(x, -40))
        self.speed = random.uniform(1.0, 3.0)
        self.health = 30
        self.shoot_cooldown = random.randint(30, 100)
        self.lasers = []
    
    def update(self):
        self.rect.y += self.speed
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        elif random.random() < 0.02:
            self.shoot()
            self.shoot_cooldown = random.randint(60, 150)
        for laser in self.lasers[:]:
            if laser.update():
                self.lasers.remove(laser)
        return self.rect.top > HEIGHT
    
    def shoot(self):
        self.lasers.append(EnemyLaser(self.rect.centerx, self.rect.bottom))
    
    def draw(self, screen):
        screen.blit(self.img, self.rect)
        for laser in self.lasers:
            laser.draw(screen)

class EnemyLaser(Laser):
    def __init__(self, x, y):
        super().__init__(x, y, RED)
        self.rect.y = y
        self.speed = -8
        self.color = RED

class Asteroid:
    def __init__(self):
        size = random.randint(25, 75)
        self.img = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.img, (150, 150, 150), (size//2, size//2), size//2)
        crater_size = size // 5
        pygame.draw.circle(self.img, (100, 100, 100), (size//3, size//3), crater_size)
        pygame.draw.circle(self.img, (100, 100, 100), (2*size//3, 2*size//3), crater_size)
        x = random.randint(size, WIDTH - size)
        self.rect = self.img.get_rect(center=(x, -size))
        self.speed = random.uniform(1.0, 4.0)
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)
        self.health = size
    
    def update(self):
        self.rect.y += self.speed
        self.rotation += self.rotation_speed
        return self.rect.top > HEIGHT
    
    def draw(self, screen):
        rotated_img = pygame.transform.rotate(self.img, self.rotation)
        new_rect = rotated_img.get_rect(center=self.rect.center)
        screen.blit(rotated_img, new_rect)
        
class HealthRegion:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH - 140, HEIGHT - 140, 120, 120)
        self.heal_cooldown = 0
    
    def update(self, player):
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1
        if self.rect.colliderect(player.rect) and self.heal_cooldown == 0:
            if player.health < player.max_health:
                player.health = min(player.max_health, player.health + 5)
                self.heal_cooldown = 60
    
    def draw(self, screen):
        s = pygame.Surface((120, 120), pygame.SRCALPHA)
        s.fill((0, 255, 0, 80))
        screen.blit(s, (WIDTH - 140, HEIGHT - 140))
        pygame.draw.rect(screen, GREEN, self.rect, 3)
        draw_text("HEAL ZONE", font_small, WHITE, WIDTH - 80, HEIGHT - 80)

class PowerUp:
    def __init__(self, x=None, y=None):
        powerup_types = ["rapid_fire", "shield", "triple_shot", "heal"]
        self.type = random.choice(powerup_types)
        
        colors = {
            "rapid_fire": YELLOW, "shield": BLUE, "triple_shot": PURPLE,
            "godmode": GOLD, "heal": HEAL_GREEN
        }
        self.img = pygame.Surface((30, 30))
        self.img.fill(colors[self.type])
        
        if self.type == "godmode":
            pygame.draw.circle(self.img, WHITE, (15, 15), 10, 2)
            pygame.draw.line(self.img, WHITE, (5, 15), (25, 15), 2)
            pygame.draw.line(self.img, WHITE, (15, 5), (15, 25), 2)
        elif self.type == "heal":
            pygame.draw.line(self.img, WHITE, (15, 5), (15, 25), 3)
            pygame.draw.line(self.img, WHITE, (5, 15), (25, 15), 3)
        elif self.type == "rapid_fire":
            pygame.draw.polygon(self.img, WHITE, [(15, 5), (8, 20), (22, 20)])
        
        if x is None:
            x = random.randint(25, WIDTH - 25)
        if y is None:
            y = random.randint(25, HEIGHT - 25)
        self.rect = self.img.get_rect(center=(x, y))
        self.speed = random.uniform(0.5, 1.5)
        self.lifetime = 300
    
    def update(self):
        self.rect.y += self.speed
        self.lifetime -= 1
        return self.rect.top > HEIGHT or self.lifetime <= 0
    
    def draw(self, screen):
        screen.blit(self.img, self.rect)

class Explosion:
    def __init__(self, x, y, size=1.0):
        self.particles = []
        for _ in range(25):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 6)
            self.particles.append({
                'x': x, 'y': y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'size': random.randint(2, 5) * size,
                'life': random.randint(15, 35),
                'color': random.choice([RED, ORANGE, YELLOW])
            })
    
    def update(self):
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
        return len(self.particles) == 0
    
    def draw(self, screen):
        for particle in self.particles:
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), int(particle['size']))

# ========== PLAYER CLASS ==========
class Player:
    def __init__(self):
        global selected_skin
        self.skin = selected_skin
        self.img = pygame.Surface((50, 40), pygame.SRCALPHA)
        self.update_skin()
        self.rect = self.img.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.speed = 7
        self.health = 100
        self.max_health = 100
        self.lasers = []
        self.laser_cooldown = 0
        self.score = 0
        self.frame_counter = 0
        self.powerups = {
            "rapid_fire": False,
            "shield": False,
            "triple_shot": False,
            "godmode": False
        }
        self.powerup_timers = {
            "rapid_fire": 0,
            "shield": 0,
            "triple_shot": 0,
            "godmode": 0
        }
        
        self.godmode_music_playing = False
        self.magazine_size = 200
        self.current_ammo = 200
        self.is_reloading = False
        self.reload_timer = 0
        self.reload_time = 60
        self.booster_particles = []
        self.iron_spider_halo_angle = 0
    
    def update_skin(self):
        self.img = pygame.Surface((50, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.img, self.skin["color"], [(25, 0), (0, 40), (50, 40)])
        pygame.draw.polygon(self.img, self.skin["accent"], [(5, 20), (0, 40), (15, 35)])
        pygame.draw.polygon(self.img, self.skin["accent"], [(45, 20), (50, 40), (35, 35)])
        pygame.draw.circle(self.img, CYAN, (25, 15), 5)
        pygame.draw.circle(self.img, WHITE, (25, 15), 2)
    
    def update(self, keys):
        self.frame_counter += 1
        self.iron_spider_halo_angle += 5
        
        prev_pos = (self.rect.centerx, self.rect.centery)
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.add_booster_particle(prev_pos, 'left')
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.add_booster_particle(prev_pos, 'right')
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.add_booster_particle(prev_pos, 'up')
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            self.add_booster_particle(prev_pos, 'down')
        
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))
        
        for particle in self.booster_particles[:]:
            particle['life'] -= 1
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            if particle['life'] <= 0:
                self.booster_particles.remove(particle)
        
        for powerup in self.powerup_timers:
            if self.powerup_timers[powerup] > 0:
                self.powerup_timers[powerup] -= 1
                if self.powerup_timers[powerup] == 0:
                    self.powerups[powerup] = False
                    
                    # Stop godmode music when godmode ends
                    if powerup == "godmode" and not self.powerups["godmode"]:
                        try:
                            play_game_music()
                        except:
                            pass
        
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1
        
        self.update_reload()
    
    def add_booster_particle(self, prev_pos, direction):
        if prev_pos[0] == self.rect.centerx and prev_pos[1] == self.rect.centery:
            return
        
        if direction == 'left':
            particle_x = self.rect.right + 5
            particle_y = self.rect.centery + random.randint(-10, 10)
            dx = random.uniform(-2, 2)
            dy = random.uniform(-1, 1)
        elif direction == 'right':
            particle_x = self.rect.left - 5
            particle_y = self.rect.centery + random.randint(-10, 10)
            dx = random.uniform(-2, 2)
            dy = random.uniform(-1, 1)
        elif direction == 'up':
            particle_x = self.rect.centerx + random.randint(-10, 10)
            particle_y = self.rect.bottom + 5
            dx = random.uniform(-1, 1)
            dy = random.uniform(1, 3)
        elif direction == 'down':
            particle_x = self.rect.centerx + random.randint(-10, 10)
            particle_y = self.rect.top - 5
            dx = random.uniform(-1, 1)
            dy = random.uniform(-3, -1)
        else:
            return
        
        self.booster_particles.append({
            'x': particle_x, 'y': particle_y, 'dx': dx, 'dy': dy,
            'life': random.randint(5, 15), 'size': random.randint(2, 4)
        })
    
    def find_nearest_enemies(self, enemies, bosses, count=3):
        all_targets = []
        for enemy in enemies:
            dist = math.sqrt((enemy.rect.centerx - self.rect.centerx)**2 + 
                           (enemy.rect.centery - self.rect.centery)**2)
            all_targets.append((dist, enemy, None))
        for boss in bosses:
            dist = math.sqrt((boss.rect.centerx - self.rect.centerx)**2 + 
                           (boss.rect.centery - self.rect.centery)**2)
            all_targets.append((dist, None, boss))
        all_targets.sort(key=lambda x: x[0])
        return all_targets[:count]
    
    def shoot(self):
        if self.is_reloading and not self.powerups["godmode"]:
            return
        
        if self.powerups["godmode"]:
            if self.laser_cooldown == 0:
                try:
                    laser_sound.play()
                except:
                    pass
                for angle in range(0, 360, 15):
                    self.lasers.append(GodModeLaser(self.rect.centerx, self.rect.centery, angle, self.frame_counter))
                self.laser_cooldown = 1
            return
        
        if self.powerups["rapid_fire"]:
            return  # Handled by shoot_auto_aim_with_targets
        
        if self.current_ammo <= 0:
            self.start_reload()
            return
        
        if self.laser_cooldown == 0:
            try:
                laser_sound.play()
            except:
                pass
            
            if self.powerups["triple_shot"]:
                self.lasers.append(Laser(self.rect.centerx - 20, self.rect.top, self.skin["laser_color"]))
                self.lasers.append(Laser(self.rect.centerx, self.rect.top, self.skin["laser_color"]))
                self.lasers.append(Laser(self.rect.centerx + 20, self.rect.top, self.skin["laser_color"]))
                self.current_ammo -= 3
            else:
                self.lasers.append(Laser(self.rect.centerx, self.rect.top, self.skin["laser_color"]))
                self.current_ammo -= 1
            
            self.laser_cooldown = 0
            
            if self.current_ammo <= 0:
                self.start_reload()
    
    def shoot_auto_aim_with_targets(self, enemies, bosses):
        if self.is_reloading:
            return
        
        if self.current_ammo <= 0:
            self.start_reload()
            return
        
        if self.laser_cooldown == 0:
            try:
                laser_sound.play()
            except:
                pass
            
            targets = self.find_nearest_enemies(enemies, bosses, 3)
            lasers_created = 0
            for dist, enemy, boss in targets:
                if enemy or boss:
                    self.lasers.append(AutoAimLaser(self.rect.centerx, self.rect.top, enemy, boss, self.skin["color"]))
                    lasers_created += 1
            
            if lasers_created == 0:
                self.lasers.append(Laser(self.rect.centerx - 15, self.rect.top, IRON_RED))
                self.lasers.append(Laser(self.rect.centerx, self.rect.top, IRON_RED))
                self.lasers.append(Laser(self.rect.centerx + 15, self.rect.top, IRON_RED))
            
            self.current_ammo -= 1
            self.laser_cooldown = 0
            
            if self.current_ammo <= 0:
                self.start_reload()
    
    def start_reload(self):
        if not self.is_reloading and self.current_ammo < self.magazine_size:
            self.is_reloading = True
            self.reload_timer = self.reload_time

    def update_reload(self):
        if self.is_reloading:
            self.reload_timer -= 1
            if self.reload_timer <= 0:
                self.current_ammo = self.magazine_size
                self.is_reloading = False
    
    def draw(self, screen):
        for particle in self.booster_particles:
            color = (self.skin["booster_color"][0], self.skin["booster_color"][1], self.skin["booster_color"][2])
            pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), particle['size'])
        
        screen.blit(self.img, self.rect)
        
        if self.powerups["rapid_fire"]:
            for ring in range(3):
                ring_radius = 28 + ring * 6 + (self.frame_counter % 20) / 4
                ring_surf = pygame.Surface((ring_radius * 2 + 10, ring_radius * 2 + 10), pygame.SRCALPHA)
                pygame.draw.circle(ring_surf, (255, 50, 50, 80 - ring * 20), 
                                 (ring_radius + 5, ring_radius + 5), int(ring_radius), 2)
                screen.blit(ring_surf, (self.rect.centerx - ring_radius - 5, self.rect.centery - ring_radius - 5))
            
            for i in range(4):
                angle_rad = math.radians(self.iron_spider_halo_angle + i * 90)
                blade_end_x = self.rect.centerx + math.cos(angle_rad) * 35
                blade_end_y = self.rect.centery + math.sin(angle_rad) * 35
                pygame.draw.line(screen, (255, 50, 50), self.rect.center, (blade_end_x, blade_end_y), 4)
                pygame.draw.line(screen, (255, 150, 50), self.rect.center, (blade_end_x, blade_end_y), 2)
            
            pygame.draw.circle(screen, BRIGHT_RED, (self.rect.centerx, self.rect.top - 3), 8)
            pygame.draw.circle(screen, (255, 100, 100), (self.rect.centerx, self.rect.top - 3), 4)
        
        if self.powerups["godmode"]:
            for i in range(4):
                glow_rect = pygame.Rect(0, 0, 85 + i*12, 75 + i*12)
                glow_rect.center = self.rect.center
                pygame.draw.ellipse(screen, (GOLD[0], GOLD[1], GOLD[2], 100 - i*25), glow_rect, 3)
            for angle in range(0, 360, 30):
                rad = math.radians(angle + self.frame_counter * 5)
                px = self.rect.centerx + math.cos(rad) * 40
                py = self.rect.centery + math.sin(rad) * 40
                pygame.draw.circle(screen, get_rainbow_color(self.frame_counter + angle), (int(px), int(py)), 3)
        
        if self.powerups["shield"]:
            shield_rect = pygame.Rect(0, 0, 75, 65)
            shield_rect.center = self.rect.center
            pygame.draw.ellipse(screen, (0, 255, 255, 100), shield_rect, 3)
        
        if not self.powerups["godmode"]:
            if self.is_reloading:
                reload_progress = (self.reload_time - self.reload_timer) / self.reload_time
                draw_text(f"RELOADING: {int(reload_progress * 100)}%", font_small, RED, 160, 85)
                bar_width = 200
                progress_width = bar_width * reload_progress
                pygame.draw.rect(screen, (100, 0, 0), (60, 95, bar_width, 8))
                pygame.draw.rect(screen, RED, (60, 95, progress_width, 8))
            else:
                ammo_color = YELLOW if self.current_ammo > 50 else ORANGE if self.current_ammo > 20 else RED
                draw_text(f"Ammo: {self.current_ammo}/{self.magazine_size}", font_small, ammo_color, 160, 85)
                bar_width = 200
                ammo_width = bar_width * (self.current_ammo / self.magazine_size)
                pygame.draw.rect(screen, (50, 50, 50), (60, 95, bar_width, 8))
                pygame.draw.rect(screen, ammo_color, (60, 95, ammo_width, 8))
        else:
            draw_text("GODMODE ACTIVE", font_small, GOLD, 160, 85)
            draw_text("INFINITE AMMO", font_small, CYAN, 160, 105)
        
        pygame.draw.rect(screen, RED, (15, 15, 280, 25))
        pygame.draw.rect(screen, GREEN, (15, 15, 280 * (self.health/self.max_health), 25))
        draw_text(f"Health: {self.health}/{self.max_health}", font_small, WHITE, 155, 30)

# ========== INSTRUCTIONS PAGE ==========
def instructions_page():
    clock = pygame.time.Clock()
    
    float_offset = 0
    float_direction = 1
    
    while True:
        screen.fill(BLACK)
        draw_starfield()
        draw_high_tech_border()
        
        float_offset += 0.5 * float_direction
        if float_offset > 10 or float_offset < 0:
            float_direction *= -1
        
        for i in range(5, 0, -1):
            draw_text("GALACTIC SPACE EXPLORER", font_large, (0, 100, 200), WIDTH//2, 45 - i//2)
        draw_text("GALACTIC SPACE EXPLORER", font_large, CYAN, WIDTH//2, 40)
        draw_text("========================================", font_small, GOLD, WIDTH//2, 85)
        
        left_panel = pygame.Rect(50, 110, WIDTH//2 - 70, HEIGHT - 160)
        right_panel = pygame.Rect(WIDTH//2 + 20, 110, WIDTH//2 - 70, HEIGHT - 160)
        
        pygame.draw.rect(screen, (0, 0, 30), left_panel, border_radius=15)
        pygame.draw.rect(screen, CYAN, left_panel, 2, border_radius=15)
        pygame.draw.rect(screen, (0, 0, 30), right_panel, border_radius=15)
        pygame.draw.rect(screen, CYAN, right_panel, 2, border_radius=15)
        
        left_x = left_panel.centerx
        right_x = right_panel.centerx
        
        y = 140
        draw_text("CONTROLS", font_medium, GOLD, left_x, y)
        y += 45
        draw_text("WASD or Arrow Keys - Move ship", font_small, WHITE, left_x, y)
        y += 35
        draw_text("SPACE - Shoot (hold for auto-fire)", font_small, WHITE, left_x, y)
        y += 35
        draw_text("ESC - Pause game", font_small, WHITE, left_x, y)
        y += 50
        
        draw_text("GAME ELEMENTS", font_medium, GOLD, left_x, y)
        y += 45
        draw_text("Your Ship", font_small, BLUE, left_x - 100, y)
        pygame.draw.circle(screen, BLUE, (left_x + 50, y - 5), 8)
        y += 35
        draw_text("Enemy Ship", font_small, RED, left_x - 100, y)
        pygame.draw.polygon(screen, RED, [(left_x + 50, y - 8), (left_x + 40, y + 4), (left_x + 60, y + 4)])
        y += 35
        draw_text("BOSS", font_small, DARK_PURPLE, left_x - 100, y)
        pygame.draw.circle(screen, DARK_PURPLE, (left_x + 50, y - 5), 6)
        y += 35
        draw_text("Asteroid", font_small, (150,150,150), left_x - 100, y)
        pygame.draw.circle(screen, (150,150,150), (left_x + 50, y - 5), 6)
        y += 35
        draw_text("Heal Zone", font_small, GREEN, left_x - 100, y)
        pygame.draw.rect(screen, GREEN, (left_x + 40, y - 12, 20, 20))
        y += 50
        
        draw_text("PORTAL MINIGAME", font_medium, MAGENTA, left_x, y)
        y += 45
        draw_text("Enter the swirling blue portal", font_small, YELLOW, left_x, y)
        y += 35
        draw_text("Press SPACE/UP on the beat", font_small, WHITE, left_x, y)
        y += 35
        draw_text("Perfect hit = +100 points", font_small, GREEN, left_x, y)
        y += 35
        draw_text("Miss = -5 HP", font_small, RED, left_x, y)
        
        y = 140
        draw_text("POWER-UPS", font_medium, GOLD, right_x, y)
        y += 45
        draw_text("YELLOW - IRON SPIDER", font_small, YELLOW, right_x, y)
        draw_text("3 homing lasers, halo effect", font_tiny, WHITE, right_x, y + 20)
        y += 45
        draw_text("PURPLE - Triple Shot", font_small, PURPLE, right_x, y)
        draw_text("Shoots 3 lasers at once", font_tiny, WHITE, right_x, y + 20)
        y += 45
        draw_text("BLUE - Shield", font_small, BLUE, right_x, y)
        draw_text("Temporary invincibility", font_tiny, WHITE, right_x, y + 20)
        y += 45
        draw_text("GREEN - Heal", font_small, HEAL_GREEN, right_x, y)
        draw_text("Restores 15 HP instantly", font_tiny, WHITE, right_x, y + 20)
        y += 45
        draw_text("GOLD - GODMODE", font_small, GOLD, right_x, y)
        draw_text("360 degree rainbow lasers", font_tiny, WHITE, right_x, y + 20)
        y += 60
        
        draw_text("BOSS INFO", font_medium, RED, right_x, y)
        y += 45
        draw_text("Takes 9 hits to kill", font_small, WHITE, right_x, y)
        y += 35
        draw_text("Shoots directly at YOU", font_small, BLOOD_RED, right_x, y)
        y += 35
        draw_text("20 damage (pierces shield)", font_small, BLOOD_RED, right_x, y)
        y += 35
        draw_text("Touch = INSTANT DEATH", font_small, BLOOD_RED, right_x, y)
        
        continue_btn = draw_button("CONTINUE TO MENU", WIDTH//2, HEIGHT - 45, 350, 50, GREEN, (0, 200, 0), "continue")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if continue_btn == "continue":
            return
        
        pygame.display.flip()
        clock.tick(60)

# ========== SKIN CAROUSEL MENU ==========
def carousel_menu():
    global current_skin_index, selected_skin
    
    clock = pygame.time.Clock()
    while True:
        screen.fill(BLACK)
        draw_starfield()
        draw_high_tech_border()
        
        draw_text("SELECT STARSHIP SKIN", font_large, GOLD, WIDTH//2, 70)
        draw_text(f"{len(SKINS)} SKINS AVAILABLE", font_medium, CYAN, WIDTH//2, 125)
        draw_text("LEFT / RIGHT arrows to browse", font_small, WHITE, WIDTH//2, 165)
        draw_text("Press ENTER to select", font_small, YELLOW, WIDTH//2, 195)
        
        s = SKINS[current_skin_index]
        
        preview_rect = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 - 160, 320, 320)
        pygame.draw.rect(screen, (20, 20, 40), preview_rect, border_radius=20)
        pygame.draw.rect(screen, s["color"], preview_rect, 4, border_radius=20)
        
        preview_ship = pygame.Surface((120, 100), pygame.SRCALPHA)
        pygame.draw.polygon(preview_ship, s["color"], [(60, 0), (0, 100), (120, 100)])
        pygame.draw.polygon(preview_ship, s["accent"], [(15, 50), (0, 100), (35, 85)])
        pygame.draw.polygon(preview_ship, s["accent"], [(105, 50), (120, 100), (85, 85)])
        pygame.draw.circle(preview_ship, CYAN, (60, 35), 12)
        pygame.draw.circle(preview_ship, WHITE, (60, 35), 5)
        
        rotated_ship = pygame.transform.rotate(preview_ship, math.sin(pygame.time.get_ticks() / 500) * 5)
        preview_rect_ship = rotated_ship.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(rotated_ship, preview_rect_ship)
        
        draw_text(s["name"], font_medium, s["color"], WIDTH//2, preview_rect.bottom + 45)
        
        if s["unlock"] == 0:
            draw_text("STARTING SKIN", font_small, GOLD, WIDTH//2, preview_rect.bottom + 85)
        elif high_score >= s["unlock"]:
            draw_text(f"UNLOCKED (Need {s['unlock']} pts)", font_small, GREEN, WIDTH//2, preview_rect.bottom + 85)
        else:
            draw_text(f"LOCKED (Need {s['unlock']} pts)", font_small, RED, WIDTH//2, preview_rect.bottom + 85)
        
        draw_text(f"{current_skin_index + 1} / {len(SKINS)}", font_small, WHITE, WIDTH//2, preview_rect.bottom + 125)
        
        back_btn = draw_button("BACK", 150, HEIGHT - 60, 160, 50, (100, 100, 150), (150, 150, 200), "back")
        select_btn = draw_button("SELECT", WIDTH - 150, HEIGHT - 60, 160, 50, (50, 150, 50), (100, 200, 100), "select")
        
        pygame.display.update()
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_skin_index = (current_skin_index - 1) % len(SKINS)
                elif event.key == pygame.K_RIGHT:
                    current_skin_index = (current_skin_index + 1) % len(SKINS)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if high_score >= SKINS[current_skin_index]["unlock"]:
                        selected_skin = s
                        settings["skin"] = s["name"]
                        save_settings(settings)
                        return
                elif event.key == pygame.K_ESCAPE:
                    return
        
        if back_btn == "back":
            return
        if select_btn == "select" and high_score >= SKINS[current_skin_index]["unlock"]:
            selected_skin = s
            settings["skin"] = s["name"]
            save_settings(settings)
            return

# ========== MAIN MENU ==========
def main_menu():
    global selected_skin, high_score
    
    clock = pygame.time.Clock()
    
    play_menu_music()
    
    while True:
        screen.fill(BLACK)
        draw_starfield()
        draw_high_tech_border()
        
        title_y = HEIGHT//2 - 250 + math.sin(pygame.time.get_ticks() / 800) * 3
        for i in range(5, 0, -1):
            draw_text("GALACTIC SPACE EXPLORER", font_large, (0, 100, 200), WIDTH//2, title_y - i)
        draw_text("GALACTIC SPACE EXPLORER", font_large, CYAN, WIDTH//2, title_y)
        
        draw_text("Shoot, Loot, and Portal to Scoot!", font_medium, WHITE, WIDTH//2, HEIGHT//2 - 180)
        
        high_score = load_highscore()
        draw_text(f"HIGH SCORE: {high_score}", font_medium, GOLD, WIDTH//2, HEIGHT//2 - 130)
        draw_text(f"Current Skin: {selected_skin['name']}", font_small, selected_skin["color"], WIDTH//2, HEIGHT//2 - 90)
        
        draw_text("NEW: PHIGROS PORTAL!", font_medium, MAGENTA, WIDTH//2, HEIGHT//2 - 40)
        draw_text("Enter the portal for a rhythm mini-game!", font_small, CYAN, WIDTH//2, HEIGHT//2 - 10)
        
        start_btn = draw_button("START GAME", WIDTH//2, HEIGHT//2 + 60, 280, 55, GREEN, (0, 200, 0), "start")
        skin_btn = draw_button("SELECT SKIN", WIDTH//2, HEIGHT//2 + 130, 280, 55, PURPLE, (150, 0, 150), "skin")
        quit_btn = draw_button("QUIT", WIDTH//2, HEIGHT//2 + 200, 280, 55, RED, (200, 0, 0), "quit")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if start_btn == "start":
            return True
        if skin_btn == "skin":
            carousel_menu()
        if quit_btn == "quit":
            return False
        
        pygame.display.flip()
        clock.tick(60)

# ========== MAIN GAME LOOP ==========
def main_game():
    global selected_skin, high_score
    
    play_game_music()
    
    player = Player()
    player.skin = selected_skin
    player.update_skin()
    
    health_region = HealthRegion()
    enemies = []
    bosses = []
    asteroids = []
    powerups = []
    portals = []
    explosions = []
    enemy_spawn_timer = 0
    boss_spawn_timer = random.randint(600, 1200)
    asteroid_spawn_timer = 0
    powerup_spawn_timer = random.randint(500, 800)
    godmode_spawn_timer = random.randint(1800, 3600)
    portal_spawn_timer = 30  # Spawn portal quickly for testing
    level = 1
    game_over = False
    paused = False
    auto_fire_timer = 0
    
    clock = pygame.time.Clock()
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                elif event.key == pygame.K_SPACE:
                    if player.powerups["godmode"]:
                        player.shoot()
                    elif player.powerups["rapid_fire"]:
                        player.shoot_auto_aim_with_targets(enemies, bosses)
                    else:
                        player.shoot()
                    auto_fire_timer = 5

        if auto_fire_timer > 0:
            auto_fire_timer -= 1
        elif pygame.key.get_pressed()[pygame.K_SPACE]:
            if player.powerups["godmode"]:
                player.shoot()
            elif player.powerups["rapid_fire"]:
                player.shoot_auto_aim_with_targets(enemies, bosses)
            else:
                player.shoot()
            auto_fire_timer = 5
        
        if paused:
            screen.fill(BLACK)
            draw_high_tech_border()
            draw_text("PAUSED", font_large, WHITE, WIDTH//2, HEIGHT//2)
            draw_text("Press ESC to continue", font_medium, CYAN, WIDTH//2, HEIGHT//2 + 70)
            pygame.display.flip()
            clock.tick(60)
            continue
        
        # Spawn enemies
        enemy_spawn_timer -= 1
        if enemy_spawn_timer <= 0:
            enemies.append(Enemy())
            enemy_spawn_timer = max(10, 50 - level)
        
        # Spawn boss
        boss_spawn_timer -= 1
        if boss_spawn_timer <= 0 and len(bosses) == 0:
            bosses.append(BossEnemy())
            boss_spawn_timer = random.randint(900, 1500)
        
        # Spawn asteroids
        asteroid_spawn_timer -= 1
        if asteroid_spawn_timer <= 0:
            asteroids.append(Asteroid())
            asteroid_spawn_timer = random.randint(30, 100)
        
        # Spawn powerups
        powerup_spawn_timer -= 1
        if powerup_spawn_timer <= 0:
            powerups.append(PowerUp())
            powerup_spawn_timer = random.randint(500, 800)
        
        # Spawn godmode powerup
        godmode_spawn_timer -= 1
        if godmode_spawn_timer <= 0:
            godmode_powerup = PowerUp()
            godmode_powerup.type = "godmode"
            godmode_powerup.img = pygame.Surface((30, 30))
            godmode_powerup.img.fill(GOLD)
            pygame.draw.circle(godmode_powerup.img, WHITE, (15, 15), 10, 2)
            pygame.draw.line(godmode_powerup.img, WHITE, (5, 15), (25, 15), 2)
            pygame.draw.line(godmode_powerup.img, WHITE, (15, 5), (15, 25), 2)
            powerups.append(godmode_powerup)
            godmode_spawn_timer = random.randint(2400, 4800)
        
        # SPAWN PORTAL - Increased frequency
        portal_spawn_timer -= 1
        if portal_spawn_timer <= 0 and len(portals) == 0:
            portal_x = random.randint(100, WIDTH - 100)
            portal_y = random.randint(100, HEIGHT - 100)
            portals.append(PhigrosPortal(portal_x, portal_y))
            portal_spawn_timer = random.randint(600, 1200)  # Spawn every 10-20 seconds
            try:
                powerup_sound.play()
            except:
                pass
        
        keys = pygame.key.get_pressed()
        player.update(keys)
        health_region.update(player)
        
        # Update portals
        for portal in portals[:]:
            if not portal.update():
                portals.remove(portal)
                continue
            if player.rect.colliderect(portal.rect):
                portals.remove(portal)
                mixer.music.pause()
                score_gain, health_loss = phigros_minigame(player, portal)
                mixer.music.unpause()
                try:
                    powerup_sound.play()
                except:
                    pass
        
        # Update lasers
        for laser in player.lasers[:]:
            if laser.update():
                player.lasers.remove(laser)
        
        # Update bosses
        for boss in bosses[:]:
            if boss.update((player.rect.centerx, player.rect.centery)):
                bosses.remove(boss)
                continue
            
            if player.rect.colliderect(boss.rect):
                game_over = True
                break
            
            for laser in boss.lasers[:]:
                if player.rect.colliderect(laser.rect):
                    if not player.powerups["godmode"]:
                        player.health -= 20
                    boss.lasers.remove(laser)
                    if player.health <= 0:
                        game_over = True
            
            for laser in player.lasers[:]:
                if boss.rect.colliderect(laser.rect):
                    boss.health -= 1
                    player.lasers.remove(laser)
                    if boss.health <= 0:
                        player.score += boss.score_value
                        explosions.append(Explosion(boss.rect.centerx, boss.rect.centery, 2.0))
                        bosses.remove(boss)
                        try:
                            explosion_sound.play()
                        except:
                            pass
                    break
        
        # Update enemies
        for enemy in enemies[:]:
            if enemy.update():
                enemies.remove(enemy)
                continue
            
            for laser in player.lasers[:]:
                if enemy.rect.colliderect(laser.rect):
                    enemy.health -= 10
                    player.lasers.remove(laser)
                    if enemy.health <= 0:
                        player.score += 100
                        explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
                        if enemy in enemies:
                            enemies.remove(enemy)
                        try:
                            explosion_sound.play()
                        except:
                            pass
                        if random.random() < 0.15:
                            powerups.append(PowerUp(enemy.rect.centerx, enemy.rect.centery))
                    break
            
            if player.rect.colliderect(enemy.rect):
                if not player.powerups["shield"] and not player.powerups["godmode"]:
                    player.health -= 20
                    explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
                    if enemy in enemies:
                        enemies.remove(enemy)
                    try:
                        explosion_sound.play()
                    except:
                        pass
                    if player.health <= 0:
                        game_over = True
                elif player.powerups["godmode"]:
                    explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
                    if enemy in enemies:
                        enemies.remove(enemy)
                    try:
                        explosion_sound.play()
                    except:
                        pass
                    player.score += 50
                continue
            
            for laser in enemy.lasers[:]:
                if player.rect.colliderect(laser.rect):
                    if not player.powerups["shield"] and not player.powerups["godmode"]:
                        player.health -= 5
                    enemy.lasers.remove(laser)
                    if player.health <= 0:
                        game_over = True
        
        # Update asteroids
        for asteroid in asteroids[:]:
            if asteroid.update():
                asteroids.remove(asteroid)
                continue
            
            if player.rect.colliderect(asteroid.rect):
                if not player.powerups["shield"] and not player.powerups["godmode"]:
                    player.health -= asteroid.health // 5
                    asteroid.health -= 50
                    if asteroid.health <= 0:
                        player.score += 50
                        explosions.append(Explosion(asteroid.rect.centerx, asteroid.rect.centery, 1.5))
                        asteroids.remove(asteroid)
                        try:
                            explosion_sound.play()
                        except:
                            pass
                    if player.health <= 0:
                        game_over = True
                elif player.powerups["godmode"]:
                    player.score += 50
                    explosions.append(Explosion(asteroid.rect.centerx, asteroid.rect.centery, 1.5))
                    asteroids.remove(asteroid)
                    try:
                        explosion_sound.play()
                    except:
                        pass
                    continue
            
            if asteroid in asteroids:
                for laser in player.lasers[:]:
                    if asteroid.rect.colliderect(laser.rect):
                        asteroid.health -= 10
                        player.lasers.remove(laser)
                        if asteroid.health <= 0:
                            player.score += 50
                            explosions.append(Explosion(asteroid.rect.centerx, asteroid.rect.centery, 1.5))
                            asteroids.remove(asteroid)
                            try:
                                explosion_sound.play()
                            except:
                                pass
                        break
        
        # Update powerups
        for powerup in powerups[:]:
            if powerup.update():
                powerups.remove(powerup)
                continue
            
            if player.rect.colliderect(powerup.rect):
                if powerup.type == "godmode":
                    player.powerups["godmode"] = True
                    player.powerup_timers["godmode"] = 900
                    player.current_ammo = player.magazine_size
                    player.is_reloading = False
                    play_godmode_music()
                elif powerup.type == "heal":
                    player.health = min(player.max_health, player.health + 15)
                    try:
                        powerup_sound.play()
                    except:
                        pass
                else:
                    player.powerups[powerup.type] = True
                    player.powerup_timers[powerup.type] = 600
                    try:
                        powerup_sound.play()
                    except:
                        pass
                powerups.remove(powerup)
        
        # Update explosions
        for explosion in explosions[:]:
            if explosion.update():
                explosions.remove(explosion)
        
        if player.score >= level * 1000:
            level += 1
        
        # DRAW EVERYTHING
        screen.fill(BLACK)
        draw_starfield()
        
        for laser in player.lasers:
            laser.draw(screen)
        
        player.draw(screen)
        health_region.draw(screen)
        
        for boss in bosses:
            boss.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for asteroid in asteroids:
            asteroid.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)
        for portal in portals:
            portal.draw(screen)
            portal.draw_minimap_indicator(screen)
        for explosion in explosions:
            explosion.draw(screen)
        
        draw_high_tech_border()
        
        draw_text(f"Score: {player.score}", font_small, WHITE, 90, 140)
        draw_text(f"Level: {level}", font_small, WHITE, 90, 175)
        
        y_pos = 220
        for powerup, active in player.powerups.items():
            if active:
                if powerup == "godmode":
                    color = GOLD
                    text = f"GODMODE: {player.powerup_timers[powerup] // 60}s"
                elif powerup == "rapid_fire":
                    color = YELLOW
                    text = f"IRON SPIDER: {player.powerup_timers[powerup] // 60}s"
                elif powerup == "triple_shot":
                    color = PURPLE
                    text = f"Triple Shot: {player.powerup_timers[powerup] // 60}s"
                elif powerup == "shield":
                    color = CYAN
                    text = f"Shield: {player.powerup_timers[powerup] // 60}s"
                else:
                    color = GREEN
                    text = f"{powerup.replace('_', ' ').title()}: {player.powerup_timers[powerup] // 60}s"
                draw_text(text, font_small, color, 140, y_pos, False)
                y_pos += 30
        
        pygame.display.flip()
        clock.tick(60)
    
    # Game Over
    stop_music()
    try:
        death_sound.play()
        pygame.time.wait(500)
    except:
        pass
    
    is_new_high = save_highscore(player.score)
    high_score = load_highscore()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(BLACK)
        draw_starfield()
        draw_high_tech_border()
        
        draw_text("GAME OVER", font_large, RED, WIDTH//2, HEIGHT//2 - 100)
        draw_text(f"Final Score: {player.score}", font_medium, WHITE, WIDTH//2, HEIGHT//2 - 30)
        draw_text(f"Level Reached: {level}", font_medium, WHITE, WIDTH//2, HEIGHT//2 + 25)
        
        if is_new_high:
            draw_text("NEW HIGH SCORE!", font_medium, GOLD, WIDTH//2, HEIGHT//2 + 80)
        
        restart = draw_button("PLAY AGAIN", WIDTH//2, HEIGHT//2 + 160, 240, 55, GREEN, (0, 200, 0), "restart")
        menu_btn = draw_button("MAIN MENU", WIDTH//2, HEIGHT//2 + 230, 240, 55, BLUE, (0, 0, 200), "menu")
        quit_btn = draw_button("QUIT", WIDTH//2, HEIGHT//2 + 300, 240, 55, RED, (200, 0, 0), "quit")
        
        if restart == "restart":
            return True
        if menu_btn == "menu":
            return "menu"
        if quit_btn == "quit":
            return False
        
        pygame.display.flip()
        clock.tick(60)

# ========== RUN GAME ==========
if __name__ == "__main__":
    instructions_page()
    
    while True:
        if main_menu():
            result = main_game()
            if result == "menu":
                continue
            elif not result:
                break
    pygame.quit()

    
