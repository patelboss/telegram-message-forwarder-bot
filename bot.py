import os
from dotenv import load_dotenv
import telebot

# Load environment variables from config.env file
load_dotenv(dotenv_path="config.env")

# Retrieve the Telegram Bot token from the environment variable
TOKEN = os.getenv("BOT_TOKEN")

# Retrieve the channel username from the environment variable
channel_username = os.getenv("CHANNEL_USERNAME")

# Create an instance of the bot
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: True)
def forward_message(message):
    # Check if the message is text
    if message.content_type == "text":
        # Forward the message to the channel
        bot.forward_message(
            chat_id=channel_username,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
        )
    elif message.content_type == "photo":
        # Forward the photo to the channel
        bot.send_photo(
            chat_id=channel_username,
            photo=message.photo[-1].file_id,
            caption=message.caption,
        )
    elif message.content_type == "video":
        # Forward the video to the channel
        bot.send_video(
            chat_id=channel_username,
            video=message.video.file_id,
            caption=message.caption,
        )
    # Add more elif blocks for different content types if needed


# Start the bot
bot.polling()
