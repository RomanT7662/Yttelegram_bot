import telebot
from youtube_functions import extract_id_from_url, get_video_duration, get_video_title, search_and_display_playlists

@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.send_message(message.chat.id, "Hello! I am a bot for finding similar playlists on YouTube. Enter a link to a video or playlist:")

@bot.message_handler(commands=["filter_duration"])
def filter_duration_handler(message):
    query = message.text
    video_id = extract_id_from_url(query)
    if video_id:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_duration = get_video_duration(video_url)
        if video_duration:
            bot.send_message(message.chat.id, f"Video duration: '{video_duration}'")
        else:
            bot.send_message(message.chat.id, "Failed to retrieve video duration information.")
    else:
        bot.send_message(message.chat.id, "Please enter a valid video URL.")

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    query = message.text

    video_id = extract_id_from_url(query)
    if video_id:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_title = get_video_title(video_url)
        if video_title:
            bot.send_message(message.chat.id, f"Similar playlists for the video '{video_title}':")
            search_and_display_playlists(message.chat.id, video_title)
        else:
            bot.send_message(message.chat.id, "Failed to retrieve video information.")
    else:
        bot.send_message(message.chat.id, "Similar playlists for your query:")
        search_and_display_playlists(message.chat.id, query)
playlists = {}  

@bot.message_handler(commands=["add_playlist"])
def handle_add_playlist(message):
    try:
        parts = message.text.split(" ", 2)
        if len(parts) < 3:
            bot.send_message(message.chat.id, "Usage: /add_playlist [playlist_name] [URL]")
            return

        playlist_name = parts[1]
        playlist_url = parts[2]

        if playlist_name in playlists:
            bot.send_message(message.chat.id, f"Playlist '{playlist_name}' already exists.")
        else:
            playlists[playlist_name] = playlist_url
            bot.send_message(message.chat.id, f"Playlist '{playlist_name}' added successfully.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error adding playlist: {e}")

@bot.message_handler(commands=["get_playlist"])
def handle_get_playlist(message):
    try:
        parts = message.text.split(" ", 1)
        if len(parts) < 2:
            bot.send_message(message.chat.id, "Usage: /get_playlist [playlist_name]")
            return

        playlist_name = parts[1]

        if playlist_name in playlists:
            bot.send_message(message.chat.id, f"Playlist '{playlist_name}': {playlists[playlist_name]}")
        else:
            bot.send_message(message.chat.id, f"Playlist '{playlist_name}' not found.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error retrieving playlist: {e}")

@bot.message_handler(commands=["remove_playlist"])
def handle_remove_playlist(message):
    try:
        parts = message.text.split(" ", 1)
        if len(parts) < 2:
            bot.send_message(message.chat.id, "Usage: /remove_playlist [playlist_name]")
            return

        playlist_name = parts[1]

        if playlist_name in playlists:
            del playlists[playlist_name]
            bot.send_message(message.chat.id, f"Playlist '{playlist_name}' removed successfully.")
        else:
            bot.send_message(message.chat.id, f"Playlist '{playlist_name}' not found.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error removing playlist: {e}")

