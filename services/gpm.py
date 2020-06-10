import csv
import html
import os

from gmusicapi import Mobileclient

from lib.collection import Collection
from lib.playlist import Playlist
from lib.song import Song, SongSet
from services.null import NullService


class Gpm:
	def __init__(self):
		self.client = Mobileclient()
		# self.client.perform_oauth()
		self.client.oauth_login(Mobileclient.FROM_MAC_ADDRESS)


	def fetchCollection(self):
		songs = self.__makeSongSet(self.client.get_all_songs())

		playlists = list()
		for playlistData in self.client.get_all_user_playlist_contents():
			playlist = self.__makePlaylist(playlistData)
			if playlist is not None:
				playlists.append(playlist)

		return Collection(songs, playlists, self)


	def __makePlaylist(self, playlistData):
		if playlistData["deleted"] == "True":
			return None

		title = playlistData["name"]
		description = playlistData["description"] if "description" in playlistData else None
		serviceId = playlistData["id"]
		songs = self.__makeSongSet(playlistData["tracks"])
		return Playlist(title, description, songs, serviceId)


	def __makeSongSet(self, songSetData):
		songs = list()
		for songData in songSetData:
			song = self.__makeSong(songData)
			if song is not None:
				songs.append(song)
		return SongSet(songs)


	def __makeSong(self, songData):
		if songData["kind"] == "sj#playlistEntry":
			if songData["deleted"] == "True" or not "track" in songData:
				return None
			songData = songData["track"]

		isDeleted = songData["deleted"] if "deleted" in songData else False
		if isDeleted:
			return None

		title = songData["title"]
		artist = songData["artist"]
		album = songData["album"]
		rating = int(songData["rating"]) if "rating" in songData else 0
		serviceId = songData["id"] if "id" in songData else songData["storeId"]

		return Song(title, artist, album, rating, serviceId)


	@staticmethod
	def loadTakeoutExport(exportPath):
		songsPath = os.path.join(exportPath, "Tracks")
		songs = Gpm.loadTakeoutSongSet(songsPath)

		playlists = list()
		playlistsPath = os.path.join(exportPath, "Playlists")
		for playlistFileName in sorted(os.listdir(playlistsPath)):
			if playlistFileName != "Thumbs Up":
				playlist = Gpm.loadTakeoutPlaylist(os.path.join(playlistsPath, playlistFileName))
				if playlist is not None:
					playlists.append(playlist)

		return Collection(songs, playlists, NullService())


	@staticmethod
	def loadTakeoutPlaylist(exportPath):
		title = os.path.basename(exportPath)
		description = ""
		isDeleted = False

		metadataPath = os.path.join(exportPath, "Metadata.csv")
		with open(metadataPath) as metadataFile:
			metadata = next(csv.DictReader(metadataFile))
			title = metadata["Title"]
			description = metadata["Description"]
			isDeleted = (metadata["Deleted"] == "Yes")

		if isDeleted:
			return None

		songs = Gpm.loadTakeoutSongSet(os.path.join(exportPath, "Tracks"))
		return Playlist(title, description, songs, None)


	@staticmethod
	def loadTakeoutSongSet(exportPath):
		songs = list()
		for songFileName in sorted(os.listdir(exportPath)):
			song = Gpm.loadTakeoutSong(os.path.join(exportPath, songFileName))
			if song is not None:
				songs.append(song)
		return SongSet(songs)


	@staticmethod
	def loadTakeoutSong(exportPath):
		with open(exportPath) as songFile:
			metadata = next(csv.DictReader(songFile))
			title = html.unescape(metadata["Title"].strip(" "))
			artist = html.unescape(metadata["Artist"].strip(" "))
			album = html.unescape(metadata["Album"].strip(" "))
			rating = int(metadata["Rating"])
			isDeleted = (metadata["Removed"] == "Yes")

		if isDeleted or (title == "" and artist == "" and album == ""):
			return None

		return Song(title, artist, album, rating, None)


	def addPlaylist(self, title, description):
		playlistId = self.client.create_playlist(title, description)
		return Playlist(title, description, list(), playlistId)


	def addSongFromSearchResults(self, song):
		trackId = self.client.add_store_tracks([song.serviceId])
		return Song(song.title, song.artist, song.album, song.rating, trackId)


	def addSongToPlaylist(self, song, playlist):
		self.client.add_songs_to_playlist(playlist.serviceId, song.serviceId)


	def likeSong(self, song):
		self.client.rate_songs({ "id": song.serviceId }, "5")


	def search(self, query):
		matches = list()
		searchResults = self.client.search(query)
		for songHit in searchResults["song_hits"]:
			song = self.__makeSong(songHit["track"])
			matches.append(song)
		return matches
