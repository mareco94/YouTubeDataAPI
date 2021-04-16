#!/usr/bin/env python3

###############################################################
#
# Script Name	:	comments.py
#
# Description	:	Scipt to get:
# 					1) get a video's comment thread [--vid || --vurl]
#							OR
# 					2) get a channel's comment thread [--chid]
#							OR
# 					3) get a info for a comment [--cid]

# 					Returns a list of comment info
#
# 					that match the API request parameters.
#
# Args			:	--vurl [input video URL]
#					--vid [input video ID]
#					--curl [input channel URL]
#					--chid [input channel ID]
#					 --cid [comment ID]
#					-o [respone order] - time || relevance [not in use]
#					--all [get all comments]
# 					-r [get r number of comments] - default 5
#					-d [display basic info] - default True
#					-h [HElP MESSAGE]
#
# Version		:	16-04-2021
#
# Author		:	Maria Oikonomidou
# Email			:	mareco@ics.forth.gr 
# 
###############################################################



import sys
import json
import csv
import pprint
import optparse
import config as cfg
import urllib.parse as urlparse
from urllib.parse import urlencode


def get_comments(items):

	collection = {}
	collection["comments"] = []


	for i in items:
		replies = {}

		if i["kind"] == "youtube#commentThread":
			if "snippet" in i.keys():
				snip = i["snippet"]
			if "replies" in i.keys():
				replies = i["replies"]
			if "id" in i.keys():
				commentID = i["id"]
			if "videoId" in snip.keys():
				videoID = snip["videoId"]

			comment_info = {
				"videoID" : videoID,
				"commentID" : commentID,
				"snippet" : snip,
				"replies" : replies
			}
			collection["comments"].append(comment_info)

	return collection


def create_parameters(options):

	PARAMETERS = {
		'part': 'snippet,replies',
		'key': cfg.API_KEY,
	}

	#order = 'time'
	maxResults = '5' 

	if options.vurl or options.vid:
		if options.vurl:
			url_data = urlparse.urlparse(options.vurl)
			query = urlparse.parse_qs(url_data.query)
			videoId = query["v"][0]
		else:
			videoId = options.vid
	
		PARAMETERS.update({'videoId': videoId})

	elif options.curl or options.chid:
		if options.curl:
			channelId = urlparse.urlparse(options.curl).path.rsplit("/", 1)[-1]
		else:
			channelId = options.chid
	
		PARAMETERS.update({'channelId': channelId})
	elif options.cid:
                cid = options.cid
                PARAMETERS.update({'id': cid})

	#if options.order:
	#	order = str(options.order)

	if options.maxResults:
		if(int(options.maxResults) > 100):
			maxResults = str(100)
		else:
			maxResults = str(options.maxResults)

	if options.all:
		maxResults = str(100)
	
	#PARAMETERS.update({'order': order})
	PARAMETERS.update({'maxResults': maxResults})

	return PARAMETERS

def print_collection(collection):
	for item in collection["comments"]:
		pprint.pprint(item)
		print("\n")


def basic_info(collection):

	counter = 0 

	for item in collection["comments"]:
		videoID = item["videoID"]
		commentID = item["commentID"]
		mainComment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
		authorID = item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
		likes = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
		publishedAt = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]

		basic_info = {
			"videoID" : videoID,
			"commentID" : commentID,
			"author" : authorID, 
			"likes" : likes,
			"publishedAt" : publishedAt,
			"type" : "main",
			"parentCommentID" : commentID,
			"text" : mainComment.replace("\n", " ")
		}
		pprint.pprint(basic_info)

		replies = item["replies"]

		if "comments" in replies.keys():
			replies = item["replies"]["comments"]
			for i in range(len(replies)):
				replies = item["replies"]["comments"][i]
				
				repAuthor = replies["snippet"]["authorChannelId"]["value"]
				repText = replies["snippet"]["textOriginal"]
				publishedAt = replies["snippet"]["updatedAt"]
				likes = replies["snippet"]["likeCount"]
				repID = replies["id"]
				parentCommentID = replies["snippet"]["parentId"]
				videoID = replies["snippet"]["videoId"]

				basic_info = {
					"videoID" : videoID,
					"commentID" : repID,
					"author" : repAuthor, 
					"likes" : likes,
					"publishedAt" : publishedAt,
					"type" : "reply",
					"parentCommentID" : parentCommentID,
					"text" : repText.replace("\n", " ")
				}
				pprint.pprint(basic_info)


def main():

	parser = optparse.OptionParser()
	
	parser.add_option("--vurl", dest = "vurl" , default=False, help="video URL")
	parser.add_option("--vid", dest = "vid", default=False, help="video ID")
	parser.add_option("--curl", dest = "curl" , default=False, help="channel URL")
	parser.add_option("--chid", dest = "chid", default=False, help="channel ID")
	parser.add_option("--cid", dest = "cid", default=False, help="comment ID")
	parser.add_option('-r',"--results", dest = "maxResults", default=False, help="search max result number")
	# parser.add_option('-o',"--order", dest = "order", default=False, help="response order time | relevance")
	parser.add_option("--all", dest = "all", action="store_true", default=False, help="get all comments of a video")
	parser.add_option('-d',"--display", dest = "display", action="store_true", default=True, help="display query response")


	(options,args) = parser.parse_args()

	if options.vurl == False and options.cid == False and options.vid == False and options.curl == False and options.chid == False:
		parser.print_help()
		sys.exit(1)

	PARAMETERS = create_parameters(options)
	response = cfg.requestURL(cfg.COMMENT_THREAD,PARAMETERS) # create url
	result = json.loads(response)

			
	items = []
	counter = 0

	# if "error" in result.keys():
	# 	if str(result["error"]["code"]) == "403":
	# 		if str(result["error"]["errors"][0]["domain"]) == "youtube.quota":
	# 			print(str(result["error"]["code"]), "QUOTA EXPIRE")
	# 			path = 'erroredcommentIDS.txt'
	# 			vids = open(path,"a")
	# 			if "videoId" in PARAMETERS.keys():
	# 				vids.write(PARAMETERS["videoId"]+"\n")
	# 			if "channelId" in PARAMETERS.keys():
	# 				vids.write(PARAMETERS["channelId"]+"\n")
	 	
	# 			vids.close()		
	# 			sys.exit(1)

	if "items" in result.keys():
		for i in result["items"]:
			items.append(i)
			counter+=1


	if options.maxResults:
		nextPageToken = result.get("nextPageToken")
		
		while nextPageToken and int(counter) < int(options.maxResults) :
			PARAMETERS.update({'pageToken': nextPageToken})
			response = cfg.requestURL(cfg.COMMENT_THREAD,PARAMETERS) # create url
			result = json.loads(response)
			if "items" in result.keys():
				for i in result["items"]:
					items.append(i)
					counter +=1 
			nextPageToken = result.get("nextPageToken")

	if options.all:
		nextPageToken = result.get("nextPageToken")
		while nextPageToken:
			
			PARAMETERS.update({'pageToken': nextPageToken})
			response = cfg.requestURL(cfg.COMMENT_THREAD,PARAMETERS) # create url
			result = json.loads(response)

			if "items" in result.keys():
				for i in result["items"]:
					items.append(i)
			
			nextPageToken = result.get("nextPageToken")
		
	collection = get_comments(items)

	if options.display:
		# print_collection(collection)
		basic_info(collection)	

if __name__ == "__main__":
	main()
