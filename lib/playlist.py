class Playlist:
	def __init__(self, title, description, songs, serviceId):
		self.title = title
		self.description = description
		self.songs = songs
		self.serviceId = serviceId


	def __eq__(self, other):
		return (self.title == other.title)


	def __str__(self):
		return self.title
