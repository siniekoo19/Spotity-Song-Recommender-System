import streamlit as st
import pandas as pd
import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


page_bg_img = """
<style>
    [data-testid = stAppViewContainer]{
        background-image : url('https://miro.medium.com/v2/resize:fit:1400/0*8EEtCTgeUbv4xZ0W');
        background-size : cover;
    }
    [data-testid=stVerticalBlock]{
        border: 0.3px solid white;
        background-color:#000000ba;
    }

    # .css-1n76uvr {
    #     width: 817px;
    # }
    # .css-1pmdbur {
    #     width: 130px;
    # }


</style>
"""

st.markdown(page_bg_img, unsafe_allow_html = True)

CLIENT_ID = "ae486686c6504ef381e3c99d894d460d"
CLIENT_SECRET = "2f290c45a5a143d1bd39588e21de6a5f"

# Initialize the spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Get Song Cover URL
def get_song_album_cover_url(song_name, artist_name):
    search_qurey = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_qurey, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        ablum_cover_url = track["album"]["images"][0]["url"]
        return ablum_cover_url
    else:
        return "songcovernotfound_img.png"

# Recommender Function
def Recommend(music1):
    music_index = songs[songs['song'] == music1].index[0]
    distances = similarity[music_index]
    music_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
    
    recommended_songs = []
    recommended_songs_posters = []
    for i in music_list:
        artist = songs.iloc[i[0]].artist

        recommended_songs_posters.append(get_song_album_cover_url(songs.iloc[i[0]].song, artist))
        recommended_songs.append(songs.iloc[i[0]].song)

    return recommended_songs, recommended_songs_posters 

# Main Code
st.header('Music Recommendation System')

music_dict = pickle.load(open('music_dict.pkl', 'rb'))
songs = pd.DataFrame(music_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

music_list = list(["Select"]) + list(songs['song'].values)

selected_song = st.selectbox(label='Select a Song : ', options= music_list, index=0)

if st.button('Recommend'):
    names, posters = Recommend(selected_song)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])