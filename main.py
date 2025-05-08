import tkinter as tk
from tkinter import filedialog
import sqlite3
import pygame
import os.path  # Add this import for path handling

conn = sqlite3.connect('samples.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS samples (id INTEGER PRIMARY KEY, filename TEXT)''')

def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def stop_sound():
    pygame.mixer.music.stop()

def create_styled_button(parent, text, command):
    """Create a styled square button"""
    button = tk.Button(
        parent,
        text=text,
        command=command,
        width=26,         # Fixed width
        height=14,         # Fixed height
        bg="#4a6cd4",     # Background color
        fg="white",       # Text color
        font=("Arial", 11),
        relief=tk.RAISED,
        borderwidth=3,
        wraplength=150,  # Wrap text if too long
    )
    return button

def add_file():
    if file_path := filedialog.askopenfilename(
        filetypes=[("MP3 files", "*.mp3")]
    ):
        # Get just the filename for display
        filename = os.path.basename(file_path)
        
        button = create_styled_button(
            samples_frame,
            text=f"{filename}",
            command=lambda path=file_path: play_sound(path)
        )
        button.pack(side=tk.LEFT, padx=15, pady=15)

        cursor.execute("INSERT INTO samples (filename) VALUES (?)", (file_path,))
        conn.commit()

def load_samples():
    cursor.execute("SELECT filename FROM samples")
    for row in cursor.fetchall():
        file_path = row[0]
        # Get just the filename for display
        filename = os.path.basename(file_path)
        
        button = create_styled_button(
            samples_frame, 
            text=f"{filename}",
            command=lambda path=file_path: play_sound(path)
        )
        button.pack(side=tk.LEFT, padx=15, pady=15)

window = tk.Tk()
window.title("MP3 Speler")
window.configure(bg="#2c2c2c")  # Dark background

# Create a frame for control buttons
control_frame = tk.Frame(window, bg="#2c2c2c")
control_frame.pack(pady=10)

# Create a frame for sample buttons
samples_frame = tk.Frame(window, bg="#2c2c2c")
samples_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

add_button = tk.Button(window, text="Voeg bestand toe", command=add_file)
add_button.pack()

stop_button = tk.Button(window, text="Stop", command=stop_sound)
stop_button.pack()
load_samples()

window.mainloop()

conn.close()