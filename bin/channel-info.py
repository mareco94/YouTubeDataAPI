#!/usr/bin/env python3

###############################################################
#
# Script Name	:	channel-info.py
#
# Description	:	Scipt to get:
# 					1) get a channel's meatadata
#
#					Returns a collection of zero or more channel 
# 					resources that match the request criteria.
#
# Args			:	-i [channel id input]
# 					-u [channel url input] 
# 					-n [channel name input]
#					-d [display query response]
#					-b [display query response basic info] - stored TRUE
#					-h [HElP MESSAGE]
#
#
# Version		:	21-09-2020
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


def get_channel_info(channel):
	collection = {}

	if "items" in channel.keys():
		
		item = channel["items"][0]
		
		channel_info = {
			'channelID' : item["id"],
			'snippet' : item["snippet"],
			'contentDetails' : item["contentDetails"],
			'statistics' : item["statistics"],
			'topicDetails' : item["topicDetails"],
			'status' : item["status"],
			'contentOwnerDetails' : item["contentOwnerDetails"],
			'brandingSettings' : item["brandingSettings"]
		}
		collection = channel_info
		
	return collection




def print_collection(collection):
		pprint.pprint(collection)
		print("\n")

def get_basic_info(collection):

		description = collection["snippet"]["description"]
		channelName = collection["snippet"]["title"]
		createdAt =  collection["snippet"]["publishedAt"]
		channelID =  collection["channelID"]
		totalViews =  collection["statistics"]["viewCount"]
		#totalComments =  collection["statistics"]["commentCount"]
		subscribers = collection["statistics"]["subscriberCount"]
		totalVideos = collection["statistics"]["videoCount"]
		privacyStatus =  collection["status"]["privacyStatus"] #string Privacy status of the channel. values : private - public - unlisted
		isLinked =  collection["status"]["isLinked"] # boolean Indicates whether the channel data identifies a user that is already linked to either a YouTube username or a Google+ account. A user that has one of these links already has a public YouTube identity, which is a prerequisite for several actions, such as uploading videos.
		longUploadsStatus =  collection["status"]["longUploadsStatus"] # Indicates whether the channel is eligible to upload videos that are more than 15 minutes long. This property is only returned if the channel owner authorized the API request. See the YouTube Help Center for more information about this feature.

		topicIDs = [] #https://developers.google.com/youtube/v3/docs/channels#topicDetails.topicIds[]
		wikiTopicCateg = []
		categories = []

		for ids in  collection["topicDetails"]["topicIds"]:
			topicIDs.append(ids)

		for ids in  collection["topicDetails"]["topicCategories"]:
			wikiTopicCateg.append(ids)
			cat = urlparse.urlparse(ids).path.rsplit("/", 1)[-1]
			categories.append(cat)

	
		if "customUrl" in  collection["snippet"].keys():
			customURL =  collection["snippet"]["customUrl"]
		else:
			customURL = ""
			

		if "country" in  collection["snippet"].keys():
			country =  collection["snippet"]["country"]
		else:
			country = ""

		if "brandingSettings" in  collection.keys():
				if "channel" in  collection["brandingSettings"].keys():
					if "keywords" in  collection["brandingSettings"]["channel"].keys():
						channelKeywords = list(filter(None,set( collection["brandingSettings"]["channel"]["keywords"].split("\""))))
					else:
						channelKeywords = []
					if "featuredChannelsUrls" in collection["brandingSettings"]["channel"].keys():
						featuredChannelsUrls = collection["brandingSettings"]["channel"]["featuredChannelsUrls"]
					else:
						featuredChannelsUrls = []
	
		if "madeForKids" in  collection["status"].keys():
			madeForKids =  str(collection["status"]["madeForKids"]) # boolean : This value indicates whether the channel is designated as child-directed, and it contains the current
		else:
			madeForKids = "NULL"


		basic_info = {
			'channelName' : channelName,
			'channelID': channelID,
			'description': description,
			'createdAt': createdAt,
			'totalViews': totalViews,
			#'totalComments': totalComments,
			'subscribers': subscribers,
			'totalVideos': totalVideos,
			'topicIDs' : topicIDs,
			'wikiTopicCategories' : wikiTopicCateg,
			'categories' : categories,
			'customURL': customURL,
			'country' : country,
			'channelKeywords' : channelKeywords,
			'featuredChannelsUrls' : featuredChannelsUrls,
			'isLinked' : isLinked,
			'madeForKids' : madeForKids
		}
		pprint.pprint(basic_info)


def create_parameters(options):
	
	# channel username for input 	
	if options.user:
		PARAMETERS = {
		'part' :"snippet,contentDetails,statistics,topicDetails,status,contentOwnerDetails,brandingSettings",
		'maxResults' : 50,
		'forUsername': options.user,
		'key': cfg.API_KEY
		}

	# channel id for input or url as input
	else:
		if options.url:
			cid = urlparse.urlparse(options.url).path.rsplit("/", 1)[-1]
		else:
			cid = options.chid

		PARAMETERS = {
		'part' :"snippet,contentDetails,statistics,topicDetails,status,contentOwnerDetails,brandingSettings",
		'maxResults' : 50,
		'id': cid,
		'key': cfg.API_KEY
		}
	
	return PARAMETERS


def main():

	parser = optparse.OptionParser()
	parser.add_option("-n", "--username", dest = "user" , default=False, help="channel username")
	parser.add_option("-i", "--id", dest = "chid", default=False, help="channel ID")
	parser.add_option("-u", "--url", dest = "url" , default=False, help="channel url")
	parser.add_option('-d',"--display", dest = "display", action="store_true", default=False, help="display query response")
	parser.add_option('-b',"--basic", dest = "basic", action="store_true", default=True, help="display query basic info")

	(options,args) = parser.parse_args()

	if options.user == False and options.chid == False and options.url == False:
		parser.print_help()
		sys.exit(1)

	PARAMETERS = create_parameters(options)
			
	response = cfg.requestURL(cfg.CHANNEL_INFO,PARAMETERS) # create url
	result = json.loads(response)

	collection = get_channel_info(result)

	if options.display == True:
		print_collection(collection)

	if options.basic == True:
		get_basic_info(collection)


if __name__ == "__main__":
	main()
