# Import necessary modules
from googleapiclient.discovery import build  # For interacting with the YouTube Data API
from urllib.parse import urlparse, parse_qs  # For parsing URLs and extracting query parameters
from pytube import YouTube  # For retrieving video details like title and duration

# Your YouTube Data API key
YOUTUBE_API_KEY = "AIzaSyAaeSLKD5o_2KQ7B_p_GsQzIiTnYHHL6Jo"

# Function to extract the video ID from a YouTube URL
def extract_id_from_url(video_url):
    parsed_url = urlparse(video_url)  # Parse the given URL
    if parsed_url.netloc == "youtu.be":  # Check if the URL is a short YouTube link
        video_id = parsed_url.path[1:]  # Extract the video ID from the path
    else:
        query_params = parse_qs(parsed_url.query)  # Parse query parameters from the URL
        video_id = query_params.get("v", [""])[0]  # Extract the 'v' parameter (video ID)
    return video_id

# Function to get the title of a YouTube video
def get_video_title(video_url):
    try:
        video = YouTube(video_url)  # Create a YouTube object using the URL
        return video.title  # Return the video's title
    except Exception as e:
        print(f"Error: {e}")  # Print the error if one occurs
        return None  # Return None if an error happens

# Function to get the duration of a YouTube video in seconds
def get_video_duration(video_url):
    try:
        video = YouTube(video_url)  # Create a YouTube object using the URL
        return video.length  # Return the video's duration in seconds
    except Exception as e:
        print(f"Error: {e}")  # Print the error if one occurs
        return None  # Return None if an error happens

# Function to search for playlists similar to a given video title
def search_similar_playlists(video_title, num_playlists, page_token=None):
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)  # Initialize the YouTube API client
        search_response = youtube.search().list(
            q=video_title,  # Search query (video title)
            type="playlist",  # Specify the result type as playlists
            part="id,snippet",  # Specify which data parts to retrieve
            maxResults=num_playlists,  # Maximum number of playlists to retrieve
            pageToken=page_token  # Token for pagination (if needed)
        ).execute()  # Execute the search request

        next_page_token = search_response.get("nextPageToken", None)  # Get the token for the next page of results
        playlists = []
        for item in search_response.get("items", []):  # Loop through the search results
            playlist_id = item["id"]["playlistId"]  # Extract the playlist ID
            playlist_title = item["snippet"]["title"]  # Extract the playlist title
            playlists.append({"playlist_id": playlist_id, "playlist_title": playlist_title})  # Add to the playlist list

        return playlists, next_page_token  # Return the playlists and the next page token

    except Exception as e:
        print(f"Error: {e}")  # Print the error if one occurs
        return [], None  # Return an empty list and None if an error happens

# Function to search for and display playlists based on a query
def search_and_display_playlists(chat_id, query):
    num_playlists = 5  # Number of playlists to retrieve
    playlists, _ = search_similar_playlists(query, num_playlists)  # Call the search function
    if not playlists:  # If no playlists are found
        bot.send_message(chat_id, "Nothing was found for this query.")  # Notify the user
        return

    response = ""  # Initialize the response message
    for idx, playlist in enumerate(playlists, start=1):  # Loop through the playlists
        playlist_title = playlist["playlist_title"]  # Get the playlist title
        playlist_id = playlist["playlist_id"]  # Get the playlist ID
        playlist_link = f"https://www.youtube.com/playlist?list={playlist_id}"  # Construct the playlist link
        response += f"{idx}. {playlist_title}\n{playlist_link}\n\n"  # Append details to the response message

    bot.send_message(chat_id, response)  # Send the response to the user
