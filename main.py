"""
Desktop Media Player Application
A simple media player using Tkinter and VLC
"""

import tkinter as tk
from tkinter import Menu, Scale, Label, Button, Frame
from tkinter import filedialog, simpledialog, messagebox


class MediaPlayer:
    """Main media player application class"""
    
    def __init__(self, root):
        """Initialize the media player window and UI elements"""
        self.root = root
        self.root.title("Media Player")
        self.root.geometry("800x600")
        
        # Create menu bar
        self.create_menu()
        
        # Create video frame (placeholder for video display)
        self.video_frame = Frame(self.root, bg="black", width=800, height=450)
        self.video_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create control panel
        self.create_controls()
        
    def create_menu(self):
        """Create the menu bar with File menu"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open File...", command=self.open_file)
        file_menu.add_command(label="Open Stream...", command=self.open_stream)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
    def create_controls(self):
        """Create control buttons, slider, and time labels"""
        # Control frame
        control_frame = Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Time labels frame
        time_frame = Frame(control_frame)
        time_frame.pack(fill=tk.X)
        
        # Current time label
        self.current_time_label = Label(time_frame, text="00:00", width=10)
        self.current_time_label.pack(side=tk.LEFT)
        
        # Progress slider
        self.progress_slider = Scale(
            time_frame, 
            from_=0, 
            to=100, 
            orient=tk.HORIZONTAL,
            showvalue=0,
            command=self.on_slider_change
        )
        self.progress_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Total time label
        self.total_time_label = Label(time_frame, text="00:00", width=10)
        self.total_time_label.pack(side=tk.RIGHT)
        
        # Buttons frame
        button_frame = Frame(control_frame)
        button_frame.pack(pady=10)
        
        # Back button
        self.back_button = Button(
            button_frame, 
            text="⏮ Back", 
            width=10,
            command=self.skip_backward
        )
        self.back_button.pack(side=tk.LEFT, padx=5)
        
        # Play/Pause button
        self.play_pause_button = Button(
            button_frame, 
            text="▶ Play", 
            width=10,
            command=self.toggle_play_pause
        )
        self.play_pause_button.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        self.stop_button = Button(
            button_frame, 
            text="⏹ Stop", 
            width=10,
            command=self.stop_playback
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Forward button
        self.forward_button = Button(
            button_frame, 
            text="Forward ⏭", 
            width=10,
            command=self.skip_forward
        )
        self.forward_button.pack(side=tk.LEFT, padx=5)
        
    def open_file(self):
        """Open file dialog to select a media file"""
        # Placeholder - will be implemented in Step 2
        messagebox.showinfo("Not Implemented", "File opening will be implemented in Step 2")
        
    def open_stream(self):
        """Open dialog to input stream URL"""
        # Placeholder - will be implemented in Step 5
        messagebox.showinfo("Not Implemented", "Stream opening will be implemented in Step 5")
        
    def toggle_play_pause(self):
        """Toggle between play and pause"""
        # Placeholder - will be implemented in Step 3
        pass
        
    def stop_playback(self):
        """Stop playback and reset to beginning"""
        # Placeholder - will be implemented in Step 3
        pass
        
    def skip_backward(self):
        """Skip backward 10 seconds"""
        # Placeholder - will be implemented in Step 3
        pass
        
    def skip_forward(self):
        """Skip forward 10 seconds"""
        # Placeholder - will be implemented in Step 3
        pass
        
    def on_slider_change(self, value):
        """Handle slider position change by user"""
        # Placeholder - will be implemented in Step 4
        pass


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    player = MediaPlayer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
