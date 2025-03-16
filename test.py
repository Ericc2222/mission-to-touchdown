import os
import sys
import tkinter as tk
from tkinter import messagebox

# Suppress deprecation warning
os.environ['TK_SILENCE_DEPRECATION'] = '1'

def main():
    try:
        # Print Python version and Tkinter information
        print(f"Python version: {sys.version}")
        print(f"Tkinter version: {tk.TkVersion}")
        
        # Create the main window
        root = tk.Tk()
        root.title("Tkinter Test")
        
        # Configure window
        root.geometry("400x300")
        root.configure(bg='black')
        
        # Add widgets
        label = tk.Label(
            root,
            text="Tkinter is working!",
            fg="yellow",
            bg="black",
            font=("Arial", 24)
        )
        label.pack(pady=50)
        
        # Add a button
        button = tk.Button(
            root,
            text="Click me!",
            command=lambda: messagebox.showinfo("Hello", "Button clicked!"),
            bg="yellow",
            fg="black"
        )
        button.pack(pady=20)
        
        # Add quit button
        quit_button = tk.Button(
            root,
            text="Quit",
            command=root.destroy,
            bg="red",
            fg="white"
        )
        quit_button.pack(pady=20)
        
        print("Window created successfully. You should see it now.")
        print(f"Window size: {root.winfo_width()}x{root.winfo_height()}")
        print(f"Window position: ({root.winfo_x()}, {root.winfo_y()})")
        
        # Start the event loop
        root.mainloop()
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 