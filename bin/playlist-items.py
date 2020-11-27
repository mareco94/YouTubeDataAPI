#!/usr/bin/env python3

###############################################################
#
# Script Name	:	playlist-items.py
#
# Description	:	Scipt to get:
# 					1) get a playlist's info
#					Returns a collection of playlist items 
# 					that match the API request parameters.
#  					You can retrieve all of the playlist items 
# 					in a specified playlist.
# 
# Args			:	-i [input playlist ID]
#					-u [input playlist URL]
#					-d [display basic info] - default stored TRUE
#					-h [HElP MESSAGE]
#
# Version		:	25-09-2020
#
# Author		:	Maria Oikonomidou
# Email			:	mareco@ics.forth.gr 
# 
###############################################################


import sys
import json
import csv
import optparse
import pprint
import config as cfg
import urllib.parse as urlparse


def get_playlist_metadata(items):
	
	playlist_info = {}

	if "items" in items[0].keys():
		
		playlist_info={
	#		'_id' : items[0]["items"][0]["snippet"]["playlistId"],
			'playlistID' : items[0]["items"][0]["snippet"]["playlistId"],
			'totalVideos' : items[0]["pageInfo"]["totalResults"],
			'channelName' : items[0]["items"][0]["snippet"]["channelTitle"],
			'channelID' : items[0]["items"][0]["snippet"]["channelId"]
		}
	
		videoids = []
		allitems = []
	
		for i in items:
			for data in i["items"]:
				videoids.append(data['contentDetails']['videoId'])
				allitems.append(data)
	
	
		playlist_info.update({'videoIDs': videoids})
		playlist_info.update({'videoData': allitems})
	

	return playlist_info



def print_basic_info(collection):
    if(collection.keys()):

        basic ={
                'playlistID' : collection['playlistID'],
                'totalVideos' : collection['totalVideos'],
                'channelName' : collection['channelName'],
                'channelID' : collection['channelID'],
                'videoIDs' : collection['videoIDs']
	}

        pprint.pprint(basic)



def create_parameters(options):

	PARAMETERS = {
	'part' :"snippet,contentDetails,status,id",
	'maxResults' : 50,
	'key': cfg.API_KEY
	}	

	# url for input 
	if options.url:
		url_data = urlparse.urlparse(options.url)
		query = urlparse.parse_qs(url_data.query)
		playlistId = query["list"][0]

	# playlist id for input 
	else:
		playlistId = options.plid

	PARAMETERS.update({'playlistId': playlistId})


	return PARAMETERS



def main():

	parser = optparse.OptionParser()
	parser.add_option("-u", "--url", dest = "url" , default=False, help="playlist URL")
	parser.add_option("-i", "--id", dest = "plid", default=False, help="playlist ID")
	parser.add_option('-d',"--display", dest = "display", action="store_true", default=True, help="display query response")
	
	(options,args) = parser.parse_args()

	if options.url == False and options.plid == False and options.vid == False:
		parser.print_help()
		sys.exit(1)

	PARAMETERS = create_parameters(options)


	response = cfg.requestURL(cfg.PLAYLIST_ITEMS,PARAMETERS)
	result = json.loads(response)

	items = []
	items.append(result)

	nextPageToken = result.get("nextPageToken")

	while nextPageToken:
		PARAMETERS.update({'pageToken': nextPageToken})
		response = cfg.requestURL(cfg.PLAYLIST_ITEMS,PARAMETERS) # create url
		result = json.loads(response)
		nextPageToken = result.get("nextPageToken")
		items.append(result)
		PARAMETERS.update({'pageToken': nextPageToken})

	collection = get_playlist_metadata(items)

	if options.display:
		print_basic_info(collection)


if __name__ == "__main__":
	main()
