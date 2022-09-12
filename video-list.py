from apiclient.discovery import build

API_KEY = '{API Key}'
API_VER = 'v3'

youtube = build('youtube', API_VER, developerKey=API_KEY)

def getChannelPlaylistId(channel_id):
  channel = youtube.channels().list(part='snippet,contentDetails', id=channel_id).execute()
  item = channel['items'][0]
  playlist_id = item['contentDetails']['relatedPlaylists']['uploads']
  return playlist_id

def getVideoIds(playlist_id, page_token):
  items_info = youtube.playlistItems().list(part='contentDetails', playlistId=playlist_id, maxResults=50, pageToken=page_token).execute()
  video_ids = list(map(lambda item: item['contentDetails']['videoId'], items_info['items']))
  if 'nextPageToken' in items_info:
    video_ids.extend(getVideoIds(playlist_id, items_info['nextPageToken']))
  return video_ids

def getVideos(video_ids):
  videos = []
  for index, video_id in enumerate(video_ids):
    video_info = youtube.videos().list(part='snippet,statistics', id=video_id).execute()
    videos.extend(video_info['items'])
  return videos

channel_id = 'UC9WJo5ZJVXMZiA5XV2jLx5Q'
playlist_id = getChannelPlaylistId(channel_id)
video_ids = getVideoIds(playlist_id, None)
videos = getVideos(video_ids)

for video in videos:
  print(video['snippet']['title'], ',', 'https://youtube.com/watch?v=' + video['id'])