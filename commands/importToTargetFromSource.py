def importToTargetFromSource(target, source, skippedSongsPath):
	for song in source.songs:
		playlists = __getSourcePlaylists(source, song)
		__showNextSong(song, playlists)

		matches = target.findPossibleMatches(song)
		canKeep = (target.getExactSongMatch(song) is not None)

		while True:
			__showOptions(matches, canKeep)

			choice = __getUserInput(matches, canKeep)
			if choice == "K":
				__importSong(target, song, song.rating, playlists)
				break
			elif choice == "S":
				query = __getUserQuery()
				matches = target.search(query)
			elif choice == "X":
				__logSkippedSong(song, playlists, skippedSongsPath)
				break
			else:
				__importSong(target, matches[int(choice)], song.rating, playlists)
				break


def __getSourcePlaylists(source, song):
	playlists = list()
	for playlist in source.playlists:
		if song in playlist.songs:
			playlists.append(playlist)
	return playlists


def __showNextSong(song, playlists):
	print()
	print("IMPORTING", song)
	if len(playlists) > 0:
		print("  Found in", [playlist.title for playlist in playlists])
	print()


def __showOptions(matches, canKeep):
	if canKeep:
		print("  [K] KEEP EXISTING")

	numMatches = min(len(matches), 10)
	for i in range(numMatches):
		print("  [{}] {}".format(i, matches[i]))

	print("  [S] Search manually")
	print("  [X] Skip this song")


def __getUserInput(matches, canKeep):
	while True:
		choice = input("? ").upper()
		if choice == "K" and canKeep:
			return "K"
		elif choice >= "0" and choice <= "9" and int(choice) < len(matches):
			return choice
		elif choice == "X" or choice == "S":
			return choice
		else:
			print("Invalid choice")


def __getUserQuery():
	return input("New query? ")


def __logSkippedSong(song, playlists, skippedSongsPath):
	with open(skippedSongsPath, "a") as skipFile:
		skipFile.write("{}\n".format(song))
		skipFile.write("  Rating: {}\n".format(song.rating))
		if len(playlists) > 0:
			skipFile.write("  Playlists: {}\n".format([playlist.title for playlist in playlists]))


def __importSong(target, externalSong, externalRating, externalPlaylists):
	song = target.getExactSongMatch(externalSong)
	if song is None:
		print("Adding to library...")
		song = target.addSongFromSearchResults(externalSong)
	else:
		print("Already in library")

	if song.rating < 5 and externalRating > 3:
		print("Marking song liked...")
		target.likeSong(song)

	for externalPlaylist in externalPlaylists:
		playlist = target.getExactPlaylistMatch(externalPlaylist)
		if playlist is None:
			print("Creating playlist '{}'...".format(externalPlaylist.title))
			playlist = target.addPlaylist(externalPlaylist.title, externalPlaylist.description)
		if not song in playlist.songs:
			print("Adding to playlist '{}'...".format(externalPlaylist.title))
			target.addSongToPlaylist(song, playlist)
