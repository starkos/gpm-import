#!/usr/bin/env python3
import os

import commands
from services.gpm import Gpm

TAKEOUT_PATH = os.path.expanduser("~/Dropbox/Takeout/Google Play Music")
SKIPPED_SONGS_PATH = os.path.expanduser("~/Dropbox/gpm-skipped.txt")

def main():
	source = loadSourceCollection(TAKEOUT_PATH)
	target = loadTargetCollection(Gpm())

	addMissingSongsFromPlaylists(source)
	importToTargetFromSource(target, source, SKIPPED_SONGS_PATH)


def loadSourceCollection(exportPath):
	source = Gpm.loadTakeoutExport(TAKEOUT_PATH)
	print("Loaded source collection: {} songs, {} playlists".format(len(source.songs), len(source.playlists)))
	return source


def loadTargetCollection(service):
	target = service.fetchCollection()
	print("Loaded target collection: {} songs, {} playlists".format(len(target.songs), len(target.playlists)))
	return target


def addMissingSongsFromPlaylists(source):
	print("Adding missing songs from playlists to library...")
	def onAdd(playlist, song):
		# print("  Added {} from '{}'".format(song, playlist))
		onAdd.count += 1
	onAdd.count = 0
	commands.addMissingSongsFromPlaylists(source, onAdd)
	print("Added {} songs from playlists to library".format(onAdd.count))


def importToTargetFromSource(target, source, skippedSongsPath):
	commands.importToTargetFromSource(target, source, skippedSongsPath)


main()