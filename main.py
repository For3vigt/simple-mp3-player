import tkinter as tk
from tkinter import filedialog
import sqlite3
import pygame
import os.path

conn = sqlite3.connect('samples.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS samples (id INTEGER PRIMARY KEY, filename TEXT)''')

# Keep track of all sample file paths for keyboard shortcuts
sample_files = []

def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def stop_sound():
    pygame.mixer.music.stop()

def create_styled_button(parent, text, command, shortcut_num=None):
    """Create a styled square button with optional shortcut indicator"""
    button_text = text
    if shortcut_num is not None:
        button_text = f"[{shortcut_num}] {text}"
        
    button = tk.Button(
        parent,
        text=button_text,
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
        
        # Add to our list of samples for keyboard shortcuts
        sample_files.append(file_path)
        shortcut_num = len(sample_files)
        
        button = create_styled_button(
            samples_frame,
            text=f"{filename}",
            command=lambda path=file_path: play_sound(path),
            shortcut_num=shortcut_num
        )
        button.pack(side=tk.LEFT, padx=15, pady=15)

        cursor.execute("INSERT INTO samples (filename) VALUES (?)", (file_path,))
        conn.commit()

def load_samples():
    cursor.execute("SELECT filename FROM samples")
    sample_files.clear()  # Clear existing samples
    
    for row in cursor.fetchall():
        file_path = row[0]
        # Add to our list of samples for keyboard shortcuts
        sample_files.append(file_path)
        shortcut_num = len(sample_files)
        
        # Get just the filename for display
        filename = os.path.basename(file_path)
        
        button = create_styled_button(
            samples_frame, 
            text=f"{filename}",
            command=lambda path=file_path: play_sound(path),
            shortcut_num=shortcut_num
        )
        button.pack(side=tk.LEFT, padx=15, pady=15)

def handle_key_press(event):
    # Check if the pressed key is a number and within our sample range
    if event.char.isdigit() and int(event.char) > 0:
        index = int(event.char) - 1  # Convert to 0-based index
        if index < len(sample_files):
            play_sound(sample_files[index])

window = tk.Tk()
window.title("MP3 Speler")
window.configure(bg="#2c2c2c")  # Dark background

# Bind keyboard events
window.bind("<KeyPress>", handle_key_press)

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

# Load existing samples
load_samples()

window.mainloop()

conn.close()