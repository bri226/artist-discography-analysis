import requests
import pandas as pd
from tabulate import tabulate

def search_artist(artist_name):
    url = f'https://api.deezer.com/search/artist?q={artist_name}'
    response = requests.get(url)
    return response.json()

def get_artist_albums(artist_id):
    url = f'https://api.deezer.com/artist/{artist_id}/albums'
    response = requests.get(url)
    return response.json()

def get_album_tracks(album_id):
    url = f'https://api.deezer.com/album/{album_id}/tracks'
    response = requests.get(url)
    return response.json()

def get_album_details(album_id):
    url = f'https://api.deezer.com/album/{album_id}'
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    artist_name = "Taylor Swift"
    
    search_results = search_artist(artist_name)
    
    if search_results['data']:
        artist_data = search_results['data'][0]
        artist_id = artist_data['id']
        artist_name = artist_data['name']
        
        albums = get_artist_albums(artist_id)
        
        album_records = []
        track_records = []
        
        for album in albums['data']:
            album_id = album['id']
            album_title = album['title']
            
            # Obtener detalles del álbum
            album_details = get_album_details(album_id)
            release_date = album_details['release_date']
            cover_url = album_details['cover_xl']
            fans = album_details['fans']
            genre_id = album_details['genre_id']
            explicit_lyrics = album_details['explicit_lyrics']
            
            # Almacenar datos del álbum
            album_records.append({
                'album_id': album_id,
                'album_title': album_title,
                'artist_name': artist_name,
                'release_date': release_date,
                'cover_url': cover_url,
                'fans': fans,
                'genre_id': genre_id,
                'explicit_lyrics': explicit_lyrics
            })
            
            # Obtener canciones del álbum
            tracks = get_album_tracks(album_id)
            for track in tracks['data']:
                track_records.append({
                    'track_album': album_title,
                    'track_id': track['id'],
                    'track_title': track['title'],
                    'album_id': album_id,
                    'track_number': track['track_position'],
                    'duration': track['duration']
                })
        
        # Crear DataFrames
        album_df = pd.DataFrame(album_records)
        track_df = pd.DataFrame(track_records)
        
        # Mostrar los DataFrames
        print("Álbumes:")
        print(tabulate(album_df, headers='keys', tablefmt='pretty'))
        print("\nCanciones:")
        print(tabulate(track_df, headers='keys', tablefmt='pretty'))
