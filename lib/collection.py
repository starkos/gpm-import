import string

from lib.playlist import Playlist


class Collection:
	def __init__(self, songs, playlists, service):
		self.songs = songs
		self.playlists = playlists
		self.service = service


	def addPlaylist(self, title, description):
		playlist = self.service.addPlaylist(title, description)
		self.playlists.append(playlist)
		return playlist


	def addSongFromSearchResults(self, externalSong):
		song = self.service.addSongFromSearchResults(externalSong)
		self.songs.append(song)
		return song


	def addSongToPlaylist(self, song, playlist):
		self.service.addSongToPlaylist(song, playlist)
		playlist.songs.append(song)


	def findPossibleMatches(self, song):
		query = " ".join([song.title, song.artist])
		query = query.translate(query.maketrans("", "", string.punctuation))  # remove all punctuation
		return self.service.search(query)


	def getExactPlaylistMatch(self, targetPlaylist):
		for playlist in self.playlists:
			if playlist == targetPlaylist:
				return playlist
		return None


	def getExactSongMatch(self, targetSong):
		if targetSong in self.songs:
			return self.songs[targetSong]
		else:
			return None


	def importPlaylist(self, externalPlaylist):
		if externalPlaylist in self.playlists:
			playlist = self.playlists[externalPlaylist]
		else:
			playlist = self.service.addPlaylist(externalPlaylist.title, externalPlaylist.description)
			self.playlists.append(playlist)
		return playlist


	def likeSong(self, song):
		self.service.likeSong(song)
		song.rating = 5


	def search(self, query):
		return self.service.search(query)
