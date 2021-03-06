
import json
import spotipy
import requests
from bs4 import BeautifulSoup 
import spotipy.util as util
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyOAuth
from pyfiglet import Figlet
from requests.utils import quote

user_ID= "bmpse4fdqb4lo6bzn0h81zxkq"

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

#This is the function for the cool banner. 

def render(text, style):
    f = Figlet(font=style)
    print(f.renderText(text))

render("The Doom Reaper", "slant") 

print("Doom reaper is a webscrapper software based on BBC1 playlist")


#this function is  used to get the authentification 

def auth():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="0403872f14e443248bc24988540275b8",
                                               client_secret="8c2e08a92513423d8d60bba51589cd01",
                                               redirect_uri="http://www.google.com",
                                               scope="playlist-modify user-read-private"))
    return sp 
#This function is used to scrap the daniel p.carter show and get the url of the show of the week. 
def get_link_homepage():
    url = "https://www.bbc.co.uk/programmes/b006wq4s/episodes/player"
    req = Request(url)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "lxml")
    start_url = "https://www.bbc.co.uk/sounds/play/"
    links = []
    links_without_none = []
    lst = []

    for link in soup.findAll('a'):
        links.append(link.get('href'))

    for i in links: 
        if i != None : 
            links_without_none.append(i) 
    
    sounds_url = [x for x in links_without_none if x.startswith(start_url)]
    return(sounds_url[0])


#this function stock_data() scrap the data on the BBC1 website and create a list ready to be search in spotify
def songs_list():
    url = get_link_homepage()
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    title = soup.p
    track = soup.find_all("p")
    artist = soup.find_all("p",{"class":"sc-c-basic-tile__artist sc-u-truncate gel-pica-bold gs-u-pr-alt@m gs-u-mb--"},)
    track_lst = []
    artist_lst = []
    lst = []
    for item in track:
        track_lst.append(item.text)
    for item in artist:
        artist_lst.append(item.text)

    for i,j in zip(artist_lst,track_lst):
        lst.append("artist:"+ i + " track:"+ j)
    print(lst)
    

#{"class":"sc-c-basic-tile__title sc-u-truncate gel-long-primer gs-u-pr-alt@m"}

    


# Get playlist tracks 
def get_playlist_tracks():
    user="bmpse4fdqb4lo6bzn0h81zxkq"
    playlist_id="3sJi9B5v8RNfJQ5TmRG0dv"
    sp = auth()
    track_list = []
    playlist_tracks = sp.user_playlist_tracks(user, playlist_id, fields='items,uri,name,id,total', market='fr')
    #print(playlist_tracks)
    #for i in playlist_tracks["items"]:
        #for 
        #print(i) 

    print(json.dumps(playlist_tracks, indent = 2 ))
    #for i in playlist_tracks:
        
    #print(playlist_tracks)
# Call the track deletion function

def playlist_remove_tracks():
    sp = auth()
    track_ids = "spotify:track:16Elz7HJPLZPMylp13ewxv"
    #sp.user_playlist_remove_all_occurrences_of_tracks(user="bmpse4fdqb4lo6bzn0h81zxkq", playlist_id="3sJi9B5v8RNfJQ5TmRG0dv", tracks_ids)


def remove_nested_parens():
    track_list = songs_list()
    cool_list = []
    for i in track_list:
        track = re.sub(r'\([^)]*\)', '', i)
        cool_list.append(track)
    return cool_list
    

#tracklist 
def track_lst_creator():
    track_lst = []
    sp = auth()
    lst = remove_nested_parens()
    error_counter = 0
    for i in lst:
        search = sp.search(q=i, limit=1, offset=0, type='track', market=None)
        songs = search["tracks"]["items"]
        if songs == []:
            error_counter = error_counter + 1
        else :
            uri = songs[0]["uri"]
            track_lst.append(uri)
    print(" ---------------- There was "+str(error_counter)+" error")
    sp.user_playlist_add_tracks(user="bmpse4fdqb4lo6bzn0h81zxkq", playlist_id="3sJi9B5v8RNfJQ5TmRG0dv", tracks=track_lst, position=None)

#get_playlist_tracks()
#playlist_remove_tracks()

#track_lst_creator()

songs_list()










