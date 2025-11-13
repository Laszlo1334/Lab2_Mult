"""
Desktop Media Player Application
A simple media player using Tkinter and VLC
"""

import tkinter as tk
from tkinter import Menu, Scale, Label, Button, Frame
from tkinter import filedialog, simpledialog, messagebox
import vlc
import sys
import platform


class MediaPlayer:
    """Main media player application class"""
    
    def __init__(self, root):
        """Initialize the media player window and UI elements"""
        self.root = root
        self.root.title("Media Player")
        self.root.geometry("800x600")
        
        try:
            # Initialize VLC instance and player
            self.instance = vlc.Instance()
            self.player = self.instance.media_player_new()
        except Exception as e:
            messagebox.showerror(
                "VLC Error",
                f"Failed to initialize VLC. Please ensure VLC is installed on your system.\nError: {str(e)}"
            )
            sys.exit(1)
        
        # Media state variables
        self.is_playing = False
        self.current_media = None
        self.is_slider_being_dragged = False
        
        # Create menu bar
        self.create_menu()
        
        # Create video frame (placeholder for video display)
        self.video_frame = Frame(self.root, bg="black", width=800, height=450)
        self.video_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bind video output to the frame
        self.setup_video_output()
        
        # Create control panel
        self.create_controls()
        
        # Start periodic UI updates
        self.update_ui()
        
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
        
    def setup_video_output(self):
        """Set up the video output to display in the Tkinter frame"""
        # Get window ID for embedding video
        if platform.system() == "Windows":
            self.player.set_hwnd(self.video_frame.winfo_id())
        elif platform.system() == "Darwin":  # macOS
            self.player.set_nsobject(self.video_frame.winfo_id())
        else:  # Linux
            self.player.set_xwindow(self.video_frame.winfo_id())
        
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
        
        # Bind slider press and release events
        self.progress_slider.bind("<ButtonPress-1>", self.on_slider_press)
        self.progress_slider.bind("<ButtonRelease-1>", self.on_slider_release)
        
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
        file_path = filedialog.askopenfilename(
            title="Select Media File",
            filetypes=[
                ("All Media Files", "*.mp3 *.mp4 *.avi *.mkv *.wav *.flac *.mov"),
                ("Audio Files", "*.mp3 *.wav *.flac"),
                ("Video Files", "*.mp4 *.avi *.mkv *.mov"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.load_media(file_path)
            
    def load_media(self, source):
        """Load media from file path or URL"""
        try:
            # Create media object
            self.current_media = self.instance.media_new(source)
            
            if not self.current_media:
                raise Exception("Failed to create media object")
                
            self.player.set_media(self.current_media)
            
            # Reset UI state
            self.is_playing = False
            self.play_pause_button.config(text="▶ Play")
            self.current_time_label.config(text="00:00")
            self.total_time_label.config(text="00:00")
            self.progress_slider.set(0)
            
            # Show success message only for files (not streams, to avoid dialog spam)
            if not source.startswith(('http://', 'https://', 'rtsp://', 'mms://')):
                messagebox.showinfo("Success", "Media loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load media: {str(e)}")
        
    def open_stream(self):
        """Open dialog to input stream URL"""
        url = simpledialog.askstring(
            "Open Stream",
            "Enter the URL of the media stream:\n(e.g., http://example.com/stream.m3u8)",
            parent=self.root
        )
        
        if url and url.strip():
            self.load_media(url.strip())
        elif url is not None:  # User entered empty string
            messagebox.showwarning("Invalid URL", "Please enter a valid URL")
        
    def toggle_play_pause(self):
        """Toggle between play and pause"""
        if not self.current_media:
            messagebox.showwarning("No Media", "Please load a media file first")
            return
            
        if self.is_playing:
            # Pause playback
            self.player.pause()
            self.is_playing = False
            self.play_pause_button.config(text="▶ Play")
        else:
            # Start or resume playback
            self.player.play()
            self.is_playing = True
            self.play_pause_button.config(text="⏸ Pause")
        
    def stop_playback(self):
        """Stop playback and reset to beginning"""
        if self.player:
            self.player.stop()
            self.is_playing = False
            self.play_pause_button.config(text="▶ Play")
            self.current_time_label.config(text="00:00")
            self.progress_slider.set(0)
        
    def skip_backward(self):
        """Skip backward 10 seconds"""
        if not self.current_media:
            return
            
        current_time = self.player.get_time()
        if current_time > 0:
            # Go back 10 seconds (10000 milliseconds)
            new_time = max(0, current_time - 10000)
            self.player.set_time(new_time)
        
    def skip_forward(self):
        """Skip forward 10 seconds"""
        if not self.current_media:
            return
            
        current_time = self.player.get_time()
        duration = self.player.get_length()
        
        if duration > 0 and current_time < duration:
            # Go forward 10 seconds (10000 milliseconds)
            new_time = min(duration, current_time + 10000)
            self.player.set_time(new_time)
        
    def on_slider_change(self, value):
        """Handle slider position change by user"""
        # Only seek if user is dragging the slider
        if self.is_slider_being_dragged and self.current_media:
            duration = self.player.get_length()
            if duration > 0:
                new_time = int((float(value) / 100) * duration)
                self.player.set_time(new_time)
                
    def on_slider_press(self, event):
        """Handle slider press event"""
        self.is_slider_being_dragged = True
        
    def on_slider_release(self, event):
        """Handle slider release event"""
        self.is_slider_being_dragged = False
        # Update position when slider is released
        if self.current_media:
            value = self.progress_slider.get()
            duration = self.player.get_length()
            if duration > 0:
                new_time = int((float(value) / 100) * duration)
                self.player.set_time(new_time)
                
    def format_time(self, milliseconds):
        """Format time from milliseconds to MM:SS"""
        if milliseconds < 0:
            return "00:00"
        seconds = int(milliseconds / 1000)
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
        
    def update_ui(self):
        """Periodically update the UI (slider and time labels)"""
        try:
            if self.current_media and not self.is_slider_being_dragged:
                # Get current playback position
                current_time = self.player.get_time()
                duration = self.player.get_length()
                
                if duration > 0:
                    # Update slider position
                    position = (current_time / duration) * 100
                    self.progress_slider.set(position)
                    
                    # Update time labels
                    self.current_time_label.config(text=self.format_time(current_time))
                    self.total_time_label.config(text=self.format_time(duration))
        except Exception:
            # Silently handle any errors in UI update to prevent crashes
            pass
        
        # Schedule next update (every 500ms)
        self.root.after(500, self.update_ui)


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    player = MediaPlayer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
