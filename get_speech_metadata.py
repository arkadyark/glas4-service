#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import sys, json

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyAPUAJBJU_bvQxTA5dfs7muCp3d2D2qdjA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options, speakers):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY)

    search_videos = []

# Merge video ids
    for line in sys.stdin:
        search_videos.append(line.strip())
        video_ids = ",".join(search_videos)

# Call the videos.list method to retrieve location details for each video.
    video_response = youtube.videos().list(
            id=video_ids,
            part='snippet'
            ).execute()

    metadata = {}

# Add each result to the list, and then display the list of matching videos.
    for video_result in video_response.get("items", []):
        for speaker in speakers:
            if speaker['name'].lower() in video_result["snippet"]["title"].lower():
                speaker_name = speaker['name']
                break
        print speaker_name, video_result['snippet']['publishedAt']

if __name__ == "__main__":
    args = argparser.parse_args()
    speakers = json.loads(open('candidates.json', 'r').read())
    try:
        youtube_search(args, speakers)
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
