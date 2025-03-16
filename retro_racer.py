import tkinter as tk
import math

class RetroRacer:
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("Retro Racer")
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            width=600,
            height=400,
            bg='black'
        )
        self.canvas.pack()
        
        # Game variables
        self.car_x = 300
        self.car_y = 300
        self.car_angle = 0
        self.speed = 0
        
        # Create track
        self.outer_track = self.canvas.create_oval(
            100, 50,
            500, 350,
            outline='white',
            width=2
        )
        
        self.inner_track = self.canvas.create_oval(
            200, 100,
            400, 300,
            outline='white',
            width=2
        )
        
        # Create car
        self.create_car()
        
        # Create status text
        self.status = self.canvas.create_text(
            300, 30,
            text="Use ARROW KEYS to drive!",
            fill='yellow',
            font=('Arial', 16, 'bold')
        )
        
        # Bind keys
        self.root.bind('<Left>', self.turn_left)
        self.root.bind('<Right>', self.turn_right)
        self.root.bind('<Up>', self.accelerate)
        self.root.bind('<Down>', self.brake)
        self.root.bind('<space>', self.reset_game)
        self.root.bind('<Escape>', lambda e: self.root.quit())

    def create_car(self):
        # Delete existing car if any
        if hasattr(self, 'car'):
            self.canvas.delete(self.car)
        
        # Calculate car points
        angle = math.radians(self.car_angle)
        points = [
            self.car_x - 10 * math.cos(angle) - 5 * math.sin(angle),
            self.car_y - 10 * math.sin(angle) + 5 * math.cos(angle),
            self.car_x + 10 * math.cos(angle) - 5 * math.sin(angle),
            self.car_y + 10 * math.sin(angle) + 5 * math.cos(angle),
            self.car_x + 15 * math.sin(angle),
            self.car_y - 15 * math.cos(angle)
        ]
        
        # Create car triangle
        self.car = self.canvas.create_polygon(
            points,
            fill='red',
            outline='yellow'
        )

    def turn_left(self, event):
        if self.speed != 0:
            self.car_angle += 5
            self.create_car()

    def turn_right(self, event):
        if self.speed != 0:
            self.car_angle -= 5
            self.create_car()

    def accelerate(self, event):
        self.speed = min(self.speed + 0.5, 5.0)
        self.move_car()

    def brake(self, event):
        self.speed = max(self.speed - 0.5, -2.0)
        self.move_car()

    def move_car(self):
        if self.speed != 0:
            angle = math.radians(self.car_angle)
            self.car_x += math.sin(angle) * self.speed
            self.car_y -= math.cos(angle) * self.speed
            
            # Check track boundaries
            if self.check_collision():
                self.game_over()
            else:
                self.create_car()
                # Schedule next movement
                self.root.after(50, self.move_car)

    def check_collision(self):
        # Get car position
        car_pos = self.canvas.coords(self.car)
        if not car_pos:
            return False
        
        # Calculate center point
        center_x = sum(car_pos[::2]) / 3
        center_y = sum(car_pos[1::2]) / 3
        
        # Check if outside track
        distance_from_center = math.sqrt((center_x - 300)**2 + (center_y - 200)**2)
        return distance_from_center < 50 or distance_from_center > 250

    def game_over(self):
        self.speed = 0
        self.canvas.itemconfig(
            self.status,
            text="GAME OVER! Press SPACE to restart",
            fill='red',
            font=('Arial', 16, 'bold')
        )

    def reset_game(self, event=None):
        self.car_x = 300
        self.car_y = 300
        self.car_angle = 0
        self.speed = 0
        self.create_car()
        self.canvas.itemconfig(
            self.status,
            text="Use ARROW KEYS to drive!",
            fill='yellow',
            font=('Arial', 16, 'bold')
        )

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = RetroRacer()
    game.run() 