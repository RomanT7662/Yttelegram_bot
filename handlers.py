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
