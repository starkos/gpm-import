def addMissingSongsFromPlaylists(collection, callback):
	for playlist in collection.playlists:
		for song in playlist.songs:
			if not song in collection.songs:
				collection.songs.append(song)
				callback(playlist, song)
