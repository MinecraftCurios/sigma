import pygame
import random
import sys
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
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

# Fonts
font_large = pygame.font.SysFont('arial', 50)
font_medium = pygame.font.SysFont('arial', 30)
font_small = pygame.font.SysFont('arial', 20)

# Load sounds
try:
    laser_sound = mixer.Sound('biu.wav')
    explosion_sound = mixer.Sound('boom2.wav')
    powerup_sound = mixer.Sound('mariocoin.wav')
    mixer.music.load('missionimpossible.mp3')
    mixer.music.set_volume(0.5)
except:
    print("Sound files missing - continuing without audio")

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
    
    if x - width//2 < mouse[0] < x + width//2 and y - height//2 < \
       mouse[1] < y + height//2:
        pygame.draw.rect(screen, active_color, (x - width//2, y - \
                                                height//2, width, height))
        if click[0] == 1 and action is not None:
            return action
    else:
        pygame.draw.rect(screen, inactive_color, (x - width//2, \
                                                  y - height//2, width, height))
    
    draw_text(text, font_medium, BLACK, x, y)
    return None

# ========== GAME CLASSES ==========
class Player:
    def __init__(self):
        self.img = pygame.Surface((40, 30))
        self.img.fill(BLUE)
        pygame.draw.polygon(self.img, WHITE, [(20, 0), (0, 30), (40, 30)])
        self.rect = self.img.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.lasers = []
        self.laser_cooldown = 0
        self.score = 0
        self.powerups = {
            "rapid_fire": False,
            "shield": False,
            "double_shot": False
        }
        self.powerup_timers = {
            "rapid_fire": 0,
            "shield": 0,
            "double_shot": 0
        }
    
    def update(self, keys):
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
        
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1
    
    def shoot(self):
        if self.laser_cooldown == 0:
            if 'laser_sound' in globals():
                laser_sound.play()
            
            if self.powerups["double_shot"]:
                self.lasers.append(Laser(self.rect.centerx - 15, self.rect.top))
                self.lasers.append(Laser(self.rect.centerx + 15, self.rect.top))
            else:
                self.lasers.append(Laser(self.rect.centerx, self.rect.top))
            
            self.laser_cooldown = 10 if self.powerups["rapid_fire"] else 20
    
    def draw(self, screen):
        screen.blit(self.img, self.rect)
        
        if self.powerups["shield"]:
            shield_rect = pygame.Rect(0, 0, 60, 50)
            shield_rect.center = self.rect.center
            pygame.draw.ellipse(screen, (0, 255, 255, 100), shield_rect, 2)
        
        pygame.draw.rect(screen, RED, (10, 10, 200, 20))
        pygame.draw.rect(screen, GREEN, (10, 10, 200 * \
                                         (self.health/self.max_health), 20))
        draw_text(f"Health: {self.health}/{self.max_health}", font_small, \
                  WHITE, 110, 20)

class Laser:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 2, y, 4, 15)
        self.speed = 10
        self.color = GREEN
    
    def update(self):
        self.rect.y -= self.speed
        return self.rect.bottom < 0
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Enemy:
    def __init__(self, x=None):
        self.img = pygame.Surface((30, 30))
        self.img.fill(RED)
        pygame.draw.polygon(self.img, WHITE, [(15, 0), (0, 30), (30, 30)])
        if x is None:
            x = random.randint(30, WIDTH - 30)
        self.rect = self.img.get_rect(center=(x, -30))
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
        super().__init__(x, y)
        self.rect.y = y
        self.speed = -7
        self.color = RED

class Asteroid:
    def __init__(self):
        size = random.randint(20, 60)
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

class PowerUp:
    def __init__(self, x=None, y=None):
        self.type = random.choice(["rapid_fire", "shield", "double_shot"])
        colors = {
            "rapid_fire": YELLOW,
            "shield": BLUE,
            "double_shot": PURPLE
        }
        self.img = pygame.Surface((20, 20))
        self.img.fill(colors[self.type])
        if x is None:
            x = random.randint(20, WIDTH - 20)
        if y is None:
            y = random.randint(20, HEIGHT - 20)
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

# ========== GAME LOOP ==========
def main_game():
    player = Player()
    enemies = []
    asteroids = []
    powerups = []
    explosions = []
    enemy_spawn_timer = 0
    asteroid_spawn_timer = 0
    powerup_spawn_timer = random.randint(300, 600)
    level = 1
    game_over = False
    paused = False
    
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
                elif event.key == pygame.K_SPACE and not paused:
                    player.shoot()
        
        if paused:
            screen.fill(BLACK)
            draw_text("PAUSED", font_large, WHITE, WIDTH//2, HEIGHT//2)
            draw_text("Press ESC to continue", font_medium, WHITE, \
                      WIDTH//2, HEIGHT//2 + 50)
            pygame.display.flip()
            clock.tick(60)
            continue
        
        enemy_spawn_timer -= 1
        if enemy_spawn_timer <= 0:
            enemies.append(Enemy())
            enemy_spawn_timer = max(10, 60 - level * 2)
        
        asteroid_spawn_timer -= 1
        if asteroid_spawn_timer <= 0:
            asteroids.append(Asteroid())
            asteroid_spawn_timer = random.randint(30, 120)
        
        powerup_spawn_timer -= 1
        if powerup_spawn_timer <= 0:
            powerups.append(PowerUp())
            powerup_spawn_timer = random.randint(300, 600)
        
        keys = pygame.key.get_pressed()
        player.update(keys)
        
        for laser in player.lasers[:]:
            if laser.update():
                player.lasers.remove(laser)
        
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
                        explosions.append(Explosion(enemy.rect.centerx, \
                                                    enemy.rect.centery))
                        enemies.remove(enemy)
                        if 'explosion_sound' in globals():
                            explosion_sound.play()
                        if random.random() < 0.2:
                            powerups.append(PowerUp(enemy.rect.centerx, \
                                                    enemy.rect.centery))
                    break
            
            if player.rect.colliderect(enemy.rect) and not player.powerups["shield"]:
                player.health -= 20
                explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
                enemies.remove(enemy)
                if 'explosion_sound' in globals():
                    explosion_sound.play()
                if player.health <= 0:
                    game_over = True
            
            for laser in enemy.lasers[:]:
                if player.rect.colliderect(laser.rect):
                    if not player.powerups["shield"]:
                        player.health -= 5
                    enemy.lasers.remove(laser)
                    if player.health <= 0:
                        game_over = True
        
        for asteroid in asteroids[:]:
            if asteroid.update():
                asteroids.remove(asteroid)
                continue
            
            if player.rect.colliderect(asteroid.rect) and not player.\
               powerups["shield"]:
                player.health -= asteroid.health // 5
                asteroid.health -= 50
                if asteroid.health <= 0:
                    player.score += 50
                    explosions.append(Explosion(asteroid.rect.centerx, \
                                                asteroid.rect.centery, 1.5))
                    asteroids.remove(asteroid)
                    if 'explosion_sound' in globals():
                        explosion_sound.play()
                if player.health <= 0:
                    game_over = True
            
            for laser in player.lasers[:]:
                if asteroid.rect.colliderect(laser.rect):
                    asteroid.health -= 10
                    player.lasers.remove(laser)
                    if asteroid.health <= 0:
                        player.score += 50
                        explosions.append(Explosion(asteroid.rect.centerx, \
                                                    asteroid.rect.centery, 1.5))
                        asteroids.remove(asteroid)
                        if 'explosion_sound' in globals():
                            explosion_sound.play()
                    break
        
        for powerup in powerups[:]:
            if powerup.update():
                powerups.remove(powerup)
                continue
            
            if player.rect.colliderect(powerup.rect):
                player.powerups[powerup.type] = True
                player.powerup_timers[powerup.type] = 600
                powerups.remove(powerup)
                if 'powerup_sound' in globals():
                    powerup_sound.play()
        
        for explosion in explosions[:]:
            if explosion.update():
                explosions.remove(explosion)
        
        if player.score >= level * 1000:
            level += 1
        
        screen.fill(BLACK)
        
        for _ in range(5):
            pygame.draw.circle(screen, WHITE, 
                             (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 
                             1)
        
        for laser in player.lasers:
            laser.draw(screen)
        
        player.draw(screen)
        
        for enemy in enemies:
            enemy.draw(screen)
        
        for asteroid in asteroids:
            asteroid.draw(screen)
        
        for powerup in powerups:
            powerup.draw(screen)
        
        for explosion in explosions:
            explosion.draw(screen)
        
        draw_text(f"Score: {player.score}", font_small, WHITE, 70, 40)
        draw_text(f"Level: {level}", font_small, WHITE, 70, 70)
        
        y_pos = 100
        for powerup, active in player.powerups.items():
            if active:
                color = GREEN
                timer = player.powerup_timers[powerup] // 60
                text = f"{powerup.replace('_', ' ').title()}: {timer}s"
            else:
                color = RED
                text = f"{powerup.replace('_', ' ').title()}: OFF"
            draw_text(text, font_small, color, 100, y_pos, False)
            y_pos += 20
        
        pygame.display.flip()
        clock.tick(60)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(BLACK)
        
        draw_text("GAME OVER", font_large, RED, WIDTH//2, HEIGHT//2 - 50)
        draw_text(f"Final Score: {player.score}", font_medium, WHITE, WIDTH//2, \
                  HEIGHT//2)
        draw_text(f"Level Reached: {level}", font_medium, WHITE, WIDTH//2, \
                  HEIGHT//2 + 40)
        
        restart = draw_button("Play Again", WIDTH//2, HEIGHT//2 + 100, 200, 50, \
                              GREEN, (0, 200, 0), "restart")
        quit_btn = draw_button("Quit", WIDTH//2, HEIGHT//2 + 160, 200, 50, RED, \
                               (200, 0, 0), "quit")
        
        if restart == "restart":
            return True
        if quit_btn == "quit":
            return False
        
        pygame.display.flip()
        clock.tick(60)

def main_menu():
    clock = pygame.time.Clock()
    
    while True:
        screen.fill(BLACK)
        
        draw_text("GALACTIC SPACE EXPLORER", font_large, BLUE, WIDTH//2, \
                  HEIGHT//2 - 100)
        draw_text("Navigate the asteroid field and defeat enemy ships!", \
                  font_medium, WHITE, WIDTH//2, HEIGHT//2 - 40)
        
        draw_text("Controls:", font_small, WHITE, WIDTH//2, HEIGHT//2 + 20)
        draw_text("WSDA or Arrow Keys to move", font_small, WHITE, WIDTH//2, \
                  HEIGHT//2 + 50)
        draw_text("SPACE to shoot", font_small, WHITE, WIDTH//2, HEIGHT//2 + 70)
        draw_text("ESC to pause", font_small, WHITE, WIDTH//2, HEIGHT//2 + 90)
        
        start_btn = draw_button("Start Game", WIDTH//2, HEIGHT//2 + 150, 200, 50, \
                                GREEN, (0, 200, 0), "start")
        quit_btn = draw_button("Quit", WIDTH//2, HEIGHT//2 + 210, 200, 50, \
                               RED, (200, 0, 0), "quit")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if start_btn == "start":
            return True
        if quit_btn == "quit":
            return False
        
        pygame.display.flip()
        clock.tick(60)

# ========== RUN GAME ==========
if __name__ == "__main__":
    while True:
        if main_menu():
            play_again = main_game()
            if not play_again:
                break
    pygame.quit()
