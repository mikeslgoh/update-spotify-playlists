import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from enum import Enum

class Time(Enum):
	DAYS = 1
	MONTHS = 30
# Set up Spotify API credentials
redirect_uri = 'http://localhost:8080/callback'  # Set this to your preferred redirect URI
creds_file_path = "credentials.json"
playlist_file_path = "playlists.json"
playlist_length = 30
# Track must not be in the playlist for at least 3 months before being added again
previous_track_added_date_threshold = 3
previous_track_added_date_units = Time.MONTHS

# Need a banned list as some artist do not match genre that is selected
banned_artist_list = ['Justin Bieber', 'Green Day']
sp = None
user = None

def get_playlists():
	with open(playlist_file_path, 'r') as file:
		playlists = json.load(file)
	
	if playlists is None:
		raise Exception('ERROR: No playlists were defined ...')
	return playlists

def setup_spotify_credentials():
	creds = None
	with open(creds_file_path, 'r') as file:
		creds = json.load(file)
	
	if creds is not None:
		global sp
		global user
		user = creds['user']
		sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=creds['client_id'],
											   client_secret=creds['client_secret'],
											   redirect_uri=redirect_uri,
											   scope="playlist-modify-public"))
	
	if sp is None:
		raise Exception('ERROR: spotify credentials not setup correctly ...')
	if user is None:
		raise Exception('ERROR: user is not set ...')

def get_genre_list():
	print(sp.recommendation_genre_seeds())

def save_previous_tracks(playlist_id):
	tracks = get_previous_tracks(playlist_id)
	results = sp.playlist_tracks(playlist_id)
	for item in results['items']:
		track = item['track']
		track_info = {
			'id': track['id'],
			'name': track['name'],
			'artists': [artist['name'] for artist in track['artists']],
		}
		if track_info['id'] not in [track['id'] for track in tracks]:
			track_info['date_added'] = datetime.today().isoformat()
			tracks.append(track_info)
	json_file = f'{playlist_id}_playlist_tracks.json'
	with open(json_file, 'w') as file:
		json.dump(tracks, file, indent=4)
	print(f'Previous tracks from playlist {playlist_id} have been saved to {json_file}...')
	return tracks

def check_playlist_exist(playlist_name) -> str:
	playlists = sp.current_user_playlists()
	playlist_id = None
	for item in playlists['items']:
		if item['name'] == playlist_name:
			playlist_id = item['id']
			print(f"Playlist '{playlist_name}' already exists. Overwriting...")
			save_previous_tracks(playlist_id=playlist_id)
			break
	if playlist_id is None:
		# Create a new playlist if it doesn't exist
		playlist = sp.user_playlist_create(user=user, name=playlist_name)
		playlist_id = playlist['id']
		print(f"Playlist '{playlist_name}' created successfully.")
	return playlist_id

def get_previous_tracks(playlist_id):
	json_file = f'{playlist_id}_playlist_tracks.json'
	try:
		with open(json_file, 'r') as file:
			previous_tracks = json.load(file)
		return previous_tracks
	except (json.JSONDecodeError, FileNotFoundError):
		return []

def is_track_unique(artists_set, artists):
	return not any(artist in artists_set for artist in artists) and not any(artist in banned_artist_list for artist in artists)

def has_track_been_added_before(new_track, previous_tracks):
	for prev_track in previous_tracks:
		if new_track['id'] is prev_track['id'] and \
			abs((datetime.fromisoformat(prev_track['date_added']) - datetime.today()).days) > previous_track_added_date_threshold * previous_track_added_date_units.value:
			return True
	return False

# Filter tracks to keep only those with unique artists and have not been in the playlist for X amount of time
def get_unique_tracks(genre, playlist_id):
	unique_tracks = []
	artists_set = set()
	previous_tracks = get_previous_tracks(playlist_id=playlist_id)

	while len(unique_tracks) < playlist_length:
		recommended_tracks = sp.recommendations(seed_genres=[genre], limit=15, country='US')
		for track in recommended_tracks['tracks']:
			artists = [artist['name'] for artist in track['artists']]
			if is_track_unique(artists_set, artists) and not has_track_been_added_before(track, previous_tracks):
				if len(unique_tracks) < playlist_length:
					unique_tracks.append(track)
					artists_set.update(artists)
	return unique_tracks

def create_playlist(genre, playlist_name):
	# Get a list of recommended tracks based on the specified genre
	playlist_id = check_playlist_exist(playlist_name=playlist_name)
	
	recommended_tracks = get_unique_tracks(genre=genre, playlist_id=playlist_id)

	# Extract track IDs
	track_ids = [track['id'] for track in recommended_tracks]
	
	# Add tracks to the new playlist
	sp.playlist_replace_items(playlist_id, [])
	sp.user_playlist_add_tracks(user=user,playlist_id=playlist_id, tracks=track_ids)

def create_playlists(playlists):
	for playlist in playlists:
		create_playlist(playlist['genre'], playlist['title'])

def main():
	setup_spotify_credentials()
	create_playlists(get_playlists())

if __name__ == "__main__":
    main()