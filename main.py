from pyrogram import Client, filters
import os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import subprocess

# Initialize Pyrogram Client
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Define channels
CHANNEL1 = os.getenv("CHANNEL1")
CHANNEL2 = os.getenv("CHANNEL2")

# Store bot start time
bot_start_time = datetime.now()

# Bot start command handler
@app.on_message(filters.command("start"))
def start_command(client, message):
    keyboard = [
        [InlineKeyboardButton("HD/English", callback_data="hd_english"),
         InlineKeyboardButton("Desi", callback_data="desi")],
        [InlineKeyboardButton("Ping", callback_data="ping"),
         InlineKeyboardButton("Uptime", callback_data="uptime")],
        [InlineKeyboardButton("Status", callback_data="status"),
         InlineKeyboardButton("Maintainers", callback_data="maintainers")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply_text("Choose an option:", reply_markup=reply_markup)

# Callback handler
@app.on_callback_query()
def callback_handler(client, query):
    data = query.data
    chat_id = query.message.chat.id
    if data == "hd_english":
        send_random_videos(client, chat_id, CHANNEL1)
    elif data == "desi":
        send_random_videos(client, chat_id, CHANNEL2)
    elif data == "ping":
        ping_server(client, chat_id)
    elif data == "uptime":
        show_uptime(client, chat_id)
    elif data == "status":
        show_status(client, chat_id)
    elif data == "maintainers":
        show_maintainers(client, chat_id)

# Function to send random videos from a channel
def send_random_videos(client, chat_id, channel):
    messages = app.get_chat_history(channel, limit=10)
    video_messages = [message for message in messages if message.video]
    if video_messages:
        for _ in range(10):
            random_video = video_messages.pop(app.random_int(0, len(video_messages) - 1))
            client.send_video(chat_id, random_video.video.file_id, caption=random_video.caption)
    else:
        client.send_message(chat_id, "No videos found in the channel.")

# Function to ping the server and send response time
def ping_server(client, chat_id):
    start_time = datetime.now()
    subprocess.Popen(["ping", "-c", "4", "google.com"]).wait()
    end_time = datetime.now()
    response_time = (end_time - start_time).total_seconds() * 1000
    client.send_message(chat_id, f"Ping response time: {response_time:.2f} ms")

# Function to show bot's uptime
def show_uptime(client, chat_id):
    uptime_duration = datetime.now() - bot_start_time
    client.send_message(chat_id, f"Bot Uptime: {uptime_duration}")

# Function to show status
def show_status(client, chat_id):
    total_files_channel1 = get_total_files(CHANNEL1)
    total_files_channel2 = get_total_files(CHANNEL2)

    status_message = f"#Total Files = {total_files_channel1 + total_files_channel2}\n"
    status_message += f"#Desi= {total_files_channel2}\n"
    status_message += f"#HD= {total_files_channel1}"

    client.send_message(chat_id, status_message)

# Function to get total number of files in a channel
def get_total_files(channel):
    messages = app.get_chat_history(channel)
    total_files = sum(1 for message in messages if message.document or message.video or message.audio)
    return total_files

# Function to show maintainers
def show_maintainers(client, chat_id):
    client.send_message(chat_id, "Maintained By @vishalsharma14 and Team @Movies_Unloaded_Ntework")

# Run the bot
app.run()
