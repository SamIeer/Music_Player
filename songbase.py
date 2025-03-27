import sqlite3

# Function to connect to the database
def connect_db():
    conn = sqlite3.connect("music_player.db")
    return conn

# Function to create the songs table if not exists
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            file_path TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a new song
def add_song(title, file_path):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO songs (title, file_path) VALUES (?, ?)", (title, file_path))
    conn.commit()
    conn.close()

# Function to fetch all songs
def get_all_songs():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()
    conn.close()
    return songs

# Create table when the script runs
create_table()
