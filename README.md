# Spotify Script
## What can it do?
* Create and update Spotify playlists using the playlist title and genre
* Update the playlist with unique tracks that have not been added before (within the past 3 months) and no duplicate artists
## Other Features
* Configure how long to wait before allowing previous tracks to be added to your playlists
* View tracks that have been previously as JSON
* Specify which artist shouldn't be added to your playlists
* Configure your Spotify API credentials and playlist info
## How does it work?
* Clone and navigate to the project repo
* Enter your Spotify API credentials and username (can be found on your Spotify profile). Instructions for API credentials can be found [here](https://developer.spotify.com/documentation/web-api)
* Enter your playlist details following the examples shown
* If you are using an IDE and on Windows, you will need to run the following:
```
python -m venv .venv
.\.venv\Scripts\activate
```
> You can do similar commands on Mac as well
* Install dependencies using `pip install -r requirements.txt`
* Run the script either through the IDE or command line (no input required!)
> It may ask you to log into your Spotify account to give authorization when you run the script
