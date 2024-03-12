#DISCORD BOT

import discord
from discord.ext import commands
from openai import OpenAI
import random
import time

discord_client = commands.Bot(command_prefix = "!", intents = discord.Intents.all())
openai_client = OpenAI()


def get_token():
    with open("token.txt", "r") as token_file:
        token = token_file.read()
        return token
token = get_token()

def get_OPENAI_API_KEY():
    with open("OPENAI_API_KEY.txt", "r") as key_file:
        key = key_file.read()
        return key
key = get_OPENAI_API_KEY()


def run_bot():
    @discord_client.event
    async def on_ready():
        print(f'{discord_client.user} is logged in')
        return 
    
    @discord_client.event
    async def on_message(message):
        user_message = message.content
        user_message.lower()

        if message.author.id == discord_client.user.id:
            return
        
        if user_message.startswith("/butler"):
            command_prefix = user_message.split(" ")[0] # command_prefix = "/butler"
            actual_message = user_message.replace(command_prefix, "")[1:] # all text after "/butler "
            first_phrase = actual_message.split(" ")[0] # the first phrase after "/butler " (ex. "/butler roll the balls" -> "roll")
            match first_phrase:
                #1
                case "hello":
                    await message.channel.send("Hiiiiiiiiiii :3")
                #2
                case "hi":
                    await message.channel.send("Heloooooooooooo :3 :3")
                #3
                case "ping":
                    bot_latency = round(discord_client.latency*1000)
                    await message.channel.send("Pong!... " + str(bot_latency) + "ms")
                #4
                case "cuss":
                    name = ["Dan", "Khang", "Phuc", "Phat"]
                    i = random.randrange(0, len(name))
                    await message.channel.send(name[i] + " ngu :333")
                    j = random.randrange(0, 2)
                    if j == 0:
                        await message.author.send("May ngu qua hahahah :33333")
                #5
                case "roll":
                    await message.channel.send("You rolled a " + str(random.randrange(0, 7)) + "!")
                #6
                case "danngu":
                    num = random.randrange(0, 10)
                    for i in range(0, num):
                        await message.channel.send("cuc cut dan <@564069718458368000>")
                        time.sleep(1)
                    await message.channel.send('I said "cuc cut dan" ' + str(num) + " times!")
                #7
                case "lobotomykaisen":
                    await message.channel.send("This feature is not yet complete")
                #8
                case "christmastree":
                    tree_height = int(actual_message[14:])
                    num_star = 1
                    for row in range(0, tree_height):
                        num_spaces = int((tree_height*2 -1 - num_star)/2)
                        await message.channel.send("-"*num_spaces + "^"*num_star + "-"*num_spaces)
                        num_star += 2

                #9
                case "happynumber":
                    num = actual_message[12:]
                    bad_nums = []
                    current_num = int(num)
                    while current_num not in bad_nums:
                        summ = 0
                        for digit in str(current_num):
                            summ += int(digit)**2
                            if summ == 1:
                                await message.channel.send("This number is happy!")
                                return
                            else:
                                bad_nums.append(summ)
                                current_num = summ
                    await message.channel.send("This number is not happy!")
                #10
                case "staircase":
                    num = int(actual_message[10:])
                    if num == 0 or num == 1:
                        await message.channel.send("There is only 1 way to reach the top of the staircase of length 0 or 1!")
                        return
                    prev, curr = 1, 1 # 2 first number in the Fibonacci sequence
                    for i in range(1, num): # (1, 1, 2, 3, 5, 8, ...) -> loop n-1 times (we start at i=1). Ex: 4 staircase -> 5 solutions; start at i=1 so need to loop 3 more times
                        temp = curr
                        curr += prev
                        prev = temp
                    await message.channel.send(f'There are {curr} ways to reach the top of a staircase of length {num}!')
                #10        
                case "/rps":
                    throw = ["rock", "paper", "scissor"]
                    user_throw = actual_message[5:]
                    user_throw.lower()
                    i = random.randrange(0, len(throw))
                    match user_throw:
                        case "rock":
                            if throw[i] == "rock":
                                await message.channel.send("I throw " + throw[i] + "!" "\nIt's a draw!")
                            elif throw[i] == "paper":
                                await message.channel.send("I throw " + throw[i] + "!" "\nCongrats u won!")
                            else:
                                await message.channel.send("I throw " + throw[i] + "!" "\nhahahah I won!")
                        case "paper":
                            if throw[i] == "paper":
                                await message.channel.send("I throw " + throw[i] + "!" "\nIt's a draw!")
                            elif throw[i] == "rock":
                                await message.channel.send("I throw " + throw[i] + "!" "\nCongrats u won!")
                            else:
                                await message.channel.send("I throw " + throw[i] + "!" "\nhahahah I won!")
                        case "scissor":
                            if throw[i] == "scissor":
                                await message.channel.send("I throw " + throw[i] + "!" "\nIt's a draw!")
                            elif throw[i] == "rock":
                                await message.channel.send("I throw " + throw[i] + "!" "\nCongrats u won!")
                            else:
                                await message.channel.send("I throw " + throw[i] + "!" "\nhahahah I won!")
                        case _:
                            await message.channel.send("Dumbass what that \n(Use command to play again)")
                #11
                case "/chat":
                    gpt_prompt = actual_message[5:]
                    gpt_response = openai_client.chat.completions.create(
                        model = "gpt-3.5-turbo",
                        messages = [
                            {"role": "system", "content": "Act as a cat that has been assigned as a butler (You are very knowledgeable and have Ph.Ds in everything). Provide detailed answers, explanations and examples to all questions. Always be concise yet informative."},
                            {"role": "assistant", "content": gpt_prompt},
                            {"role": "user", "content": gpt_prompt}
                        ]
                    )
                    extracted_gpt_response = gpt_response.choices[0].message.content
                    await message.channel.send(extracted_gpt_response)
                #12
                case "/image":
                    try:
                        dalle__prompt = actual_message[7:]
                        dalle__response = openai_client.images.generate(
                            model = "dall-e-3",
                            prompt = dalle__prompt,
                            size = "1024x1024",
                            quality = "standard",
                            n = 1
                        )
                        image_url = dalle__response.data[0].url
                        await message.channel.send(image_url)
                    except:
                        await message.channel.send("You must have said something bad, the AI stopped responding.")
                #13
                case "help":
                    await message.channel.send("""Here is a list of commands: 
                                               \n/butler [hello/hi]: Say hello 
                                               \n/butler ping: View current ping 
                                               \n/butler cuss: Cuss at a random person (50/50 chance bot private message you!) 
                                               \n/butler roll: Roll a dice
                                               \n/butler danngu: chui thang hua the dan
                                               \n/butler lobotomykaisen: lobotomy kaisen
                                               \n/butler christmastree [num]: Print a christmas tree with input height
                                               \n/butler happynumber [num]: Check if number is happy
                                               \n/butler staircase [num]: Check how many ways you can reach the top of a staicase of length num
                                               \n/butler /rps [rock/paper/scissor]: Play rock paper scissor! 
                                               \n/butler /chat [prompt]: Enter prompt to chat with AI
                                               \n/butler /image [prompt]: Enter prompt to generate an image with AI
                                               \n/butler help: See list of commands""")
                #default    
                case _:
                    await message.channel.send("tf u sayin")

    discord_client.run(token)