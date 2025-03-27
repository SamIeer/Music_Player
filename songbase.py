import sqlite3

# Connect to SQLite Database (Creates the file if it doesn't exist)
conn = sqlite3.connect("musicplayer.db")
cursor = conn.cursor()

# Create the 'songs' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        path TEXT NOT NULL UNIQUE
    )
""")
conn.commit()

def add_song(title, path):
    """Add a song to the database."""
    try:
        cursor.execute("INSERT INTO songs (title, path) VALUES (?, ?)", (title, path))
        conn.commit()
        print(f"Added song: {title}")
    except sqlite3.IntegrityError:
        print("Song already exists in the database.")

def get_all_songs():
    """Fetch all songs from the database."""
    cursor.execute("SELECT * FROM songs")
    return cursor.fetchall()

def delete_song(song_id):
    """Delete a song from the database."""
    cursor.execute("DELETE FROM songs WHERE id = ?", (song_id,))
    conn.commit()
    print(f"Deleted song with ID: {song_id}")

# Close the connection when done (not needed in script mode)
# conn.close()
