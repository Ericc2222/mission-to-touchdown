import pygame
import sys
import math
import random
from enum import Enum
import os

# Initialize Pygame and its mixer for sound
pygame.init()
pygame.mixer.init()

# Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (50, 255, 50)
ORANGE = (255, 165, 0)

class GameState(Enum):
    MENU = 1
    PLANET_SELECT = 2
    PLAYING = 3
    GAME_OVER = 4
    VICTORY = 5

class Planet:
    def __init__(self, name, gravity, has_atmosphere):
        self.name = name
        self.gravity = gravity
        self.has_atmosphere = has_atmosphere
        self.surface_color = None
        self.atmosphere_color = None
        self.surface_height = 150  # Make ground more visible
        self.description = ""
        self.wind_force = 0  # Horizontal force
        self.landing_pad_x = random.randint(200, WINDOW_WIDTH - 200)  # Random pad position
        self.landing_pad_width = 100
        self.setup_planet_properties()

    def setup_planet_properties(self):
        if self.name == "Moon":
            self.gravity = 1.62  # m/s²
            self.surface_color = (200, 200, 200)  # Lighter gray
            self.atmosphere_color = None
            self.wind_force = 0
            self.description = "Low gravity (1.6 m/s²)\nNo atmosphere\nPerfect for precise landing!"
        elif self.name == "Mars":
            self.gravity = 3.72  # m/s²
            self.surface_color = (194, 98, 45)  # Reddish
            self.atmosphere_color = (255, 150, 100, 50)
            self.wind_force = random.uniform(-0.1, 0.1)  # Light wind
            self.description = "Medium gravity (3.7 m/s²)\nThin atmosphere\nWatch for dust storms!"
        elif self.name == "Earth":
            self.gravity = 9.81  # m/s²
            self.surface_color = (100, 150, 255)  # Bluish
            self.atmosphere_color = (150, 200, 255, 50)
            self.wind_force = random.uniform(-0.2, 0.2)  # Moderate wind
            self.description = "Strong gravity (9.8 m/s²)\nThick atmosphere\nStrong winds!"
        elif self.name == "Europa":
            self.gravity = 1.315  # m/s²
            self.surface_color = (220, 220, 255)  # Icy white-blue
            self.atmosphere_color = None
            self.wind_force = 0
            self.description = "Very low gravity (1.3 m/s²)\nNo atmosphere\nIcy surface!"
        elif self.name == "Mystery Planet X":
            self.gravity = random.uniform(1, 12)
            self.surface_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            self.has_atmosphere = random.choice([True, False])
            self.wind_force = random.uniform(-0.3, 0.3) if self.has_atmosphere else 0
            if self.has_atmosphere:
                self.atmosphere_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255), 50)
            self.description = f"Mystery gravity ({self.gravity:.1f} m/s²)\n{'Has atmosphere' if self.has_atmosphere else 'No atmosphere'}\nUnpredictable!"

    def draw(self, screen):
        # Draw atmosphere if present
        if self.atmosphere_color:
            atmosphere = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            atmosphere.fill(self.atmosphere_color)
            atmosphere.set_alpha(50)
            screen.blit(atmosphere, (0, 0))
        
        # Draw surface with some terrain variation
        ground_y = WINDOW_HEIGHT - self.surface_height
        pygame.draw.rect(screen, self.surface_color,
                        (0, ground_y, WINDOW_WIDTH, self.surface_height))
        
        # Draw landing pad
        pad_y = ground_y
        pad_color = GREEN if abs(self.wind_force) < 0.1 else (YELLOW if abs(self.wind_force) < 0.2 else ORANGE)
        pygame.draw.rect(screen, pad_color,
                        (self.landing_pad_x - self.landing_pad_width//2, pad_y,
                         self.landing_pad_width, 10))
        
        # Draw landing pad lights
        for x in range(self.landing_pad_x - self.landing_pad_width//2, 
                      self.landing_pad_x + self.landing_pad_width//2, 20):
            pygame.draw.circle(screen, WHITE, (x, pad_y + 5), 2)
        
        # Add some surface details (craters or rocks)
        for i in range(10):
            x = random.randint(0, WINDOW_WIDTH)
            if abs(x - self.landing_pad_x) > self.landing_pad_width:  # Don't put rocks on landing pad
                pygame.draw.circle(screen, (min(255, self.surface_color[0] - 30),
                                         min(255, self.surface_color[1] - 30),
                                         min(255, self.surface_color[2] - 30)),
                                 (x, ground_y + random.randint(10, 40)), random.randint(5, 15))

class Spacecraft:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.velocity_x = random.uniform(-2, 2)  # Initial orbital velocity
        self.angle = 0  # Always upright
        self.thrust_power = 0.5
        self.horizontal_power = 0.3  # Power for left/right movement
        self.fuel = 50
        self.width = 40
        self.height = 60
        self.is_thrusting = False
        self.moving_left = False
        self.moving_right = False
        self.parachute_deployed = False
        self.landed = False
        self.landing_effect_timer = 0
        self.fuel_warning_timer = 0

    def apply_thrust(self):
        if self.fuel > 0 and self.is_thrusting and not self.landed:
            # Thrust is always upward
            self.velocity_y -= self.thrust_power
            self.fuel -= 1.0

            # Update warning timer when fuel is low
            if self.fuel <= 10:
                self.fuel_warning_timer = 30

    def apply_horizontal_movement(self):
        if self.landed:
            return

        # Apply horizontal movement based on input
        if self.moving_left and self.fuel > 0:
            self.velocity_x -= self.horizontal_power
            self.fuel -= 0.5  # Less fuel usage for horizontal movement
        if self.moving_right and self.fuel > 0:
            self.velocity_x += self.horizontal_power
            self.fuel -= 0.5  # Less fuel usage for horizontal movement

    def update(self, planet):
        if self.landed:
            if self.landing_effect_timer > 0:
                self.landing_effect_timer -= 1
            return None

        # Update fuel warning timer
        if self.fuel_warning_timer > 0:
            self.fuel_warning_timer -= 1

        # Apply gravity
        self.velocity_y += planet.gravity * 0.016  # 1/60th of a second

        # Apply wind force if there's atmosphere
        if planet.has_atmosphere:
            # Wind effect is stronger at higher altitudes
            altitude_factor = min(1.0, (WINDOW_HEIGHT - self.y) / WINDOW_HEIGHT)
            effective_wind = planet.wind_force * altitude_factor
            self.velocity_x += effective_wind * 0.016
            
            # Simple air resistance
            self.velocity_x *= 0.99  # Slight horizontal drag
            self.velocity_y *= 0.99  # Slight vertical drag

        # Apply atmospheric drag if planet has atmosphere and parachute is deployed
        if planet.has_atmosphere and self.parachute_deployed:
            drag = 0.02
            self.velocity_y *= (1 - drag)
            self.velocity_x *= (1 - drag)

        # Apply horizontal movement
        self.apply_horizontal_movement()

        # Update horizontal position
        self.x += self.velocity_x
        
        # Keep spacecraft in bounds with bounce effect
        if self.x < self.width/2:
            self.x = self.width/2
            self.velocity_x = abs(self.velocity_x) * 0.5
        elif self.x > WINDOW_WIDTH - self.width/2:
            self.x = WINDOW_WIDTH - self.width/2
            self.velocity_x = -abs(self.velocity_x) * 0.5

        # Update vertical position and check for landing
        ground_y = WINDOW_HEIGHT - planet.surface_height
        next_y = self.y + self.velocity_y
        
        if next_y + self.height/2 >= ground_y:
            # We've hit the ground
            self.y = ground_y - self.height/2
            
            # Check if we're on the landing pad
            on_pad = abs(self.x - planet.landing_pad_x) < planet.landing_pad_width/2
            
            # Check for safe landing
            if (abs(self.velocity_y) < 2 and  # Vertical speed ok
                abs(self.velocity_x) < 1 and  # Horizontal speed ok
                on_pad):                      # On the pad
                self.landed = True
                self.landing_effect_timer = 60
                self.velocity_y = 0
                self.velocity_x = 0
                return True  # Safe landing
            else:
                self.velocity_y = 0  # Stop vertical movement on crash
                self.velocity_x = 0  # Stop horizontal movement on crash
                return False  # Crash
        else:
            self.y = next_y
            return None  # Still flying

    def draw(self, screen):
        # Draw fuel warning when low
        if self.fuel <= 10 and self.fuel_warning_timer > 0 and not self.landed:
            warning_font = pygame.font.Font(None, 48)
            warning_text = warning_font.render("LOW FUEL!", True, RED)
            warning_rect = warning_text.get_rect(center=(WINDOW_WIDTH/2, 50))
            screen.blit(warning_text, warning_rect)

        # Draw landing effect if just landed
        if self.landed and self.landing_effect_timer > 0:
            # Draw expanding circle
            effect_radius = (60 - self.landing_effect_timer) * 2
            effect_alpha = int((self.landing_effect_timer / 60) * 255)
            effect_surface = pygame.Surface((effect_radius * 2, effect_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(effect_surface, (*GREEN, effect_alpha), 
                             (effect_radius, effect_radius), effect_radius, 2)
            screen.blit(effect_surface, 
                       (self.x - effect_radius, self.y + self.height/2 - effect_radius))

        # Draw the spacecraft body (more detailed)
        points = [
            (self.x - self.width/3, self.y + self.height/2),  # Bottom left
            (self.x + self.width/3, self.y + self.height/2),  # Bottom right
            (self.x + self.width/4, self.y),                  # Middle right
            (self.x, self.y - self.height/2),                 # Top
            (self.x - self.width/4, self.y),                  # Middle left
        ]
        
        # Rotate points around center
        center = (self.x, self.y)
        angle_rad = math.radians(self.angle)
        rotated_points = []
        for px, py in points:
            dx = px - center[0]
            dy = py - center[1]
            rotated_x = dx * math.cos(angle_rad) - dy * math.sin(angle_rad) + center[0]
            rotated_y = dx * math.sin(angle_rad) + dy * math.cos(angle_rad) + center[1]
            rotated_points.append((rotated_x, rotated_y))

        # Draw the spacecraft
        pygame.draw.polygon(screen, WHITE, rotated_points)
        pygame.draw.polygon(screen, BLUE, rotated_points, 2)

        # Draw landing legs when close to ground or landed
        ground_y = WINDOW_HEIGHT - self.current_planet.surface_height if hasattr(self, 'current_planet') else WINDOW_HEIGHT - 150
        if self.y + self.height/2 >= ground_y - 100 or self.landed:
            leg_length = 15
            left_leg_start = rotated_points[0]  # Bottom left point
            right_leg_start = rotated_points[1]  # Bottom right point
            
            # Left leg
            left_leg_end = (left_leg_start[0] - 10, left_leg_start[1] + leg_length)
            pygame.draw.line(screen, BLUE, left_leg_start, left_leg_end, 2)
            
            # Right leg
            right_leg_end = (right_leg_start[0] + 10, right_leg_start[1] + leg_length)
            pygame.draw.line(screen, BLUE, right_leg_start, right_leg_end, 2)

        # Draw thrust flame when thrusting
        if self.is_thrusting and self.fuel > 0 and not self.landed:
            flame_points = [
                (self.x - self.width/4, self.y + self.height/2),
                (self.x + self.width/4, self.y + self.height/2),
                (self.x, self.y + self.height/2 + 20)
            ]
            # Rotate flame points
            rotated_flame = []
            for px, py in flame_points:
                dx = px - center[0]
                dy = py - center[1]
                rotated_x = dx * math.cos(angle_rad) - dy * math.sin(angle_rad) + center[0]
                rotated_y = dx * math.sin(angle_rad) + dy * math.cos(angle_rad) + center[1]
                rotated_flame.append((rotated_x, rotated_y))
            pygame.draw.polygon(screen, ORANGE, rotated_flame)

        # Draw parachute if deployed
        if self.parachute_deployed and not self.landed:
            parachute_top = (self.x, self.y - self.height)
            parachute_left = (self.x - self.width, self.y - self.height/2)
            parachute_right = (self.x + self.width, self.y - self.height/2)
            pygame.draw.polygon(screen, RED, [parachute_left, parachute_top, parachute_right])

    def draw_wind_indicator(self, screen, planet):
        if not planet.has_atmosphere:
            return
            
        # Draw wind direction and strength
        wind_x = 20
        wind_y = 140
        wind_length = abs(planet.wind_force) * 200
        wind_color = GREEN if abs(planet.wind_force) < 0.1 else (YELLOW if abs(planet.wind_force) < 0.2 else RED)
        
        # Draw wind arrow
        if planet.wind_force != 0:
            direction = 1 if planet.wind_force > 0 else -1
            pygame.draw.line(screen, wind_color, 
                           (wind_x, wind_y),
                           (wind_x + wind_length * direction, wind_y), 3)
            # Arrow head
            pygame.draw.polygon(screen, wind_color, [
                (wind_x + wind_length * direction, wind_y),
                (wind_x + wind_length * direction - 10 * direction, wind_y - 5),
                (wind_x + wind_length * direction - 10 * direction, wind_y + 5)
            ])

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Mission to Touch Down")
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        
        # Define available planets
        self.planets = [
            Planet("Moon", 1.62, False),
            Planet("Mars", 3.72, True),
            Planet("Earth", 9.81, True),
            Planet("Europa", 1.315, False),
            Planet("Mystery Planet X", 0, False)  # Gravity will be randomized
        ]
        self.selected_planet_index = 0
        self.current_planet = self.planets[self.selected_planet_index]
        self.spacecraft = Spacecraft(WINDOW_WIDTH//4, 100)  # Start from left side
        
        # Load sounds
        self.thrust_sound = None
        self.crash_sound = None
        self.victory_sound = None
        self.load_sounds()

    def load_sounds(self):
        try:
            self.thrust_sound = pygame.mixer.Sound("assets/thrust.wav")
            self.crash_sound = pygame.mixer.Sound("assets/crash.wav")
            self.victory_sound = pygame.mixer.Sound("assets/victory.wav")
        except:
            print("Warning: Sound files not found")

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == GameState.MENU:
                        self.state = GameState.PLANET_SELECT
                    elif self.state == GameState.PLANET_SELECT:
                        self.state = GameState.PLAYING
                        self.current_planet = self.planets[self.selected_planet_index]
                        self.spacecraft = Spacecraft(WINDOW_WIDTH//4, 100)
                    elif self.state == GameState.PLAYING:
                        self.spacecraft.parachute_deployed = True
                    elif self.state in [GameState.VICTORY, GameState.GAME_OVER]:
                        self.state = GameState.PLANET_SELECT
                        self.spacecraft = Spacecraft(WINDOW_WIDTH//4, 100)
                elif event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLANET_SELECT:
                        self.state = GameState.MENU
                    else:
                        return False
                elif self.state == GameState.PLANET_SELECT:
                    if event.key == pygame.K_LEFT:
                        self.selected_planet_index = (self.selected_planet_index - 1) % len(self.planets)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_planet_index = (self.selected_planet_index + 1) % len(self.planets)
                    
        if self.state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            self.spacecraft.is_thrusting = keys[pygame.K_UP]
            self.spacecraft.moving_left = keys[pygame.K_LEFT]
            self.spacecraft.moving_right = keys[pygame.K_RIGHT]
            
        return True

    def update(self):
        if self.state == GameState.PLAYING:
            self.spacecraft.apply_thrust()
            landing_status = self.spacecraft.update(self.current_planet)
            
            # Check if we've landed or crashed
            if landing_status is not None:  # We've hit the ground
                if landing_status:  # Safe landing
                    self.state = GameState.VICTORY
                    if self.victory_sound:
                        self.victory_sound.play()
                else:  # Crash
                    self.state = GameState.GAME_OVER
                    if self.crash_sound:
                        self.crash_sound.play()

    def draw_menu(self):
        self.screen.fill(BLACK)
        
        # Draw title
        font_big = pygame.font.Font(None, 74)
        font = pygame.font.Font(None, 36)
        
        title = font_big.render("Mission to Touch Down", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH/2, 150))
        self.screen.blit(title, title_rect)
        
        # Draw instructions
        instructions = [
            "Welcome to Space Landing Training!",
            "",
            "Your Mission:",
            "Land the spacecraft safely on the landing pad",
            "",
            "Controls:",
            "↑ UP ARROW = Fire main engine",
            "← LEFT ARROW = Move left",
            "→ RIGHT ARROW = Move right",
            "SPACE = Deploy parachute (when in atmosphere)",
            "",
            "For a safe landing you need:",
            "- Land slowly (watch your speed!)",
            "- Land precisely on the pad",
            "- Don't run out of fuel!",
            "",
            "Press SPACE to Start",
            "Press ESC to Quit"
        ]
        
        y = 250
        for line in instructions:
            text = font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH/2, y))
            self.screen.blit(text, text_rect)
            y += 30

    def draw_game_over(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        font_big = pygame.font.Font(None, 74)
        text = font_big.render("CRASH!", True, RED)
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50))
        self.screen.blit(text, text_rect)
        
        # Add crash details
        font = pygame.font.Font(None, 36)
        if self.spacecraft.velocity_y >= 2:
            detail = "Vertical speed too high!"
        elif self.spacecraft.velocity_x >= 1:
            detail = "Horizontal speed too high!"
        else:
            detail = "Missed the landing pad!"
        
        detail_text = font.render(detail, True, YELLOW)
        detail_rect = detail_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.screen.blit(detail_text, detail_rect)
        
        text = font.render("Press SPACE to Try Again", True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50))
        self.screen.blit(text, text_rect)

    def draw_victory(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        font_big = pygame.font.Font(None, 74)
        text = font_big.render("PERFECT LANDING!", True, GREEN)
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50))
        self.screen.blit(text, text_rect)
        
        # Add landing stats
        font = pygame.font.Font(None, 36)
        stats = f"Final Speed: {abs(self.spacecraft.velocity_y):.1f} m/s"
        stats_text = font.render(stats, True, GREEN)
        stats_rect = stats_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.screen.blit(stats_text, stats_rect)
        
        # Only show "Press SPACE" after landing effect is done
        if self.spacecraft.landing_effect_timer <= 0:
            text = font.render("Press SPACE to Play Again", True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50))
            self.screen.blit(text, text_rect)

    def draw_controls_reminder(self):
        font = pygame.font.Font(None, 24)
        controls = [
            "↑: Thrust",
            "←→: Move",
            "Space: Parachute"
        ]
        y = WINDOW_HEIGHT - 100
        for control in controls:
            text = font.render(control, True, WHITE)
            self.screen.blit(text, (WINDOW_WIDTH - 120, y))
            y += 25

    def draw_planet_select(self):
        self.screen.fill(BLACK)
        
        # Draw title
        font_big = pygame.font.Font(None, 74)
        font = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)
        
        title = font_big.render("Select Your Landing Site", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH/2, 100))
        self.screen.blit(title, title_rect)

        # Draw planet preview
        planet = self.planets[self.selected_planet_index]
        
        # Draw planet name
        name_text = font_big.render(planet.name, True, WHITE)
        name_rect = name_text.get_rect(center=(WINDOW_WIDTH/2, 200))
        self.screen.blit(name_text, name_rect)
        
        # Draw planet description
        y = 250
        for line in planet.description.split('\n'):
            desc_text = font.render(line, True, WHITE)
            desc_rect = desc_text.get_rect(center=(WINDOW_WIDTH/2, y))
            self.screen.blit(desc_text, desc_rect)
            y += 40

        # Draw navigation arrows and instructions
        if self.selected_planet_index > 0:
            left_arrow = font_big.render("←", True, WHITE)
            self.screen.blit(left_arrow, (50, WINDOW_HEIGHT/2))
        
        if self.selected_planet_index < len(self.planets) - 1:
            right_arrow = font_big.render("→", True, WHITE)
            self.screen.blit(right_arrow, (WINDOW_WIDTH - 80, WINDOW_HEIGHT/2))

        # Draw preview of the planet
        preview_surface = pygame.Surface((400, 200))
        preview_surface.fill(BLACK)
        if planet.atmosphere_color:
            atmosphere = pygame.Surface((400, 200))
            atmosphere.fill(planet.atmosphere_color[:3])  # Remove alpha
            atmosphere.set_alpha(50)
            preview_surface.blit(atmosphere, (0, 0))
        pygame.draw.rect(preview_surface, planet.surface_color, (0, 150, 400, 50))
        
        # Add some surface details
        for i in range(5):
            x = random.randint(0, 400)
            pygame.draw.circle(preview_surface, (min(255, planet.surface_color[0] - 30),
                                              min(255, planet.surface_color[1] - 30),
                                              min(255, planet.surface_color[2] - 30)),
                             (x, 160 + random.randint(0, 20)), random.randint(5, 10))
        
        preview_rect = preview_surface.get_rect(center=(WINDOW_WIDTH/2, 450))
        self.screen.blit(preview_surface, preview_rect)

        # Draw instructions
        instructions = [
            "← → Arrow Keys: Change Planet",
            "SPACE: Start Mission",
            "ESC: Back to Menu"
        ]
        
        y = WINDOW_HEIGHT - 150
        for instruction in instructions:
            inst_text = font_small.render(instruction, True, WHITE)
            inst_rect = inst_text.get_rect(center=(WINDOW_WIDTH/2, y))
            self.screen.blit(inst_text, inst_rect)
            y += 30

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw stars
        for _ in range(100):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            pygame.draw.circle(self.screen, WHITE, (x, y), 1)

        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLANET_SELECT:
            self.draw_planet_select()
        else:
            # Draw planet
            self.current_planet.draw(self.screen)
            
            # Draw spacecraft
            self.spacecraft.draw(self.screen)

            # Draw HUD
            self.draw_hud()
            
            # Draw controls reminder
            self.draw_controls_reminder()

            if self.state == GameState.GAME_OVER:
                self.draw_game_over()
            elif self.state == GameState.VICTORY:
                self.draw_victory()

        pygame.display.flip()

    def draw_hud(self):
        # Background for HUD
        pygame.draw.rect(self.screen, (0, 0, 0, 128), (10, 10, 200, 160))
        
        # Draw altitude
        altitude = WINDOW_HEIGHT - self.current_planet.surface_height - self.spacecraft.y
        font = pygame.font.Font(None, 36)
        altitude_text = font.render(f"Height: {int(altitude)}m", True, WHITE)
        self.screen.blit(altitude_text, (20, 20))

        # Draw velocity with color feedback
        velocity = math.sqrt(self.spacecraft.velocity_x**2 + self.spacecraft.velocity_y**2)
        color = GREEN if velocity < 2 else (YELLOW if velocity < 4 else RED)
        velocity_text = font.render(f"Speed: {abs(velocity):.1f} m/s", True, color)
        self.screen.blit(velocity_text, (20, 60))

        # Draw horizontal velocity
        h_vel_color = GREEN if abs(self.spacecraft.velocity_x) < 1 else (YELLOW if abs(self.spacecraft.velocity_x) < 2 else RED)
        h_velocity_text = font.render(f"H-Speed: {abs(self.spacecraft.velocity_x):.1f} m/s", True, h_vel_color)
        self.screen.blit(h_velocity_text, (20, 100))

        # Draw fuel with color feedback
        fuel_color = GREEN if self.spacecraft.fuel > 50 else (YELLOW if self.spacecraft.fuel > 25 else RED)
        fuel_text = font.render(f"Fuel: {int(self.spacecraft.fuel)}%", True, fuel_color)
        self.screen.blit(fuel_text, (20, 140))

        # Draw wind indicator
        self.spacecraft.draw_wind_indicator(self.screen, self.current_planet)

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run() 