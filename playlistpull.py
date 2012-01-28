# coding: utf-8

from BeautifulSoup import BeautifulSoup
import gdata.youtube
import gdata.youtube.service
import urlparse
import webbrowser
import random
import os
import time
import re
import urllib2
import string

word_search = re.compile('\w+')
count = 0
playlist = "new_file_yeah.txt"
played = []

def SearchAndPlay(search_terms):
	"""Plays the first result in a youtube search for the term"""
	video_info = you_tube_search(search_terms)
	if video_info:
		player(video_info[0], search_terms)
		sleeper(video_info[1])
		return video_info

def you_tube_search(search_terms):
	video = searcher(search_terms)
	if video:
		video_url = video.player.url
		video_duration = (video.duration.seconds)
		return [video_url, video_duration]


def tuner(playlist):
	"""Takes a playlist and returns a random line"""
	file = open(playlist, 'r')
	file_size = os.stat(playlist)[6]
	file.seek((file.tell()+random.randint(0,file_size-1))%file_size)
	file.readline()
	line = file.readline()
	line = line.strip()
	
	print line
	return line

def searcher(search_terms):
   """Search for terms in you tube and return the first result for
      artist and title """ 
	yt_service = gdata.youtube.service.YouTubeService()
	query = gdata.youtube.service.YouTubeVideoQuery()
	query.vq = search_terms
	query.racy = 'include'
	feed = yt_service.YouTubeQuery(query)
	if feed.entry:
		return feed.entry[0].media


def player(video_url, search_terms):
    """Play video in Firefox"""
	counter = 0
	x = webbrowser.get('firefox')
	x.open(video_url.strip())
	print video_url
	#webbrowser.open(video_url, new=2)

def sleeper(duration):
    """sleep for given time, keyboard interrupt (Ctrl-C) to cancel"""
	for i in range(0, int(duration)):
		try:
			time.sleep(1)

		except KeyboardInterrupt:
			break

def writer(name, duration, url, f):
    """writes to the file f"""	
	new_line = name.strip() + " " + url + "      " + str(duration) + "\n"
	f.write(new_line)
	

def scanner(title, f):
    """Checks if result is in file"""	
	for line in f:
		line = line.strip()
		
		if line[0:len(title)] == title:
			return [line[(len(title)+1):-7], line[-7:]]
					

def check_cache(title):
    """Main function, searches file, plays song, or searches youtube
       then plays song"""
	title = title[2:]
	f = open('cache.txt', 'r+')		
	cached = scanner(title, f)
	title = title.translate(string.maketrans("",""), string.punctuation)
	print title
	
	if cached:
		
		player(cached[0], title)
		sleeper(cached[1])
	else:
		
		video_data = SearchAndPlay(title)
		if video_data:
			writer(title, video_data[1], video_data[0] , f)
	
	f.close
		
#start of program
		
while count is not 7:
	
	play = tuner(playlist)
	if play not in played:
		check_cache(play)
		played.append(play)
		count += 1

