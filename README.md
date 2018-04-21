# song of the hour

[song of the hour](https://twitter.com/randomizedsongs) is a Twitter bot that posts random songs from Spotify every hour. The bot uses a word list from [sindresorhus/word-list](https://github.com/sindresorhus/word-list), [Spotify Web API](https://beta.developer.spotify.com/documentation/web-api/), and Twitter API through [tweepy](https://github.com/tweepy/tweepy).

## Dependencies

* a recent version of Python 2 with [requests](https://github.com/requests/requests) and tweepy
* a scheduled command daemon
* Twitter and Spotify accounts (_obviously_)

## Installation
1. Clone the repository to your computer.
2. Download the `words.txt` file from [sindresorhus/word-list](https://github.com/sindresorhus/word-list).
2. Enter the required information in `spotify.py`. To obtain Spotify's tokens, you have to go through their authorization process, outlined [here](https://beta.developer.spotify.com/documentation/general/guides/authorization-guide/).
3. Configure your scheduled command daemon to run `spotify.py` with the desired interval.
4. Done!

## Contribution

Pull requests are welcomed.

## License

You can do whatever you want under the MIT license. See the `LICENSE` file for more information.
