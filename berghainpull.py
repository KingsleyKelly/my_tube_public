# coding: utf-8
import sys
import urllib2
import re
import webbrowser
import itertools
from BeautifulSoup import BeautifulSoup

"""TO USE: Insert the club url as argument 1,
           and the start point for the list as
           argument number 2."""

url = sys.argv[1]
start_point = sys.argv[2]
def remove_all(sub, s):
	"Remove a substring from a string"
	return re.sub(re.escape(sub), '', s)

def flatten(listOfLists):
    "Flatten one level of nesting"
    return list(itertools.chain.from_iterable(listOfLists))

def soup_maker(url, to_find):
	end_url = urllib2.urlopen(url)
	soup = BeautifulSoup(end_url)
	return soup

def puller(url, element, to_find):
	"Workhorse puller"
	soup = soup_maker(url, to_find)
	found = soup.findAll(element)
	to_compile = re.compile(to_find)
	to_return = to_compile.findall(str(found))
	return to_return

def lazy_read(string, regex):
	"lazy reader for string"
	reader = re.compile(regex)
	read = reader.search(string)
	read = len(read.group())
	return read

def club_puller(url):
	"Pull all events from a club"
	night_urls = []
	night_list = puller(url, ('a', {"class" : "cat"}), '[/event.aspx?]+[0-9]{6}')
	
	for i in range(len(night_list)):
		night_url = "http://www.residentadvisor.net" + night_list[i]
		night_urls.append(night_url)
	return night_urls

def dj_puller(night_url):
	"Pull all djs playing on a night"
	djs_playing = []
	djs = puller(night_url, 'a', '/dj/.*?"')
	
	if djs != []:
		for dj in djs:
			dj = dj[0:-1]

			if dj[-4:] != '.jpg':
				dj_top_10 = "http://www.residentadvisor.net" + dj + "/top10"
				djs_playing.append(dj_top_10)

		return djs_playing

	else:
		return
	
def top10_puller(dj_top_10):

	"Pull all songs from a djs top 10"
	to_return = []
	new_artists_and_labels = []
	new_tracks = []
	
	top_soup = soup_maker(dj_top_10, top10_url)
	artists_and_labels = top_soup.findAll('div', { "style" : "height:45px;"})
	tracks = top_soup.findAll('td', { "style" : "padding:8px 8px 4px 0;"})

	for artist in artists_and_labels:
		new_artist = str(artist)
		new_artist.strip()
		if new_artist[0:27] == '<a href="/record-label.aspx':
			artists_and_labels.remove(artist)
		elif new_artist[0:38] == '<div style="height:45px;"><a href="/dj':
			found = lazy_read(new_artist, '/dj/.*?"')
			new_artists_and_labels.append(new_artist[(35+found+17):-10])
		else:
			new_artists_and_labels.append(new_artist[26:-6])

	for track in tracks:
		new_track = str(track)
		new_track.strip()
		if new_track[0:44] == '<td style="padding:8px 8px 4px 0;"><a href="':
			found = lazy_read(new_track, '/track.*?"')
			new_track = new_track[(44+found+17):-9]
		else:
			new_track = new_track[35:-5]	
		new_track = remove_all('<br />', new_track)
		new_tracks.append(new_track) 

	if len(new_tracks) == 10:
		for i in xrange(10):
			to_return.append([(i+1), new_tracks[i], new_artists_and_labels[i]])
	
		return to_return
	else:
		return
	
berghain = club_puller(url)[start_point:(start_point + 5)]
berghain = map(dj_puller, berghain)
berghain = flatten(berghain)

djs = map(top10_puller, berghain)
djs = filter(None, djs)
print djs
f = open('new_file_yeah.txt', 'r+')

r = flatten(djs)
print r
for i in r:
	f.write(str(i)[1:-1]+'\n')

f.close


