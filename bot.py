# DISCORD BOT

import discord
from discord.ext import commands
from openai import OpenAI
import random

# Initialize bot and OpenAI
discord_client = commands.Bot(command_prefix="", intents=discord.Intents.all())
openai_client = OpenAI()

# Utility functions for token and API key
def get_file_content(filename):
    with open(filename, "r") as file:
        return file.read()

token = get_file_content("token.txt")
key = get_file_content("OPENAI_API_KEY.txt")

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
        print(f'Server member count: {guild.member_count}')

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
                    response = openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Act as a knowledgeable cat butler."},
                            {"role": "user", "content": args}
                        ]
                    )
                    await message.channel.send(response.choices[0].message.content)
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

            case "help":
                await message.channel.send(
                    """Here is a list of commands: 
                    /butler ping: View current ping.
                    /butler roll: Roll a dice.
                    /butler /chat <prompt>: Chat with GPT.
                    /butler /image <prompt>: Generate an image with DALL-E.
                    /butler help: See list of commands."""
                )

            case _:
                await message.channel.send("Unrecognized command. Use /butler help for a list of commands.")

# Function to run the bot
def run_bot():
    setup_bot()
    discord_client.run(token)
