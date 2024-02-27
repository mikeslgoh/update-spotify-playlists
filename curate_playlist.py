import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up Spotify API credentials
client_id = 'TODO'
client_secret = 'TODO'
redirect_uri = 'http://localhost:8080/callback'  # Set this to your preferred redirect URI
user = 'TODO'
# Initialize Spotify client with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
											   client_secret=client_secret,
											   redirect_uri=redirect_uri,
											   scope="playlist-modify-public"))

def get_genre_list():
	print(sp.recommendation_genre_seeds())

def check_playlist_exist(playlist_name) -> str:
	playlists = sp.current_user_playlists()
	playlist_id = None
	for item in playlists['items']:
		if item['name'] == playlist_name:
			playlist_id = item['id']
			print(f"Playlist '{playlist_name}' already exists. Overwriting...")
			sp.playlist_replace_items(playlist_id, [])
			break
	if playlist_id is None:
		# Create a new playlist if it doesn't exist
		playlist = sp.user_playlist_create(user=user, name=playlist_name)
		playlist_id = playlist['id']
		print(f"Playlist '{playlist_name}' created successfully.")
	return playlist_id

def create_playlist(genre, playlist_name):
	# Get a list of recommended tracks based on the specified genre
	recommended_tracks = sp.recommendations(seed_genres=[genre], limit=30, country='US')
	
	playlist_id = check_playlist_exist(playlist_name=playlist_name)

	# Extract track IDs
	track_ids = [track['id'] for track in recommended_tracks['tracks']]
	
	# Add tracks to the new playlist
	sp.user_playlist_add_tracks(user=user,playlist_id=playlist_id, tracks=track_ids)
	
	print(f"Playlist '{playlist_name}' created successfully with {len(track_ids)} tracks.")

playlists = [{'genre': 'TODO', 'title': 'TODO'}]

for playlist in playlists:
	create_playlist(playlist['genre'], playlist['title'])

# DESCRIPTIONS
# Acoustic - Escape the chaos with 'Relax and Unwind.' Tune in weekly for calming tracks that soothe your soul. Press play, breathe, and find peace in music.
# Jazz - Sink into the laid-back vibes of 'Jazzy Lofi Lounge,' a weekly curated selection of smooth jazz beats. Perfect for unwinding and discovering new favorites.