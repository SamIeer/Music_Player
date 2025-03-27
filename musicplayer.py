import os
import time
import random
from tkinter import Tk, Frame, Label, Button, Listbox, Scrollbar, filedialog, HORIZONTAL, Scale
from tkinter import ttk
from pygame import mixer
from mutagen.mp3 import MP3

from songbase import add_song, get_all_songs

# Example: Adding a song
add_song("Song Name", "C:/Users/hp/Music/song.mp3")

# Example: Fetching all songs
songs = get_all_songs()
for song in songs:
    print(f"ID: {song[0]}, Title: {song[1]}, Path: {song[2]}")


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x600")
        self.root.title("FreshTune Pro - Music Player")
        self.root.configure(bg='#1e1e1e')

        self.playlist = []
        self.is_paused = False
        self.current_song_index = None
        self.is_repeat = False
        self.is_shuffle = False

        self.initialize_mixer()
        self.setup_ui()
        self.load_songs_from_predefined_folder()

    def initialize_mixer(self):
        mixer.init()
        mixer.music.set_volume(0.5)

    def setup_ui(self):
        self.setup_song_list()
        self.setup_labels()
        self.setup_controls()
        self.setup_progress_bar()
        self.setup_volume_control()
        self.setup_add_song_button()
        self.setup_repeat_shuffle_buttons()

    # Change this path to your songs folder
    songs_folder = r"C:\Users\hp\OneDrive\Desktop\#PROJECTS\py.projects\Music_Player\songs"

    # Get all MP3 files from the folder
    mp3_files = [f for f in os.listdir(songs_folder) if f.endswith('.mp3')]

    # Add each song to the database
    for song in mp3_files:
        song_path = os.path.join(songs_folder, song)
        add_song(song, song_path)

    print("All songs have been added to the database!")

    def load_songs_from_predefined_folder(self):
        folder_path = "\\Music_Player\songs"  # Change this to your actual folder path

        if os.path.exists(folder_path):
            mp3_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".mp3")]

            if mp3_files:
               for song in mp3_files:
                song_name = os.path.basename(song)
                self.playlist.append(song)  # Store the full path
                self.song_list.insert('end', song_name)  # Display in Listbox
                print(f"Loaded {len(mp3_files)} songs from {folder_path}")
            else:
                print("No MP3 files found in the predefined folder.")
        else:
            print("The specified folder does not exist.")
 
    

    def setup_volume_control(self):
        volume_frame = Frame(self.root, bg='#282c34')
        volume_frame.pack(pady=10)

        volume_label = Label(volume_frame, text="Volume", bg='#282c34', fg='white', font=("Helvetica", 12))
        volume_label.grid(row=0, column=0, padx=10)

    # Create volume control slider (Scale)
        self.volume_scale = Scale(volume_frame, from_=0, to=100, orient=HORIZONTAL, command=self.set_volume, bg='#282c34', fg='white', font=("Helvetica", 12))
        self.volume_scale.set(50)  # Default volume set to 50%
        self.volume_scale.grid(row=0, column=1)

    def set_volume(self, value):
            volume = int(value)
            mixer.music.set_volume(volume / 100)  # Set volume as a float (0.0 to 1.0)
            print(f"Volume set to: {volume}%")
    
    def setup_add_song_button(self):
            button_frame = Frame(self.root, bg='#282c34')
            button_frame.pack(pady=10)

    # Create Add Song button
            add_song_btn = Button(button_frame, text="Add Song", font=("Helvetica", 12, 'bold'), bg='#3a3f4b', fg='white', command=self.add_song)
            add_song_btn.grid(row=0, column=0)

    def add_song(self):
        """Add a new song and store it in the database."""
        song_path = filedialog.askopenfilename(title="Select a song", filetypes=[("MP3 files", "*.mp3")])
        if song_path:
            song_name = os.path.basename(song_path)
            add_song(song_name, song_path)  # Store in database
            self.load_songs_from_database()  # Refresh GUI with new song

    def setup_repeat_shuffle_buttons(self):
            button_frame = Frame(self.root, bg='#282c34')
            button_frame.pack(pady=10)

    # Create Repeat button
            repeat_btn = Button(button_frame, text="Repeat", font=("Helvetica", 12, 'bold'), bg='#3a3f4b', fg='white', command=self.toggle_repeat)
            repeat_btn.grid(row=0, column=0, padx=10)

    # Create Shuffle button
            shuffle_btn = Button(button_frame, text="Shuffle", font=("Helvetica", 12, 'bold'), bg='#3a3f4b', fg='white', command=self.toggle_shuffle)
            shuffle_btn.grid(row=0, column=1, padx=10)

    def toggle_repeat(self):
                self.is_repeat = not self.is_repeat
                print(f"Repeat {'Enabled' if self.is_repeat else 'Disabled'}")

    def toggle_shuffle(self):
                self.is_shuffle = not self.is_shuffle
                print(f"Shuffle {'Enabled' if self.is_shuffle else 'Disabled'}")


    def setup_song_list(self):
       frame = Frame(self.root, bg='#3a3f4b')
       frame.pack(pady=10, padx=10, fill='both', expand=True)
    
       self.song_list = Listbox(frame, bg='#404552', fg='white', selectbackground='#ff5733', height=10)
       self.song_list.pack(side='left', fill='both', expand=True)
    
       scrollbar = Scrollbar(frame, command=self.song_list.yview)
       scrollbar.pack(side='right', fill='y')
       self.song_list.config(yscrollcommand=scrollbar.set)
       self.song_list.bind('<Double-1>', lambda event: self.play_song())

       self.load_songs_from_database()  # Load songs when the player starts

    def setup_labels(self):
        self.song_label = Label(self.root, text='No Song Playing', bg='#282c34', fg='white', font=("Helvetica", 12))
        self.song_label.pack(pady=10)

    def prev_song(self):
        """Play the previous song in the playlist."""
        if self.current_song_index is not None and self.current_song_index > 0:
            self.play_song(self.current_song_index - 1)

    def toggle_play_pause(self):
        """Toggle between play and pause."""
        if self.is_paused:
            mixer.music.unpause()
            self.play_pause_btn.config(text="⏸️")  # Change button text to pause icon
            self.is_paused = False
        else:
            mixer.music.pause()
            self.play_pause_btn.config(text="▶️")  # Change button text to play icon
            self.is_paused = True

    def next_song(self):
        """Play the next song in the playlist."""
        if self.current_song_index is not None and self.current_song_index < len(self.playlist) - 1:
            if self.is_shuffle:
                self.play_song(random.randint(0, len(self.playlist) - 1))  # Play random song if shuffle is ON
            else:
                self.play_song(self.current_song_index + 1)  # Play the next song
        elif self.is_repeat:
            self.play_song(self.current_song_index)  # Replay the current song if repeat is ON


    def setup_controls(self):
        button_frame = Frame(self.root, bg='#282c34')
        button_frame.pack(pady=10)

        btn_style = {'width': 5, 'height': 2, 'bg': '#3a3f4b', 'fg': 'white', 'font': ('Helvetica', 12, 'bold')}
        
        self.prev_btn = Button(button_frame, text="⏮", **btn_style, command=self.prev_song)
        self.prev_btn.grid(row=0, column=0, padx=10)
        
        self.play_pause_btn = Button(button_frame, text="▶", **btn_style, command=self.toggle_play_pause)
        self.play_pause_btn.grid(row=0, column=1, padx=10)

        
        self.next_btn = Button(button_frame, text="⏭", **btn_style, command=self.next_song)
        self.next_btn.grid(row=0, column=2, padx=10)

    def setup_progress_bar(self):
        controls = Frame(self.root, bg='#282c34')
        controls.pack(pady=10)

        self.start_time = Label(controls, text="00:00", bg='#282c34', fg='white')
        self.start_time.grid(row=0, column=0)
        
        self.progress_bar = ttk.Progressbar(controls, orient=HORIZONTAL, mode='determinate', length=300)
        self.progress_bar.grid(row=0, column=1, padx=20)
        
        self.end_time = Label(controls, text="00:00", bg='#282c34', fg='white')
        self.end_time.grid(row=0, column=2)

    def update_progress_bar(self):
        if mixer.music.get_busy():
            current_time = mixer.music.get_pos() / 1000
            converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
            
            if self.current_song_index is not None:
                song = MP3(self.playlist[self.current_song_index])
                song_length = song.info.length
                converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
                
                self.start_time.config(text=converted_current_time)
                self.end_time.config(text=converted_song_length)
                
                progress = (current_time / song_length) * 100
                self.progress_bar.config(value=progress)
                self.progress_bar.after(1000, self.update_progress_bar)
    
    def load_songs_from_database(self):
        """Fetch songs from the database and add them to the playlist & GUI."""
        songs = get_all_songs()
        self.playlist = []  # Reset playlist
        self.song_list.delete(0, 'end')  # Clear existing list

        for song in songs:
            song_id, title, path = song
            self.playlist.append(path)
            self.song_list.insert('end', title)  # Show only title in the GUI
        print(f"Loaded {len(songs)} songs from database.")

    def play_song(self, index=None):
        if index is None:
            selected_song_index = self.song_list.curselection()
            if selected_song_index:
                self.current_song_index = int(selected_song_index[0])
            else:
                return
        else:
            self.current_song_index = index
        
        song_path = self.playlist[self.current_song_index]
        try:
            mixer.music.load(song_path)
            mixer.music.play()
            self.song_label.config(text=self.song_list.get(self.current_song_index), fg='white')
            self.song_list.selection_clear(0, 'end')
            self.song_list.activate(self.current_song_index)
            self.song_list.selection_set(self.current_song_index)
            self.update_progress_bar()
        except Exception as e:
            print(f"Error loading song: {e}")

if __name__ == "__main__":
    root = Tk()
    music_player = MusicPlayer(root)
    root.mainloop()
