# DISCORD BOT

import asyncio
import discord
from discord.ext import commands
from openai import OpenAI
import random
import os
import yt_dlp
from dotenv import load_dotenv


# Initialize bot and OpenAI
discord_client = commands.Bot(command_prefix="", intents=discord.Intents.all())
openai_client = OpenAI()

# Utility functions for token and API key
def get_file_content(filename):
    with open(filename, "r") as file:
        return file.read()

token = get_file_content("token.txt")
key = get_file_content("OPENAI_API_KEY.txt")

# A dictionary to store conversation history for each user
conversation_history = {}

# Vairables to store audio metadata
queues = {}
voice_clients = {}
yt_dl_options = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192"
    }]
}
yt_dl = yt_dlp.YoutubeDL(yt_dl_options)

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}

# Helper function to parse user commands
def extract_command_and_args(message_content, prefix="/butler"):
    if message_content.startswith(prefix):
        components = message_content[len(prefix):].strip().split(" ", 1)
        command = components[0]
        args = components[1] if len(components) > 1 else ""
        return command, args
    return None, None

# Define bot event handlers
def setup_bot():
    @discord_client.event
    async def on_ready():
        print(f'{discord_client.user} is logged in')

        guild = discord_client.guilds[0]
        bot_member = guild.get_member(discord_client.user.id)

        roles = bot_member.roles
        role_names = [role.name for role in roles]
        
        permissions = bot_member.guild_permissions
        permission_integer = permissions.value
        
        print(f'Roles assigned to the bot: {", ".join(role_names)}')
        print(f'Bot Permission Integer: {permission_integer}')
        print(f'Connected to server: {guild.name} (ID: {guild.id})')
        print(f'Server member count (including bot): {guild.member_count}')

    @discord_client.event
    async def on_message(message):
        if message.author.id == discord_client.user.id:
            return

        command, args = extract_command_and_args(message.content)
        if not command:
            return

        match command:
            case "ping":
                latency = round(discord_client.latency * 1000)
                await message.channel.send(f"Pong!... {latency}ms")

            case "roll":
                roll_result = random.randint(1, 6)
                await message.channel.send(f"You rolled a {roll_result}!")

            case "/chat":
                openai_client.api_key = key
                try:
                    # Get the user's unique ID
                    user_id = str(message.author.id)

                    # Initialize the conversation history for the user if not present
                    if user_id not in conversation_history:
                        conversation_history[user_id] = [
                            {"role": "system", "content": "Act as a knowledgeable cat butler."}
                        ]
                    
                    # Append the user's message to the conversation history
                    conversation_history[user_id].append({"role": "user", "content": args})
                    
                    # Make the API call with the conversation history
                    response = openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=conversation_history[user_id]
                    )
                    
                    # Get the bot's response and add it to the conversation history
                    bot_message = response.choices[0].message.content
                    conversation_history[user_id].append({"role": "assistant", "content": bot_message})
                    
                    # Send the bot's response to the channel
                    await message.channel.send(bot_message)
                except Exception:
                    await message.channel.send("Error communicating with GPT.")

            case "/image":
                openai_client.api_key = key
                try:
                    response = openai_client.images.generate(
                        model="dall-e-3",
                        prompt=args,
                        size="1024x1024",
                        n=1
                    )
                    await message.channel.send(response.data[0].url)
                except Exception:
                    await message.channel.send("Error generating image.")

            case "/play":
                try:
                    # Check if the user is in a voice channel
                    if message.author.voice is None:
                        await message.channel.send("You must be in a voice channel to use this command.")
                        return
                    # Connect to the user's voice channel
                    voice_channel = message.author.voice.channel
                    guild_id = message.guild.id

                    if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
                        voice_client = await voice_channel.connect()
                        voice_clients[guild_id] = voice_client
                    else:
                        voice_client = voice_clients[guild_id]
                except Exception as e:
                    await message.channel.send(f"Error joining voice channel: {str(e)}")
                    return
                try:
                    load_dotenv()
                    # Get the URL and extract audio
                    url = args
                    loop = asyncio.get_event_loop()
                    data = await loop.run_in_executor(None, lambda: yt_dl.extract_info(url, download=False))
                    song = data["url"]
                    # Create an audio player and play the song
                    player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
                    if not voice_client.is_playing():
                        voice_client.play(player, after=lambda e: print("Song playback finished."))
                        await message.channel.send(f"Now playing: {data.get('title', 'Unknown')}")
                    else:
                        await message.channel.send("Already playing a song. Please wait for it to finish.")
                except Exception as e:
                    await message.channel.send(f"Error playing song: {str(e)}")
            case "pause":
                try:
                    guild_id = message.guild.id
                    if guild_id in voice_clients and voice_clients[guild_id].is_playing():
                        voice_clients[guild_id].pause()
                        await message.channel.send("Playback paused.")
                    else:
                        await message.channel.send("No song is currently playing.")
                except Exception as e:
                    await message.channel.send(f"Error pausing playback: {str(e)}")
            case "resume":
                try:
                    guild_id = message.guild.id
                    if guild_id in voice_clients and voice_clients[guild_id].is_paused():
                        voice_clients[guild_id].resume()
                        await message.channel.send("Playback resumed.")
                    else:
                        await message.channel.send("No song is currently paused.")
                except Exception as e:
                    await message.channel.send(f"Error resuming playback: {str(e)}")
            case "stop":
                try:
                    guild_id = message.guild.id
                    if guild_id in voice_clients:
                        voice_clients[guild_id].stop()
                        await voice_clients[guild_id].disconnect()
                        del voice_clients[guild_id]
                        await message.channel.send("Playback stopped and disconnected from the voice channel.")
                    else:
                        await message.channel.send("No active playback to stop.")
                except Exception as e:
                    await message.channel.send(f"Error stopping playback: {str(e)}")

            case "help":
                await message.channel.send(
                    """Here is a list of commands:
                    \n/butler ping: View current ping.
                    \n/butler roll: Roll a dice.
                    \n/butler /chat <prompt>: Chat with GPT.
                    \n/butler /image <prompt>: Generate an image with DALL-E.
                    \n/butler /play <url>: Play a song.
                    \n/butler pause: Pause the current song.
                    \n/butler resume: Resume the current song.
                    \n/butler stop: Stop the current song.
                    \n/butler help: See list of commands."""
                )

            case _:
                await message.channel.send("Whatchu sayin bro. Use /butler help for a list of commands.")

# Function to run the bot
def run_bot():
    setup_bot()
    discord_client.run(token)
