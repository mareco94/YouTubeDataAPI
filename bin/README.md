
### To run add at the config.py.template your API KEY - to get API KEY see [SETUP GUIDE](https://github.com/mareco94/YouTubeAnalytics/tree/master/setup)

### Then change the name of config.py.template to config.py

### READY TO GO!

## :small_blue_diamond: VIDEO INFO  - [./video-info.py]
1) get a video's meatadata\
			OR
2) get most popular videos (YouTube Trends) and their metadata\
Returns a list of videos that match the API request parameters.

```bash
./video-info.py <ARGUMENTS>

# <ARGUMENTS>:
	-i 	#[video id input] -  multiple ids comma seperated 
	-u 	#[video url input] 
	-p 	#[search trending videos] - most popular 
	--region #[search trending videos per region ] - regionCode eg. GR
	-r 	#[max result number] - default 5
	-d 	#[display query response]
	-b 	#[display query basic info] - default stored TRUE
	-h 	#[HElP MESSAGE]

e.g ./video-info.py -u https://www.youtube.com/watch?v=6NXnxTNIWkc
```

## :small_blue_diamond: CHANNEL INFO  - [./channel-info.py]
1) get a channel's information

Returns a collection of zero or more channel resources that match the request criteria.

```bash
./channel-info.py <ARGUMENTS>

# <ARGUMENTS>:
	-i	#[input channel ID]
	-u	#[input channel URL]
	-n	#[input channel name]
	-d	#[display basic info]
	-b 	#[display query basic info] - default stored TRUE
	-h	#[HElP MESSAGE]

e.g ./channel-info.py -i UCtTHxumNZOUhicIbIFeHmug
```

## :small_blue_diamond: PLAYLIST'S ITEMS  - [./playlist-items.py]
1) get a playlist's information

Returns a collection of playlist items that match the API request parameters.
You can retrieve all of the playlist items in a specified playlist.eturns a collection of playlists that match the API request parameters.

```bash
././playlist-items.py <ARGUMENTS>

# <ARGUMENTS>:
	-i #[input playlist ID]
	-u #[input playlist URL]
	-d #[display basic info] - default stored TRUE
	-h #[HElP MESSAGE]

e.g ./playlist-items.py -u https://www.youtube.com/watch?v=BKYWt8B9hgs&list=PLGVZCDnMOq0oX4ymLgldSvpfiZj-S8-fH
```




<!-- 
## :small_blue_diamond: CHANNEL PLAYLISTS  - [./playlists.py]
1) get playlists of a channel\
			OR
2) get a playlist's basic info\
Returns a collection of playlists that match the API request parameters.

```bash
./playlists.py <ARGUMENTS>

# <ARGUMENTS>:
	-i #[video id input] -  multiple ids comma seperated 
	-u #[video url input] 
	-p #[search trending videos] - most popular 
	--region #[search trending videos per region ] - regionCode eg. GR
	-r #[max result number] - default 5
	-d #[display query response]
	-h #[HElP MESSAGE] 
```

## :small_blue_diamond: COMMENT THREAD of a video or a channel - [./comments.py]

1) get a video's comment thread\
			OR
2) get a channel's comment thread\
Returns a list of comment threads that match the API request parameters.

```bash
./video-comments.py <ARGUMENTS>

# <ARGUMENTS>:		
	--vurl	#[input video URL]
	--vid	#[input video ID]
	--curl	#[input channel URL]
	--cid	#[input channel ID]
	-o	#[respone order] - time || relevance
	--all	#[get all comments]
	-r	#[max result number] - default 20
	-d	#[display basic info]
	-h	#[HElP MESSAGE]
```

## :small_blue_diamond: SEARCH QUERY  - [./search.py]

Scipt to search a query at YouTube. Returns a collection of search results that match the query parameters specified in the API request.

```bash
./search.py <ARGUMENTS>

# <ARGUMENTS>:
	-t #[search term]
	-r #[max result number]
	-v #[search videos only]
	-c #[search channels only]
	-p #[search playlists only]
	-b #[search before specifi date]
	-a #[search after specific date]
	-o #[specify result order]
	-s #[query for specifi topic]
	-d #[display query response]
	-f #[get all responses]
	-h #[HElP MESSAGE]
 -->
<!-- ```

<!-- ## :small_blue_diamond: GET SECTIONS of a CHANNEL 
```bash

./channel-sections.py -u  <CHANNEL_URL> #input channel's url

./channel-sections.py -i  <CHANNEL_ID> #input channel's id

./channel-sections.py -n  <CHANNEL_USERNAME> #input channel's name

``` --> 
