#!/usr/bin/env python3

###############################################################
#
# Script Name	:	video-info.py
#
# Description	:	Scipt to get:
# 					1) get a video's meatadata
#							OR
# 					2) get most popular videos (YouTube Trends)
#						and their metadata
# 					Returns a list of videos that match 
# 					the API request parameters.
#
# Args			:	-i [video id input] -  multiple ids comma seperated 
# 					-u [video url input] 
# 					-p [search trending videos] - most popular 
# 					--region [search trending videos per region ] - regionCode eg. GR
# 					-r [max result number] - default 5
#					-d [display query response]
#					-h [HElP MESSAGE]
#
# Version		:	18-09-2020
#
# Author		:	Maria Oikonomidou
# Email			:	mareco@ics.forth.gr 
# 
###############################################################



import sys
import json
import pprint
import optparse
import config as cfg
import urllib.parse as urlparse


def get_video_info(videoList):
	collection = {}
	collection["videos"] = []


	for item in videoList:
		if item['kind'] == 'youtube#video':
			
			videoID = item['id']
			snip = item['snippet']
			content = item["contentDetails"]
			status = item["status"]
			statistics = item["statistics"]
			player = item["player"]
			recordingDetails = item["recordingDetails"] 

			topicDetails = {}
			if "topicDetails" in item.keys():
				topicDetails = item["topicDetails"] 

			video_info = {
				"videoID" : videoID,
				"videoTitle" : snip["title"],
				"snippet" : snip,
				"contentDetails" : content,
				"status" : status,
				"statistics" : statistics,
				"topicDetails" : topicDetails,
				"recordingDetails" : recordingDetails,
				"player" : player
			}
			
			collection["videos"].append(video_info)

	return collection



def print_collection(collection):
	for item in collection["videos"]:
		pprint.pprint(item)
		print("\n")

def get_basic_info(collection):

	item = collection["videos"][0]
	snip = item["snippet"]
	stats = item["statistics"]
	categories = []

	if "topicDetails" in item.keys():
		cati = item["topicDetails"]
		if "topicCategories" in cati.keys():
			categ = item["topicDetails"]["topicCategories"]
			for i in categ:
				cat = urlparse.urlparse(i).path.rsplit("/", 1)[-1]
				categories.append(cat.lower())
	commentCount = 0
	if "commentCount" in stats.keys():
		commentCount = stats["commentCount"]

	tags = []
	if "tags" in snip.keys():
		tags = snip["tags"]


	basic_info = {
		"videoID" : item["videoID"],
		"duration" : item["contentDetails"]["duration"],
		"categoryID" : snip["categoryId"],
		"channelID" : snip["channelId"],
		"description" : snip["description"],
		"title" : snip["title"],
		"publishedAt" : snip["publishedAt"],
		"tags" : tags,
		"commentCount" : commentCount,
		"dislikeCount" :  stats["dislikeCount"],
		"favoriteCount" : stats["favoriteCount"],
		"likeCount" : stats["likeCount"],
		"viewCount" : stats["viewCount"],
		"topicCategories" : categories
	}
	pprint.pprint(basic_info)



def create_parameters(options):
	
	PARAMETERS = {
		'part' :"snippet,liveStreamingDetails,statistics,status,topicDetails,contentDetails,recordingDetails,id,localizations,player",
		'key': cfg.API_KEY
	}

	if options.url or options.id:
		if options.url:
			url_data = urlparse.urlparse(options.url)
			query = urlparse.parse_qs(url_data.query)
			vid = query["v"][0]
		else:
			vid = options.id
		
		PARAMETERS.update({'id': str(vid)})
	
	if options.popular:
		PARAMETERS.update({'maxResults': maxResults})
		PARAMETERS.update({'chart': "mostPopular"})
		if options.regionCode:
			PARAMETERS.update({'regionCode': str(options.regionCode)})
	
	if options.maxResults: 
		PARAMETERS.update({'maxResults': options.maxResults})
	
	return PARAMETERS



def main():
	parser = optparse.OptionParser()
	parser.add_option("-u", "--url", dest = "url" , default=False, help="video url as input")
	parser.add_option("-i", "--id", dest = "id", default=False, help="video id as input")
	parser.add_option('-p',"--popular", dest = "popular", action="store_true", default=False, help="most popular videos")
	parser.add_option("--region", dest = "regionCode", default=False, help="popular videos per region")
	parser.add_option('-r',"--results", dest = "maxResults", default=False, help="search max result number")
	parser.add_option('-d',"--display", dest = "display", action="store_true", default=False, help="display query response")
	parser.add_option('-b',"--basic", dest = "basic", action="store_true", default=False, help="display query basic info")


	(options,args) = parser.parse_args()

	if options.url == False and options.id == False and options.popular == False:
		parser.print_help()
		sys.exit(1)

	PARAMETERS = create_parameters(options)
	
	response = cfg.requestURL(cfg.YOUTUBE_VIDEO,PARAMETERS) # create url
	result = json.loads(response)
		
	items = []

	if "items" in result.keys():
		for i in result["items"]:
			items.append(i)

	if options.popular == True:
		nextPageToken = result.get("nextPageToken")
		while nextPageToken:
			PARAMETERS.update({'pageToken': nextPageToken})
			response = cfg.requestURL(cfg.YOUTUBE_VIDEO,PARAMETERS)
			result = json.loads(response)
			
			if "items" in result.keys():
				for i in result["items"]:
					items.append(i)

			nextPageToken = result.get("nextPageToken")
		
	collection = get_video_info(items)

	if options.display == True:
		print_collection(collection)

	if options.basic == True:
		get_basic_info(collection)


if __name__ == "__main__":
	main()