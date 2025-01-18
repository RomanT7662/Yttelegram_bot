# Import necessary modules and functions
import telebot  # Library for interacting with the Telegram Bot API
from youtube_functions import extract_id_from_url, get_video_duration, get_video_title, search_and_display_playlists  # Custom YouTube utility functions

# Define the handler for the /start command
@bot.message_handler(commands=["start"])
def start_handler(message):
    # Sends a welcome message explaining the bot's functionality
    bot.send_message(message.chat.id, "Hello! I am a bot for finding similar playlists on YouTube. Enter a link to a video or playlist:")

# Define the handler for the /filter_duration command
@bot.message_handler(commands=["filter_duration"])
def filter_duration_handler(message):
    query = message.text  # Retrieve the user input
    video_id = extract_id_from_url(query)  # Extract video ID from the provided URL
    if video_id:
        video_url = f"https://www.youtube.com/watch?v={video_id}"  # Construct the video URL
        video_duration = get_video_duration(video_url)  # Get the video's duration
        if video_duration:
            bot.send_message(message.chat.id, f"Video duration: '{video_duration}'")  # Send the duration to the user
        else:
            bot.send_message(message.chat.id, "Failed to retrieve video duration information.")
    else:
        bot.send_message(message.chat.id, "Please enter a valid video URL.")

# Define the handler for general messages
@bot.message_handler(func=lambda message: True)
def message_handler(message):
    query = message.text  # Retrieve the user input

    video_id = extract_id_from_url(query)  # Extract video ID from the provided URL
    if video_id:
        video_url = f"https://www.youtube.com/watch?v={video_id}"  # Construct the video URL
        video_title = get_video_title(video_url)  # Retrieve the video's title
        if video_title:
            bot.send_message(message.chat.id, f"Similar playlists for the video '{video_title}':")
            search_and_display_playlists(message.chat.id, video_title)  # Search for similar playlists
        else:
            bot.send_message(message.chat.id, "Failed to retrieve video information.")
    else:
        bot.send_message(message.chat.id, "Similar playlists for your query:")
        search_and_display_playlists(message.chat.id, query)  # Search for playlists based on the query

# Dictionary to store playlists
playlists = {}

# Define the handler for the /add_playlist command
@bot.message_handler(commands=["add_playlist"])
def handle_add_playlist(message):
    try:
        parts = message.text.split(" ", 2)  # Split the command into parts
        if len(parts) < 3:
            bot.send_message(message.chat.id, "Usage: /add_playlist [playlist_name] [URL]")  # Send usage instructions
            return

        playlist_name = parts[1]  # Extract the playlist name
        playlist_url = parts[2]  # Extract the playlist URL

        if playlist_name in playlists:  # Check if the playlist already exists
            bot.send_message(message.chat.id, f"Playlist '{playlist_name}' already exists.")
        else:
            playlists[playlist_name] = playlist_url  # Add the playlist to the dictionary
            bot.send_message(message.chat.id, f"Playlist '{playlist_name}' added successfully.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error adding playlist: {e}")  # Handle errors gracefully

# Define the handler for the /get_playlist command
@bot.message_handler(commands=["get_playlist"])
def handle_get_playlist(message):
    try:
        parts = message.text.split(" ", 1)  # Split the command into parts
        if len(parts) < 2:
            bot.send_message(message.chat.id, "Usage: /get_playlist [playlist_name]")  # Send usage instructions
            return

        playlist_name = parts[1]  # Extract the playlist name

        if playlist_name in playlists:  # Check if the playlist exists
            bot.send_message(message.chat.id, f"Playlist '{playlist_name}': {playlists[playlist_name]}")
        else:
            bot.send_message(message.chat.id, f"Playlist '{playlist_name}' not found.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error retrieving playlist: {e}")  # Handle errors gracefully

# Define the handler for the /remove_playlist command
@bot.message_handler(commands=["remove_playlist"])
def handle_remove_playlist(message):
    try:
        parts = message.text.split(" ", 1)  # Split the command into parts
        if len(parts) < 2:
            bot.send_message(message.chat.id, "Usage: /remove_playlist [playlist_name]")  # Send usage instructions
            return

        playlist_name = parts[1]  # Extract the playlist name

        if playlist_name in playlists:  # Check if the playlist exists
            del playlists[playlist_name]  # Remove the playlist from the dictionary
            bot.send_message(message.chat.id, f"Playlist '{playlist_name}' removed successfully.")
        else:
            bot.send_message(message.chat.id, f"Playlist '{playlist_name}' not found.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error removing playlist: {e}")  # Handle errors gracefully
