import pyodbc
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import CLIENT_ID, CLIENT_SECRET, SERVER, DATABASE

conn_str = (
    r'DRIVER={SQL Server};'
    rf'SERVER={SERVER};'  # Cambia por tu instancia de SQL Server
    rf'DATABASE={DATABASE};'    # Cambia por tu base de datos
    r'Trusted_Connection=yes;'
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Configurar las credenciales de Spotify
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Obtener la información del artista
artist_name = "Shakira"
result = sp.search(q=f'artist:{artist_name}', type='artist')
artist_info = result['artists']['items'][0]

# Crear y cargar datos en la tabla Artista
artista_data = {
    "Nombre": artist_info.get('name', ''),
    "Genero": ", ".join(artist_info.get('genres', [])),
    "Popularidad": artist_info.get('popularity', None),
    "Url_Spotify": artist_info.get('external_urls', {}).get('spotify', ''),
    "Seguidores": artist_info.get('followers', {}).get('total', None)
}

cursor.execute("""
    INSERT INTO Artista (Nombre, Genero, Popularidad, Url_Spotify, Seguidores)
    VALUES (?, ?, ?, ?, ?)
""", artista_data["Nombre"], artista_data["Genero"], artista_data["Popularidad"], artista_data["Url_Spotify"], artista_data["Seguidores"])

# Obtener los álbumes del artista
albums = sp.artist_albums(artist_info['id'], album_type='album')

for album in albums['items']:
    album_data = {
        "Nombre_Artista": artist_info.get('name', ''),
        "Nombre_Album": album.get('name', ''),
        "Label": album.get('label', ''),
        "Total_Tracks": album.get('total_tracks', None),
        "Generos": ", ".join(artist_info.get('genres', [])),
        "Release_Date": album.get('release_date', None)
    }

    cursor.execute("""
        INSERT INTO Album (Nombre_Artista, Nombre_Album, Label, Total_Tracks, Generos, Release_Date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, album_data["Nombre_Artista"], album_data["Nombre_Album"], album_data["Label"], album_data["Total_Tracks"], album_data["Generos"], album_data["Release_Date"])

    # Obtener las pistas del álbum
    tracks = sp.album_tracks(album['id'])

    for track in tracks['items']:
        #print("track: ", track)
        track_data = {
            "Nombre_Artista": artist_info.get('name', ''),
            "Nombre_Album": album.get('name', ''),
            "Nombre_Track": track.get('name', ''),
            # "Disc_Number": track.get('disc_number', None),
            "Duration_ms": track.get('duration_ms', None),
            "Explicit": track.get('explicit', False),
            "Artists": ", ".join([artist['name'] for artist in track.get('artists', [])]),
            "Track_Number": track.get('track_number', None)
            # "Popularidad": track.get('popularity', None)
        }

        cursor.execute("""
            INSERT INTO Track (Nombre_Artista, Nombre_Album, Nombre_Track, Duration_ms, Explicit, Artists, Track_Number)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, track_data["Nombre_Artista"], track_data["Nombre_Album"], track_data["Nombre_Track"], track_data["Duration_ms"], track_data["Explicit"], track_data["Artists"], track_data["Track_Number"])

# Confirmar las transacciones
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()
