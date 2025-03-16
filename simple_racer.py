import os
import tkinter as tk
import math

# Suppress deprecation warning
os.environ['TK_SILENCE_DEPRECATION'] = '1'

class SimpleRacer:
    def __init__(self):
        print("Initializing window...")
        self.window = tk.Tk()
        self.window.title("Simple Racer")
        self.window.configure(bg='black')  # Set window background
        
        # Create canvas with fixed size
        print("Creating canvas...")
        self.canvas = tk.Canvas(
            self.window,
            width=600,
            height=400,
            bg='black',
            highlightthickness=0  # Remove border
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Add debug text
        self.debug_text = self.canvas.create_text(
            300, 20,
            text="Game Running",
            fill="green",
            font=("Arial", 14)
        )
        
        # Car properties
        self.car_x = 300
        self.car_y = 300
        self.car_angle = 0
        self.speed = 0
        
        print("Creating game elements...")
        # Create track
        self.create_track()
        # Create car
        self.create_car()
        
        print("Binding controls...")
        # Bind keys
        self.window.bind('<Up>', lambda e: self.set_speed(2))
        self.window.bind('<Down>', lambda e: self.set_speed(-2))
        self.window.bind('<Left>', lambda e: self.turn(-5))
        self.window.bind('<Right>', lambda e: self.turn(5))
        self.window.bind('<KeyRelease>', lambda e: self.set_speed(0))
        self.window.bind('<Escape>', lambda e: self.window.destroy())
        
        # Force window to front and set minimum size
        print("Configuring window properties...")
        self.window.lift()
        self.window.attributes('-topmost', True)
        self.window.minsize(620, 420)
        
        # Start game loop
        print("Starting game loop...")
        self.update()
        self.window.mainloop()
    
    def create_track(self):
        # Simple oval track
        self.track = self.canvas.create_oval(
            50, 50,
            550, 350,
            outline='white',
            width=3  # Make track more visible
        )
    
    def create_car(self):
        self.car = self.canvas.create_polygon(
            self.car_x, self.car_y-10,
            self.car_x-5, self.car_y+10,
            self.car_x+5, self.car_y+10,
            fill='red',
            outline='yellow',
            width=2  # Make car outline more visible
        )
    
    def set_speed(self, speed):
        self.speed = speed
        # Update debug text
        self.canvas.itemconfig(
            self.debug_text,
            text=f"Speed: {speed}"
        )
    
    def turn(self, angle):
        self.car_angle += angle
    
    def update(self):
        try:
            # Move car
            self.car_x += math.sin(math.radians(self.car_angle)) * self.speed
            self.car_y -= math.cos(math.radians(self.car_angle)) * self.speed
            
            # Update car position
            points = [
                self.car_x, self.car_y-10,
                self.car_x-5, self.car_y+10,
                self.car_x+5, self.car_y+10
            ]
            
            # Rotate points
            center_x = self.car_x
            center_y = self.car_y
            rotated_points = []
            for i in range(0, len(points), 2):
                x = points[i] - center_x
                y = points[i+1] - center_y
                rotated_x = x * math.cos(math.radians(self.car_angle)) - y * math.sin(math.radians(self.car_angle))
                rotated_y = x * math.sin(math.radians(self.car_angle)) + y * math.cos(math.radians(self.car_angle))
                rotated_points.extend([rotated_x + center_x, rotated_y + center_y])
            
            self.canvas.coords(self.car, *rotated_points)
            
            # Schedule next update
            self.window.after(16, self.update)  # About 60 FPS
        except Exception as e:
            print(f"Error in update: {str(e)}")

if __name__ == "__main__":
    print("Starting Simple Racer...")
    print("Controls:")
    print("Arrow keys to move")
    print("Escape to quit")
    game = SimpleRacer() 