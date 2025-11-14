import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Menu
import vlc
import os
from pathlib import Path


class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Медіаплеєр")
        self.root.geometry("800x600")
        self.root.configure(bg="#2b2b2b")

        # Ініціалізація VLC (БЕЗ ЗМІН - працює)
        try:
            self.instance = vlc.Instance()
            self.player = self.instance.media_player_new()
        except Exception as e:
            messagebox.showerror(
                "Помилка",
                "VLC media player не знайдено!\n\n"
                "Завантажте та встановіть VLC з:\n"
                "https://www.videolan.org/vlc/\n\n"
                f"Деталі помилки: {str(e)}"
            )
            self.root.quit()
            return

        # Змінні стану
        self.is_playing = False
        self.current_file = None
        self.is_user_seeking = False  # ← Вже є

        # Створення меню та віджетів
        self.create_menu()
        self.create_widgets()

        # Запуск оновлення прогресу
        self.update_progress()

    def create_menu(self):
        """Створення меню програми"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # Меню "Файл"
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Відкрити файл...", command=self.open_file)
        file_menu.add_command(label="Відкрити потік...", command=self.open_stream)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

    def create_widgets(self):
        """Створення GUI елементів"""
        # Фрейм для відео
        self.video_frame = tk.Frame(self.root, bg="black", height=400)
        self.video_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Прив'язка VLC до фрейму (Windows)
        self.player.set_hwnd(self.video_frame.winfo_id())

        # Повзунок прогресу
        self.progress_slider = tk.Scale(
            self.root,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.set_position,
            showvalue=0,
            bg="#3c3c3c",
            fg="white",
            troughcolor="#1c1c1c",
            highlightthickness=0
        )
        self.progress_slider.pack(fill=tk.X, padx=10, pady=5)

        # Мітка часу
        self.time_label = tk.Label(
            self.root,
            text="00:00 / 00:00",
            font=("Arial", 10),
            bg="#2b2b2b",
            fg="white"
        )
        self.time_label.pack(pady=5)

        # Фрейм для кнопок керування
        control_frame = tk.Frame(self.root, bg="#2b2b2b")
        control_frame.pack(pady=10)

        # Кнопки керування
        btn_style = {
            "font": ("Arial", 12),
            "width": 10,
            "bg": "#4c4c4c",
            "fg": "white",
            "activebackground": "#5c5c5c",
            "activeforeground": "white",
            "relief": tk.FLAT,
            "bd": 0,
            "highlightthickness": 0
        }

        self.play_pause_btn = tk.Button(
            control_frame,
            text="▶ Play",
            command=self.play_pause,
            **btn_style
        )
        self.play_pause_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame,
            text="⏹ Stop",
            command=self.stop,
            **btn_style
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame,
            text="⏪ -10s",
            command=self.backward,
            **btn_style
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame,
            text="⏩ +10s",
            command=self.forward,
            **btn_style
        ).pack(side=tk.LEFT, padx=5)

    def open_file(self):
        """Відкриття локального файлу"""
        file_path = filedialog.askopenfilename(
            title="Виберіть файл",
            filetypes=[
                ("Медіа файли", "*.mp3 *.mp4 *.avi *.mkv *.wav *.ogg *.flac *.mov *.wmv"),
                ("Аудіо", "*.mp3 *.wav *.ogg *.flac"),
                ("Відео", "*.mp4 *.avi *.mkv *.mov *.wmv"),
                ("Всі файли", "*.*")
            ]
        )

        if file_path:
            try:
                self.current_file = file_path
                media = self.instance.media_new(file_path)
                self.player.set_media(media)
                self.player.play()
                self.is_playing = True
                self.play_pause_btn.config(text="⏸ Pause")

                # Оновлення заголовка вікна
                filename = Path(file_path).name
                self.root.title(f"Медіаплеєр - {filename}")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося відкрити файл:\n{str(e)}")

    def open_stream(self):
        """Відкриття потокового медіа"""
        url = simpledialog.askstring(
            "Відкрити потік",
            "Введіть URL потоку:",
            parent=self.root
        )

        if url:
            try:
                # Очищення URL від пробілів (виправлення для стрімів)
                url = url.strip()

                media = self.instance.media_new(url)
                self.player.set_media(media)
                self.player.play()
                self.is_playing = True
                self.play_pause_btn.config(text="⏸ Pause")
                self.root.title(f"Медіаплеєр - Потік")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося відкрити потік:\n{str(e)}")

    def play_pause(self):
        """Відтворення / Пауза"""
        if self.player.is_playing():
            self.player.pause()
            self.is_playing = False
            self.play_pause_btn.config(text="▶ Play")
        else:
            self.player.play()
            self.is_playing = True
            self.play_pause_btn.config(text="⏸ Pause")

    def stop(self):
        """Зупинка відтворення"""
        self.player.stop()
        self.is_playing = False
        self.play_pause_btn.config(text="▶ Play")
        self.progress_slider.set(0)
        self.time_label.config(text="00:00 / 00:00")
        self.root.title("Медіаплеєр")

    def forward(self):
        """Перемотка вперед на 10 секунд"""
        current_time = self.player.get_time()
        if current_time != -1:
            self.player.set_time(current_time + 10000)  # +10 секунд у мілісекундах

    def backward(self):
        """Перемотка назад на 10 секунд"""
        current_time = self.player.get_time()
        if current_time != -1:
            new_time = max(0, current_time - 10000)  # -10 секунд у мілісекундах
            self.player.set_time(new_time)

    def set_position(self, value):
        """Зміна позиції відтворення через повзунок"""
        # ВИПРАВЛЕННЯ: блокуємо автооновлення під час переміщення повзунка
        self.is_user_seeking = True
        position = float(value) / 100
        self.player.set_position(position)
        # Розблокуємо через 300 мс
        self.root.after(300, lambda: setattr(self, 'is_user_seeking', False))

    def update_progress(self):
        """Оновлення повзунка прогресу та часу"""
        try:
            # ВИПРАВЛЕННЯ: оновлюємо повзунок ТІЛЬКИ якщо користувач не переміщує його
            if not self.is_user_seeking:
                position = self.player.get_position()
                if position != -1 and position > 0:
                    self.progress_slider.set(position * 100)

            # Час оновлюємо завжди
            current_time = self.player.get_time()
            total_time = self.player.get_length()

            if current_time != -1 and total_time != -1:
                current_str = self.format_time(current_time)
                total_str = self.format_time(total_time)
                self.time_label.config(text=f"{current_str} / {total_str}")
        except:
            pass

        # Рекурсивний виклик через 500 мс
        self.root.after(500, self.update_progress)

    def format_time(self, milliseconds):
        """Форматування часу з мілісекунд у MM:SS"""
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"


if __name__ == "__main__":
    root = tk.Tk()
    app = MediaPlayer(root)
    root.mainloop()
