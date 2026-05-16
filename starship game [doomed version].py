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
IRON_RED = (255, 50, 50)  # Color for auto-aim lasers

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
    mixer.music.load('missionimpossible.mp3')
    mixer.music.set_volume(0.5)
    
    # GODMODE music file
    godmode_music_file = 'music.mp3'
except:
    print("Sound files missing - continuing without audio")

# ---- Storage files ----
BASE_DIR = Path(__file__).parent
SETTINGS_FILE = BASE_DIR / "starship_settings.json"
HIGHSCORE_FILE = BASE_DIR / "starship_highscore.json"

# ---- Skins for starship ----
SKINS = [
    {"name": "Classic Blue", "unlock": 0, "color": BLUE, "accent": WHITE, "laser_color": (0, 100, 255)},
    {"name": "Red Phoenix", "unlock": 5, "color": RED, "accent": YELLOW, "laser_color": (255, 50, 50)},
    {"name": "Golden Eagle", "unlock": 10, "color": (255, 215, 0), "accent": (255, 100, 0), "laser_color": (255, 200, 0)},
    {"name": "Purple Nebula", "unlock": 15, "color": PURPLE, "accent": (200, 100, 255), "laser_color": (160, 50, 255)},
    {"name": "Cyan Storm", "unlock": 20, "color": (0, 255, 255), "accent": WHITE, "laser_color": (0, 200, 200)},
    {"name": "Lava Core", "unlock": 30, "color": (255, 60, 0), "accent": (255, 200, 0), "laser_color": (255, 80, 0)},
    {"name": "Emerald", "unlock": 40, "color": (0, 255, 100), "accent": (100, 255, 100), "laser_color": (0, 200, 80)},
    {"name": "Arctic Ice", "unlock": 50, "color": (200, 230, 255), "accent": WHITE, "laser_color": (150, 200, 255)},
    {"name": "Dark Matter", "unlock": 60, "color": (50, 50, 80), "accent": (150, 150, 200), "laser_color": (100, 100, 150)},
    {"name": "Solar Flare", "unlock": 75, "color": (255, 140, 0), "accent": (255, 255, 100), "laser_color": (255, 120, 0)},
    {"name": "Cosmic Pink", "unlock": 90, "color": (255, 100, 200), "accent": (255, 200, 255), "laser_color": (255, 80, 180)},
    {"name": "Platinum", "unlock": 110, "color": (192, 192, 192), "accent": WHITE, "laser_color": (180, 180, 180)},
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

# ========== HELPER FUNCTIONS ==========
def draw_text(text, font, color, x, y, center=True):
    text_surface = font.render(text, True, color)
    if center:
        screen.blit(text_surface, (x - text_surface.get_width()//2, y - \
                                   text_surface.get_height()//2))
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
    for _ in range(8):
        pygame.draw.circle(screen, WHITE, 
                         (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 
                         1)

def get_rainbow_color(frame):
    """Return a rainbow color based on frame counter"""
    colors = [
        (255, 0, 0),    # Red
        (255, 165, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),    # Green
        (0, 255, 255),  # Cyan
        (0, 0, 255),    # Blue
        (128, 0, 255),  # Purple
        (255, 0, 255)   # Magenta
    ]
    return colors[frame % len(colors)]

# ========== INSTRUCTIONS PAGE ==========
def instructions_page():
    clock = pygame.time.Clock()
    
    while True:
        screen.fill(BLACK)
        draw_starfield()
        
        draw_text("GAME INSTRUCTIONS", font_large, GOLD, WIDTH//2, 50)
        
        draw_text("CONTROLS:", font_medium, CYAN, WIDTH//2, 110)
        draw_text("• WASD or Arrow Keys - Move your ship", font_small, WHITE, WIDTH//2, 155)
        draw_text("• SPACE - Shoot (hold for auto-fire)", font_small, WHITE, WIDTH//2, 185)
        draw_text("• ESC - Pause game", font_small, WHITE, WIDTH//2, 215)
        
        draw_text("GAME ELEMENTS:", font_medium, CYAN, WIDTH//2, 265)
        draw_text("• Colored Triangle - Your ship (changes color with skin)", font_small, BLUE, WIDTH//2, 305)
        draw_text("• Red Triangles - Enemy ships (shoot at you)", font_small, RED, WIDTH//2, 335)
        draw_text("• DARK PURPLE w/ GOLD Spikes - BOSS SHIP (EXTREMELY DANGEROUS!)", font_small, DARK_PURPLE, WIDTH//2, 365)
        draw_text("• Gray Circles - Asteroids (avoid or shoot)", font_small, (150, 150, 150), WIDTH//2, 395)
        draw_text("• Green Square - Healing zone (stand inside to heal)", font_small, GREEN, WIDTH//2, 425)
        
        draw_text("POWER-UPS:", font_medium, CYAN, WIDTH//2, 475)
        draw_text("• Yellow - IRON SPIDER MODE (3 auto-aim laser lines, instant fire!)", font_small, YELLOW, WIDTH//2, 515)
        draw_text("• Purple - Triple Shot (shoots 3 lasers)", font_small, PURPLE, WIDTH//2, 545)
        draw_text("• Blue - Shield (temporary invincibility - DOES NOT block boss)", font_small, BLUE, WIDTH//2, 575)
        draw_text("• Bright Green - HEALING (restores 15 health instantly!)", font_small, HEAL_GREEN, WIDTH//2, 605)
        draw_text("• GOLD - GODMODE (ULTRA RARE! Full 360° rainbow lasers, invincible!)", font_small, GOLD, WIDTH//2, 635)
        
        draw_text("BOSS INFO:", font_medium, RED, WIDTH//2, 685)
        draw_text("• Spawns randomly - Takes 9 hits to kill - Shoots directly at you", font_small, RED, WIDTH//2, 725)
        draw_text("• BOSS SHOTS: 20 damage (pierces shield!) - Touch = INSTANT DEATH (even in GODMODE!)", font_small, BLOOD_RED, WIDTH//2, 755)
        
        continue_btn = draw_button("CONTINUE TO MENU", WIDTH//2, HEIGHT - 30, 350, 50, GREEN, (0, 200, 0), "continue")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if continue_btn == "continue":
            return
        
        pygame.display.flip()
        clock.tick(60)

# ========== AUTO-AIM LASER CLASS (FIXED) ==========
class AutoAimLaser:
    def __init__(self, x, y, target_enemy, target_boss):
        self.x = x  # Start at ship's nose
        self.y = y
        self.start_x = x
        self.start_y = y
        self.target_enemy = target_enemy  # Store reference to enemy object
        self.target_boss = target_boss    # Store reference to boss object
        self.speed = 18  # Faster speed for better tracking
        self.color = IRON_RED
        self.alive = True
        self.rect = pygame.Rect(x - 3, y - 3, 6, 6)
    
    def get_target_position(self):
        """Get current position of the target (handles moving enemies)"""
        # Check if enemy still exists and has a rect attribute
        if self.target_enemy is not None:
            try:
                # Check if the enemy still has a rect (hasn't been destroyed)
                if hasattr(self.target_enemy, 'rect') and self.target_enemy.rect is not None:
                    return (self.target_enemy.rect.centerx, self.target_enemy.rect.centery)
            except:
                pass
        
        # Check if boss still exists
        if self.target_boss is not None:
            try:
                if hasattr(self.target_boss, 'rect') and self.target_boss.rect is not None:
                    return (self.target_boss.rect.centerx, self.target_boss.rect.centery)
            except:
                pass
        
        return None
    
    def update(self):
        # Get current target position (enemy might have moved)
        target_pos = self.get_target_position()
        
        if target_pos is None:
            # Target died, laser disappears
            self.alive = False
            return True
        
        # Recalculate direction to moving target
        dx = target_pos[0] - self.x
        dy = target_pos[1] - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Move toward target with constant speed
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
        else:
            self.x += dx
            self.y += dy
        
        self.rect.x = int(self.x - 3)
        self.rect.y = int(self.y - 3)
        
        # Check if out of bounds
        return (self.rect.bottom < 0 or self.rect.top > HEIGHT or 
                self.rect.right < 0 or self.rect.left > WIDTH)
    
    def draw(self, screen):
        # Draw line from ship to current position for trail effect
        pygame.draw.line(screen, self.color, (int(self.start_x), int(self.start_y)), (int(self.x), int(self.y)), 4)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 2)

# ========== BOSS ENEMY CLASS ==========
class BossEnemy:
    def __init__(self):
        self.img = pygame.Surface((70, 70), pygame.SRCALPHA)
        # Main body - dark purple
        pygame.draw.polygon(self.img, DARK_PURPLE, [(35, 0), (0, 70), (70, 70)])
        # Gold spikes on edges
        for i in range(3):
            spike_x = 10 + i * 25
            pygame.draw.polygon(self.img, SPIKE_GOLD, [(spike_x, 20), (spike_x - 5, 35), (spike_x + 5, 35)])
        # Red blotches
        pygame.draw.circle(self.img, BLOOD_RED, (35, 45), 12)
        pygame.draw.circle(self.img, BLOOD_RED, (20, 30), 8)
        pygame.draw.circle(self.img, BLOOD_RED, (50, 30), 8)
        # Eyes
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
        
        # Shoot directly at player
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
        # Calculate direction to player
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 0:
            dx /= distance
            dy /= distance
        self.lasers.append(BossLaser(self.rect.centerx, self.rect.centery, dx, dy))
    
    def draw(self, screen):
        screen.blit(self.img, self.rect)
        # Draw health bar
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
        self.speed = 10
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

# ========== GAME CLASSES ==========
class Player:
    def __init__(self):
        global selected_skin
        self.skin = selected_skin
        self.img = pygame.Surface((50, 40))
        self.img.fill(self.skin["color"])
        pygame.draw.polygon(self.img, self.skin["accent"], [(25, 0), (0, 40), (50, 40)])
        self.rect = self.img.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.speed = 7 #<=== change player speed
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
        
        # Track GODMODE music
        self.godmode_music_playing = False
        
        self.magazine_size = 200
        self.current_ammo = 200
        self.is_reloading = False
        self.reload_timer = 0
        self.reload_time = 60
    
    def update_skin(self):
        self.img = pygame.Surface((50, 40))
        self.img.fill(self.skin["color"])
        pygame.draw.polygon(self.img, self.skin["accent"], [(25, 0), (0, 40), (50, 40)])
    
    def update(self, keys):
        self.frame_counter += 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))
        
        for powerup in self.powerup_timers:
            if self.powerup_timers[powerup] > 0:
                self.powerup_timers[powerup] -= 1
                if self.powerup_timers[powerup] == 0:
                    self.powerups[powerup] = False
        
        # Handle GODMODE music
        if self.powerups["godmode"]:
            if not self.godmode_music_playing:
                try:
                    mixer.music.load('music.mp3')
                    mixer.music.play(-1)
                    mixer.music.set_volume(0.7)
                    self.godmode_music_playing = True
                    print("GODMODE MUSIC STARTED")
                except Exception as e:
                    print(f"Could not play GODMODE music: {e}")
        else:
            if self.godmode_music_playing:
                try:
                    mixer.music.load('missionimpossible.mp3')
                    mixer.music.play(-1)
                    mixer.music.set_volume(0.5)
                    self.godmode_music_playing = False
                    print("GODMODE MUSIC STOPPED")
                except Exception as e:
                    print(f"Could not restore normal music: {e}")
        
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1
        
        self.update_reload()
    
    def find_nearest_enemies(self, enemies, bosses, count=3):
        """Find the nearest enemies to aim at"""
        all_targets = []
        
        # Add all enemies
        for enemy in enemies:
            dist = math.sqrt((enemy.rect.centerx - self.rect.centerx)**2 + 
                           (enemy.rect.centery - self.rect.centery)**2)
            all_targets.append((dist, enemy, None))
        
        # Add all bosses
        for boss in bosses:
            dist = math.sqrt((boss.rect.centerx - self.rect.centerx)**2 + 
                           (boss.rect.centery - self.rect.centery)**2)
            all_targets.append((dist, None, boss))
        
        # Sort by distance and return top 'count' targets
        all_targets.sort(key=lambda x: x[0])
        return all_targets[:count]
    
    def shoot(self):
        if self.is_reloading and not self.powerups["godmode"]:
            return
        
        if self.powerups["godmode"]:
            if self.laser_cooldown == 0:
                if 'laser_sound' in globals():
                    laser_sound.play()
                
                for angle in range(0, 360, 20):
                    self.lasers.append(GodModeLaser(self.rect.centerx, self.rect.centery, angle, self.frame_counter))
                
                self.laser_cooldown = 1
            return
        
        if self.current_ammo <= 0:
            self.start_reload()
            return
        
        if self.laser_cooldown == 0:
            if 'laser_sound' in globals():
                laser_sound.play()
            
            if self.powerups["triple_shot"]:
                self.lasers.append(Laser(self.rect.centerx - 25, self.rect.top, self.skin["laser_color"]))
                self.lasers.append(Laser(self.rect.centerx, self.rect.top, self.skin["laser_color"]))
                self.lasers.append(Laser(self.rect.centerx + 25, self.rect.top, self.skin["laser_color"]))
                self.current_ammo -= 3
            else:
                self.lasers.append(Laser(self.rect.centerx, self.rect.top, self.skin["laser_color"]))
                self.current_ammo -= 1
            
            self.laser_cooldown = 0  # Base firing rate changed to 0
            
            if self.current_ammo <= 0:
                self.start_reload()
    
    def shoot_auto_aim(self, enemies, bosses):
        """Special auto-aim shot for Iron Spider mode - shoots 3 homing lasers that track moving enemies"""
        if self.is_reloading:
            return
        
        if self.current_ammo <= 0:
            self.start_reload()
            return
        
        if self.laser_cooldown == 0:
            if 'laser_sound' in globals():
                laser_sound.play()
            
            # Find 3 nearest targets (enemies or bosses)
            targets = self.find_nearest_enemies(enemies, bosses, 3)
            
            # Create auto-aim lasers for each target
            lasers_created = 0
            for dist, enemy, boss in targets:
                if enemy or boss:
                    # Laser starts from the tip of the ship (nose)
                    laser_x = self.rect.centerx
                    laser_y = self.rect.top
                    self.lasers.append(AutoAimLaser(laser_x, laser_y, enemy, boss))
                    lasers_created += 1
            
            # If no targets found, shoot 3 lasers in a spread pattern
            if lasers_created == 0:
                self.lasers.append(Laser(self.rect.centerx - 15, self.rect.top, IRON_RED))
                self.lasers.append(Laser(self.rect.centerx, self.rect.top, IRON_RED))
                self.lasers.append(Laser(self.rect.centerx + 15, self.rect.top, IRON_RED))
            
            self.current_ammo -= 1
            self.laser_cooldown = 0  # Instant fire
            
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
        screen.blit(self.img, self.rect)
        
        if self.powerups["godmode"]:
            for i in range(3):
                glow_rect = pygame.Rect(0, 0, 80 + i*10, 70 + i*10)
                glow_rect.center = self.rect.center
                pygame.draw.ellipse(screen, (GOLD[0], GOLD[1], GOLD[2], 100 - i*30), glow_rect, 3)
        
        if self.powerups["shield"]:
            shield_rect = pygame.Rect(0, 0, 75, 65)
            shield_rect.center = self.rect.center
            pygame.draw.ellipse(screen, (0, 255, 255, 100), shield_rect, 3)
        
        if not self.powerups["godmode"]:
            if self.is_reloading:
                reload_progress = (self.reload_time - self.reload_timer) / self.reload_time
                reload_text = f"RELOADING: {int(reload_progress * 100)}%"
                draw_text(reload_text, font_small, RED, 160, 85)
            else:
                ammo_color = YELLOW if self.current_ammo > 0 else RED
                draw_text(f"Ammo: {self.current_ammo}/{self.magazine_size}", font_small, ammo_color, 160, 85)
        else:
            draw_text("GODMODE ACTIVE!", font_small, GOLD, 160, 85)
        
        pygame.draw.rect(screen, RED, (15, 15, 280, 25))
        pygame.draw.rect(screen, GREEN, (15, 15, 280 * (self.health/self.max_health), 25))
        draw_text(f"Health: {self.health}/{self.max_health}", font_small, WHITE, 155, 30)

class Laser:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x - 3, y, 6, 20)
        self.speed = 12
        self.color = color
    
    def update(self):
        self.rect.y -= self.speed
        return self.rect.bottom < 0
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class GodModeLaser:
    def __init__(self, x, y, angle, frame):
        self.rect = pygame.Rect(x - 2, y - 10, 4, 15)
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 15
        self.frame = frame
        self.color = get_rainbow_color(frame + angle)
        rad = math.radians(angle)
        self.vx = math.sin(rad) * self.speed
        self.vy = -math.cos(rad) * self.speed
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x - 2)
        self.rect.y = int(self.y - 10)
        self.color = get_rainbow_color(self.frame)
        self.frame += 1
        return (self.rect.bottom < 0 or self.rect.top > HEIGHT or 
                self.rect.right < 0 or self.rect.left > WIDTH)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

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
        self.color = GREEN
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
        s.fill((0, 255, 0, 100))
        screen.blit(s, (WIDTH - 140, HEIGHT - 140))
        pygame.draw.rect(screen, GREEN, self.rect, 3)
        draw_text("HEAL", font_medium, WHITE, WIDTH - 80, HEIGHT - 80)

class PowerUp:
    def __init__(self, x=None, y=None):
        powerup_types = ["rapid_fire", "shield", "triple_shot", "triple_shot", "rapid_fire", "shield", "godmode", "heal", "heal"]
        self.type = random.choice(powerup_types)
        
        colors = {
            "rapid_fire": YELLOW,
            "shield": BLUE,
            "triple_shot": PURPLE,
            "godmode": GOLD,
            "heal": HEAL_GREEN
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
        self.color = random.choice([RED, ORANGE, YELLOW])
        for _ in range(20):
            self.particles.append({
                'x': x,
                'y': y,
                'dx': random.uniform(-3, 3),
                'dy': random.uniform(-3, 3),
                'size': random.randint(2, 5) * size,
                'life': random.randint(20, 40)
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
            pygame.draw.circle(screen, self.color, 
                             (int(particle['x']), int(particle['y'])), 
                             int(particle['size']))

# ========== SKIN CAROUSEL MENU ==========
def carousel_menu():
    global current_skin_index, selected_skin
    
    clock = pygame.time.Clock()
    while True:
        screen.fill(BLACK)
        draw_starfield()
        
        draw_text("SELECT STARSHIP SKIN", font_large, BLUE, WIDTH//2, 100)
        draw_text("Use LEFT/RIGHT arrows to browse, ENTER to select", font_medium, WHITE, WIDTH//2, 170)
        
        s = SKINS[current_skin_index]
        
        preview_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 150, 300, 300)
        pygame.draw.rect(screen, (30, 30, 40), preview_rect, border_radius=15)
        
        preview_ship = pygame.Surface((100, 80))
        preview_ship.fill(s["color"])
        pygame.draw.polygon(preview_ship, s["accent"], [(50, 0), (0, 80), (100, 80)])
        preview_rect_ship = preview_ship.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(preview_ship, preview_rect_ship)
        
        skin_color = s["color"]
        draw_text(s["name"], font_medium, skin_color, WIDTH//2, preview_rect.bottom + 60)
        draw_text(f"Unlock at: {s['unlock']} points", font_small, YELLOW, WIDTH//2, preview_rect.bottom + 100)
        draw_text(f"{current_skin_index + 1} / {len(SKINS)}", font_small, WHITE, WIDTH//2, preview_rect.bottom + 140)
        
        back_btn = draw_button("BACK", 150, HEIGHT - 70, 200, 60, (100, 100, 150), (150, 150, 200), "back")
        select_btn = draw_button("SELECT", WIDTH - 150, HEIGHT - 70, 200, 60, (50, 150, 50), (100, 200, 100), "select")
        
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
                    selected_skin = s
                    settings["skin"] = s["name"]
                    save_settings(settings)
                    return
                elif event.key == pygame.K_ESCAPE:
                    return
        
        if back_btn == "back":
            return
        if select_btn == "select":
            selected_skin = s
            settings["skin"] = s["name"]
            save_settings(settings)
            return

# ========== MAIN MENU ==========
def main_menu():
    global selected_skin, high_score
    
    clock = pygame.time.Clock()
    
    while True:
        screen.fill(BLACK)
        draw_starfield()
        
        draw_text("GALACTIC SPACE EXPLORER", font_large, BLUE, WIDTH//2, HEIGHT//2 - 260)
        draw_text("Shoot, Loot, and get ready to Scoot!", font_medium, WHITE, WIDTH//2, HEIGHT//2 - 180)
        
        high_score = load_highscore()
        draw_text(f"HIGH SCORE: {high_score}", font_medium, GOLD, WIDTH//2, HEIGHT//2 - 130)
        
        draw_text(f"Current Skin: {selected_skin['name']}", font_small, selected_skin["color"], WIDTH//2, HEIGHT//2 - 90)
        
        draw_text("Controls:", font_medium, WHITE, WIDTH//2, HEIGHT//2 - 30)
        draw_text("WASD or Arrow Keys to move", font_small, WHITE, WIDTH//2, HEIGHT//2 + 15)
        draw_text("SPACE to shoot (hold for auto-fire)", font_small, WHITE, WIDTH//2, HEIGHT//2 + 50)
        draw_text("ESC to pause", font_small, WHITE, WIDTH//2, HEIGHT//2 + 85)
        
        start_btn = draw_button("START GAME", WIDTH//2, HEIGHT//2 + 150, 280, 60, GREEN, (0, 200, 0), "start")
        skin_btn = draw_button("SELECT SKIN", WIDTH//2, HEIGHT//2 + 225, 280, 60, PURPLE, (150, 0, 150), "skin")
        quit_btn = draw_button("QUIT", WIDTH//2, HEIGHT//2 + 300, 280, 60, RED, (200, 0, 0), "quit")
        
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

# ========== GAME LOOP ==========
def main_game():
    global selected_skin, high_score
    
    player = Player()
    player.skin = selected_skin
    player.update_skin()
    
    health_region = HealthRegion()
    enemies = []
    bosses = []
    asteroids = []
    powerups = []
    explosions = []
    enemy_spawn_timer = 0
    boss_spawn_timer = random.randint(600, 1200)
    asteroid_spawn_timer = 0
    powerup_spawn_timer = random.randint(300, 600)
    level = 1
    game_over = False
    paused = False
    auto_fire_timer = 0
    
    try:
        mixer.music.play(-1)
    except:
        pass
    
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
                    if player.powerups["rapid_fire"]:
                        player.shoot_auto_aim(enemies, bosses)
                    else:
                        player.shoot()
                    auto_fire_timer = 5

        if auto_fire_timer > 0:
            auto_fire_timer -= 1
        elif pygame.key.get_pressed()[pygame.K_SPACE]:
            if player.powerups["rapid_fire"]:
                player.shoot_auto_aim(enemies, bosses)
            else:
                player.shoot()
            auto_fire_timer = 5
        
        if paused:
            screen.fill(BLACK)
            draw_text("PAUSED", font_large, WHITE, WIDTH//2, HEIGHT//2)
            draw_text("Press ESC to continue", font_medium, WHITE, WIDTH//2, HEIGHT//2 + 70)
            pygame.display.flip()
            clock.tick(60)
            continue
        
        enemy_spawn_timer -= 1
        if enemy_spawn_timer <= 0:
            enemies.append(Enemy())
            enemy_spawn_timer = max(10, 60 - level * 2)
        
        boss_spawn_timer -= 1
        if boss_spawn_timer <= 0 and len(bosses) == 0:
            bosses.append(BossEnemy())
            boss_spawn_timer = random.randint(600, 1200)
        
        asteroid_spawn_timer -= 1
        if asteroid_spawn_timer <= 0:
            asteroids.append(Asteroid())
            asteroid_spawn_timer = random.randint(30, 120)
        
        powerup_spawn_timer -= 1
        if powerup_spawn_timer <= 0:
            powerups.append(PowerUp())
            powerup_spawn_timer = random.randint(400, 700)
        
        keys = pygame.key.get_pressed()
        player.update(keys)
        health_region.update(player)
        
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
                        if 'explosion_sound' in globals():
                            explosion_sound.play()
                    break
        
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
                        enemies.remove(enemy)
                        if 'explosion_sound' in globals():
                            explosion_sound.play()
                        if random.random() < 0.2:
                            powerups.append(PowerUp(enemy.rect.centerx, enemy.rect.centery))
                    break
            
            if player.rect.colliderect(enemy.rect) and not player.powerups["shield"] and not player.powerups["godmode"]:
                player.health -= 20
                explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
                enemies.remove(enemy)
                if 'explosion_sound' in globals():
                    explosion_sound.play()
                if player.health <= 0:
                    game_over = True
            elif player.rect.colliderect(enemy.rect) and player.powerups["godmode"]:
                explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
                enemies.remove(enemy)
                if 'explosion_sound' in globals():
                    explosion_sound.play()
                player.score += 50
            
            for laser in enemy.lasers[:]:
                if player.rect.colliderect(laser.rect):
                    if not player.powerups["shield"] and not player.powerups["godmode"]:
                        player.health -= 5
                    enemy.lasers.remove(laser)
                    if player.health <= 0:
                        game_over = True
        
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
                        if 'explosion_sound' in globals():
                            explosion_sound.play()
                    if player.health <= 0:
                        game_over = True
                elif player.powerups["godmode"]:
                    player.score += 50
                    explosions.append(Explosion(asteroid.rect.centerx, asteroid.rect.centery, 1.5))
                    asteroids.remove(asteroid)
                    if 'explosion_sound' in globals():
                        explosion_sound.play()
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
                            if 'explosion_sound' in globals():
                                explosion_sound.play()
                        break
        
        for powerup in powerups[:]:
            if powerup.update():
                powerups.remove(powerup)
                continue
            
            if player.rect.colliderect(powerup.rect):
                if powerup.type == "godmode":
                    player.powerups["godmode"] = True
                    player.powerup_timers["godmode"] = 900 #<=== change godmode duration
                    player.current_ammo = player.magazine_size
                    player.is_reloading = False
                elif powerup.type == "heal":
                    player.health = min(player.max_health, player.health + 10) #<=== change regen amount
                    if 'powerup_sound' in globals():
                        powerup_sound.play()
                else:
                    player.powerups[powerup.type] = True
                    player.powerup_timers[powerup.type] = 600
                    if 'powerup_sound' in globals():
                        powerup_sound.play()
                
                powerups.remove(powerup)
        
        for explosion in explosions[:]:
            if explosion.update():
                explosions.remove(explosion)
        
        if player.score >= level * 1000:
            level += 1
        
        screen.fill(BLACK)
        
        for _ in range(8):
            pygame.draw.circle(screen, WHITE, 
                             (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 
                             1)
        
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
        
        for explosion in explosions:
            explosion.draw(screen)
        
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
                    text = f"IRON SPIDER MODE: {player.powerup_timers[powerup] // 60}s"
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
    
    # Save high score
    is_new_high = save_highscore(player.score)
    high_score = load_highscore()
    
    # Game over screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(BLACK)
        draw_starfield()
        
        draw_text("GAME OVER", font_large, RED, WIDTH//2, HEIGHT//2 - 100)
        draw_text(f"Final Score: {player.score}", font_medium, WHITE, WIDTH//2, HEIGHT//2 - 30)
        draw_text(f"Level Reached: {level}", font_medium, WHITE, WIDTH//2, HEIGHT//2 + 25)
        
        if is_new_high:
            draw_text("NEW HIGH SCORE!", font_medium, GOLD, WIDTH//2, HEIGHT//2 + 80)
        
        restart = draw_button("PLAY AGAIN", WIDTH//2, HEIGHT//2 + 160, 240, 60, GREEN, (0, 200, 0), "restart")
        menu_btn = draw_button("MAIN MENU", WIDTH//2, HEIGHT//2 + 240, 240, 60, BLUE, (0, 0, 200), "menu")
        quit_btn = draw_button("QUIT", WIDTH//2, HEIGHT//2 + 320, 240, 60, RED, (200, 0, 0), "quit")
        
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

    
