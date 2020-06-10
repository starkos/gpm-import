# gpm-tool

A bespoke script to import a [Google Play Music][gm] music collection from a [Google Takeout][gt] backup. Developed for my own personal use to move my library and playlists from one Google account to another as a one-shot import. In theory, should work to import any Google Takeout GPM export, but I've only tested with my own.

Unintended benefit: if you started your GPM library by uploading all of your music, the dry run mode will show all of the tracks that Google can't identify, along with the closest matches. In most cases, a simple metadata fix will improve the match.

Uses [gmusicapi][api] to interact with the GPM account.

## Usage

* _TODO: add a dry run option, recommend its use here_

* Uncomment line 3 (`mobileClient.perform_oauth()`) and follow the instructions to connect your GPM account. Then comment it back out again to use the cached credentials, so you don't have to redo it each run

## Known Limitations

**Does not attempt to upload songs**

While [gmusicapi][api] supports uploading, it wasn't important enough for me to bother with it. I used a dry run to identify the missing tracks, and then uploaded them into my collection manually before running the real import.

**It's bespoke**

In theory it ought to work with any GPM library, but I've only tested it with my own. Now that I've completed moving my library to its new home I'm no longer developing it (but I'll consider pull requests if anyone wants to submit a fix or improvement).

## Getting It

I haven't bothered trying to create a proper package; just download the script manually.

## Stay in touch

* Twitter - [@starkos](https://twitter.com/starkos)

## License

[MIT](https://opensource.org/licenses/MIT)

[gm]: https://play.google.com/music/listen
[gt]: https://takeout.google.com/settings/takeout
[api]: https://github.com/simon-weber/gmusicapi
