#!/usr/bin/python
import requests, tweepy
from random import randrange, randint

spotify_refresh_token = ""
spotify_access_token = ""
spotify_playlist_id = ""
spotify_username = ""
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

def getWord():
    # generate random 3-6 char word
    file = open("words.txt")
    line = next(file)
    for num, aline in enumerate(file):
        if randrange(num + 2):
            continue
        line = aline
    file.close()
    return line.strip()

def getOffset(word):
    # getting the max offset of a query
    spotifyHeaders = getAccessToken()
    r = requests.get("https://api.spotify.com/v1/search?q=" + word + "&type=track&offset=0&limit=1", headers=spotifyHeaders)
    songData = r.json()

    maxOffset = songData['tracks']['total']

    if maxOffset == 0:
        return -1

    return randint(0, 100000) if maxOffset > 100000 else randint(0, maxOffset - 1)

def getSong(word, offset):
    # get the song information, if it is existent
    spotifyHeaders = getAccessToken()
    r = requests.get("https://api.spotify.com/v1/search?q=" + word + "&type=track&offset=0&limit=1", headers=spotifyHeaders)
    songData = r.json()
    # pull the information out of the dict
    name = songData['tracks']['items'][0]['name']
    artist = songData['tracks']['items'][0]['artists'][0]['name']
    openUrl = songData['tracks']['items'][0]['external_urls']['spotify']
    songUri = songData['tracks']['items'][0]['uri']

    return name, artist, openUrl, songUri

def isDuplicate(uri):
    # check if the song already exists on playlist
    # getting the playlists total song count
    spotifyHeaders = getAccessToken()
    r = requests.get("https://api.spotify.com/v1/users/" + spotify_username + "/playlists/" + spotify_playlist_id + "/tracks?fields=total", headers=spotifyHeaders)
    totalNumber = r.json()['total']
    offset = 0
    for i in xrange((totalNumber // 100) + 1):
        # get songs from offset to offset + 99
        spotifyHeaders = getAccessToken()
        r = requests.get("https://api.spotify.com/v1/users/" + spotify_username + "/playlists/" + spotify_playlist_id + "/tracks?fields=items(track(uri))&offset=" + str(offset) + "&limit=100", headers=spotifyHeaders)
        songData = r.json()
        tracks = [x['track']['uri'] for x in songData['items']]
        if uri in tracks:
            return True
        else:
            offset = offset + 100
    return False

def getAccessToken():
    spotifyData = {'grant_type': 'refresh_token', 'refresh_token': spotify_refresh_token}
    spotifyHeaders = {"Authorization": "Basic " + spotify_access_token}
    r = requests.post("https://accounts.spotify.com/api/token", data=spotifyData, headers=spotifyHeaders)
    spotifyData = r.json()
    accessToken = spotifyData['access_token']
    spotifyHeaders = {"Authorization": "Bearer " + accessToken, "Accept": "application/json"}
    return spotifyHeaders

def main():
    # getting a word and a song
    offset = -1
    while (offset == -1):
        word = getWord()
        offset = getOffset(word)
    name, artist, openUrl, songUri = getSong(word, offset)

    if isDuplicate(songUri):
        main()
        exit()

    # tweeting
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    try:
        api.update_status("this hour's song is " + name + " by " + artist + ". listen it here: " + openUrl)
    except tweepy.TweepError as e:
        main()
        exit()

    # adding to the spotify playlist
    # getting a brand new access token
    spotifyHeaders = getAccessToken()
    # actually adding to the playlist
    r = requests.post("https://api.spotify.com/v1/users/" + spotify_username + "/playlists/" + spotify_playlist_id + "/tracks?uris=" + songUri, headers=spotifyHeaders)

if __name__ == "__main__":
    main()
