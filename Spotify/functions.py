import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from os import path



def top_ten(arg_uri):
    client_id = ''
    client_secret = ''
    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    csv_path = path.join(path.dirname(__file__), 'regional-jp-weekly-2022-09-29.csv')
    songs = pd.read_csv(csv_path)

    uris = list(songs.iloc[:]['uri'])
    uris = [uri[14:] for uri in uris]

    music_features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']

    target_song_feature = spotify.audio_features(arg_uri)

    index_and_diff = [[0, i] for i in range(len(songs))]
    for (i, uri) in enumerate(uris):
        diff_sum = 0
        features = spotify.audio_features(uri)
        for feature in music_features:
            diff_sum += abs(target_song_feature[0][feature] - features[0][feature])
        index_and_diff[i][0] = diff_sum

    top_ten_data = sorted(index_and_diff)[:10]
    top_ten_songs = []
    for (i, data) in enumerate(top_ten_data):
        song_info = []
        song_info.append(i+1)
        song_info.append(songs.iloc[data[1]]['artist_names'])
        song_info.append(songs.iloc[data[1]]['track_name'])
        score = round(100 - data[0]*100/7, 2)
        song_info.append(score)
        top_ten_songs.append(song_info)
    
    return top_ten_songs
