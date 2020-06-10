import collections

class Song:
	def __init__(self, title, artist, album, rating, serviceId):
		self.title = title
		self.artist = artist
		self.album = album
		self.rating = rating
		self.serviceId = serviceId
		self.key = "{}~{}~{}".format(title, artist, album)

	def __str__(self):
		return "'{}' ({}/{})".format(self.title, self.artist, self.album)


class SongSet(list):
	def __init__(self, songs):
		self.super = super(SongSet, self)
		self.super.__init__(songs)
		self.index = {}
		for song in songs:
			self.index[song.key] = song

	def __contains__(self, song):
		return song.key in self.index

	def __getitem__(self, song):
		return self.index[song.key]

	def append(self, song):
		self.super.append(song)
		self.index[song.key] = song
