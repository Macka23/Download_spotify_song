import pytube
import requests
from secrets import *
import base64
from pytube import YouTube


def getID(connector_to_process):
    list = connector_to_process.split('/')
    list1 = list[4].split('?')
    return list1[0]


# Authorization
url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

# Encode as Base64
message = f"{clientId}:{clientSecret}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')

headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"

r = requests.post(url, headers=headers, data=data)

token = r.json()['access_token']

urlSong = str(input("Enter the url song : "))

while not urlSong.find('track'):
    print("This is not a track link.")
    urlSong = str(input("Enter the url song : "))


songID = getID(urlSong)

trackurl = f"https://api.spotify.com/v1/tracks/{songID}"

headers = {
    "Authorization": "Bearer " + token
}

res = requests.get(url=trackurl, headers=headers)

name_main_artist = ""
name_second_artist = ""

resAPI = res.json()
song_name = resAPI.get('name')
artist = resAPI.get('artists')

for i in artist:
    if name_main_artist != "":
        name_second_artist = i.get('name')
        break
    name_main_artist = i.get('name')

title = name_main_artist + " " + name_second_artist + " - " + song_name
search = pytube.Search(title)
results = search.results

search_object = str(results[0])
split1 = search_object.split(':')
split2 = split1[1].split('=')
key = ""

for i in split2[1]:
    if i != '>':
        key += i
url_yt = "https://www.youtube.com/watch?v=" + key
yt = YouTube(url_yt)

stream = yt.streams.get_by_itag(251)
stream.download(output_path)
print(yt.title)
print(url_yt)
print("Downloaded successfully.")