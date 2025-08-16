import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_CLIENT")
print(client_id)


Date = "2020-03-01"
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}
response = requests.get(f"https://www.billboard.com/charts/hot-100/{Date}", headers)

soup = BeautifulSoup(response.text,'html.parser')

# songs_name_spans = soup.find_all("h3", id="title-of-a-story")
songs_name_spans = soup.select("li.o-chart-results-list__item h3#title-of-a-story")
songs_name = [song.getText().strip() for song in songs_name_spans]

sp = spotipy.Spotify(
    auth_manager= SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com",
        client_id= client_id,
        client_secret= client_secret,
        show_dialog= True,
        cache_path="token.txt",
        username="Sandeep"
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year = Date.split("-")[0]
for song in songs_name:
    result = sp.search(q=f"track: {song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)

    except IndexError:
        print(f"{song} doesn't exist in Spotify, skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{Date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)