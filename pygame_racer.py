import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Track parameters
TRACK_WIDTH = 80
CIRCLE_RADIUS = 120
CIRCLE_OFFSET = 100

# Car parameters
CAR_LENGTH = 20
CAR_WIDTH = 10
MIN_SPEED = 2.0
MAX_SPEED = 4.0
ACCELERATION = 0.1
TURN_SPEED = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # Angle in degrees
        self.speed = MIN_SPEED
        
    def get_corners(self):
        # Calculate the four corners of the car
        cos_angle = math.cos(math.radians(self.angle))
        sin_angle = math.sin(math.radians(self.angle))
        
        # Front corners
        front_left = (
            self.x + CAR_LENGTH/2 * sin_angle - CAR_WIDTH/2 * cos_angle,
            self.y - CAR_LENGTH/2 * cos_angle - CAR_WIDTH/2 * sin_angle
        )
        front_right = (
            self.x + CAR_LENGTH/2 * sin_angle + CAR_WIDTH/2 * cos_angle,
            self.y - CAR_LENGTH/2 * cos_angle + CAR_WIDTH/2 * sin_angle
        )
        
        # Back corners
        back_left = (
            self.x - CAR_LENGTH/2 * sin_angle - CAR_WIDTH/2 * cos_angle,
            self.y + CAR_LENGTH/2 * cos_angle - CAR_WIDTH/2 * sin_angle
        )
        back_right = (
            self.x - CAR_LENGTH/2 * sin_angle + CAR_WIDTH/2 * cos_angle,
            self.y + CAR_LENGTH/2 * cos_angle + CAR_WIDTH/2 * sin_angle
        )
        
        return [front_left, front_right, back_right, back_left]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Figure 8 Racer")
        self.clock = pygame.time.Clock()
        
        # Track centers
        self.center_x = WINDOW_WIDTH // 2
        self.center_y = WINDOW_HEIGHT // 2
        
        # Create car at starting position
        self.car = Car(self.center_x, self.center_y - CIRCLE_OFFSET)
        
    def is_point_in_track(self, x, y):
        # Check if point is within either circle of figure 8
        dist_top = math.sqrt((x - self.center_x)**2 + (y - (self.center_y - CIRCLE_OFFSET))**2)
        dist_bottom = math.sqrt((x - self.center_x)**2 + (y - (self.center_y + CIRCLE_OFFSET))**2)
        
        # Point is valid if it's within TRACK_WIDTH/2 of either circle's circumference
        in_top = abs(dist_top - CIRCLE_RADIUS) <= TRACK_WIDTH/2
        in_bottom = abs(dist_bottom - CIRCLE_RADIUS) <= TRACK_WIDTH/2
        
        return in_top or in_bottom
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Acceleration
        if keys[pygame.K_UP]:
            self.car.speed = min(self.car.speed + ACCELERATION, MAX_SPEED)
        elif keys[pygame.K_DOWN]:
            self.car.speed = max(self.car.speed - ACCELERATION, MIN_SPEED)
        
        # Turning
        if keys[pygame.K_LEFT]:
            self.car.angle += TURN_SPEED
        if keys[pygame.K_RIGHT]:
            self.car.angle -= TURN_SPEED
            
        # Keep angle in [0, 360)
        self.car.angle %= 360
    
    def update(self):
        # Calculate new position
        new_x = self.car.x + math.sin(math.radians(self.car.angle)) * self.car.speed
        new_y = self.car.y - math.cos(math.radians(self.car.angle)) * self.car.speed
        
        # Temporarily move car to check if new position would be valid
        old_x, old_y = self.car.x, self.car.y
        self.car.x, self.car.y = new_x, new_y
        corners = self.car.get_corners()
        self.car.x, self.car.y = old_x, old_y
        
        # Only update position if all corners would be within track
        if all(self.is_point_in_track(x, y) for x, y in corners):
            self.car.x = new_x
            self.car.y = new_y
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw track
        for offset in [-CIRCLE_OFFSET, CIRCLE_OFFSET]:
            # Draw outer circle
            pygame.draw.circle(self.screen, GRAY, 
                             (self.center_x, self.center_y + offset),
                             CIRCLE_RADIUS + TRACK_WIDTH/2)
            # Draw inner circle (black)
            pygame.draw.circle(self.screen, BLACK,
                             (self.center_x, self.center_y + offset),
                             CIRCLE_RADIUS - TRACK_WIDTH/2)
            # Draw track borders
            pygame.draw.circle(self.screen, WHITE,
                             (self.center_x, self.center_y + offset),
                             CIRCLE_RADIUS + TRACK_WIDTH/2, 2)
            pygame.draw.circle(self.screen, WHITE,
                             (self.center_x, self.center_y + offset),
                             CIRCLE_RADIUS - TRACK_WIDTH/2, 2)
        
        # Draw car
        corners = self.car.get_corners()
        pygame.draw.polygon(self.screen, RED, corners)
        pygame.draw.polygon(self.screen, WHITE, corners, 2)
        
        # Draw speed indicator
        font = pygame.font.Font(None, 36)
        speed_text = font.render(f"Speed: {self.car.speed:.1f}", True, WHITE)
        self.screen.blit(speed_text, (10, 10))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("Starting Figure 8 Racer...")
    print("Controls:")
    print("Up Arrow: Accelerate")
    print("Down Arrow: Decelerate")
    print("Left/Right Arrows: Turn")
    print("Escape: Quit")
    game = Game()
    game.run() 