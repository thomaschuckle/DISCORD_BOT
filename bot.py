#DISCORD BOT

#Importing neccessary libraries.
import discord
from discord.ext import commands
from openai import OpenAI
import random
import time

#Initializing bot and openai.
discord_client = commands.Bot(command_prefix = "", intents = discord.Intents.all()) #Command prefix is set to nothing as custome prefix will be set later on.
openai_client = OpenAI()

#Method for getting token.
def get_token():
    with open("token.txt", "r") as token_file:
        token = token_file.read()
        return token
token = get_token()

#Method for getting openai api key.
def get_OPENAI_API_KEY():
    with open("OPENAI_API_KEY.txt", "r") as key_file:
        key = key_file.read()
        return key
key = get_OPENAI_API_KEY()

#Method for runnning the bot.
def run_bot():
    @discord_client.event
    async def on_ready():
        print(f'{discord_client.user} is logged in') #Message printed in console to indicate successful bot log in.
        return 
    
    @discord_client.event
    async def on_message(message):
        user_message = message.content          #Registering what user sent to the server. Contains every characters of the message.
        user_message.lower()                    #Lowercase the message for easier processing later on.

        if message.author.id == discord_client.user.id: #If case to return nothing when the bot send a message to avoid message registering confusion.
                                                        #We dont want the bot to be the user calling out commands.
            return
        
        if user_message.startswith("/butler"):              #If case to run commands:
            command_prefix = user_message.split(" ")[0]     #Set command_prefix to "/butler". 
                                                            #Delimeter " " is used to split the contents of the user's message.

            actual_message = user_message.replace(command_prefix, "")[1:]   #All text after "/butler ", 
                                                                            #which contains the actual message without the prefix.

            first_phrase = actual_message.split(" ")[0] #The first phrase after "/butler " (ex. "/butler roll" -> "roll")
                                                        #First phrases will be evaluated to check for which commands to run.

            match first_phrase:
                #1st command, get the latency of the bot:
                case "ping":                                                            
                    bot_latency = round(discord_client.latency*1000)                    #Convert seconds to milliseconds and round it to the tenth digit.
                    await message.channel.send("Pong!... " + str(bot_latency) + "ms")   #Send message to the server.


                #2nd command, randomly choose a person:
                case "random":                                  
                    name = ["Dan", "Khang", "Phuc", "Phat"]     #List of server member's names.
                    i = random.randrange(0, len(name))          #Randomly generate an index.
                    await message.channel.send(name[i] + "was the chosen one!") #Send message to the server.
                    j = random.randrange(0, 2)                                  #Randomly generate a number (0 or 1) to private message the command caller.
                    if j == 0:
                        await message.author.send("You are the chosen one!")    #Send message privately to the command caller.


                #3rd command, randomly roll a number
                case "roll":                                                                       
                    await message.channel.send("You rolled a " + str(random.randrange(0, 7)) + "!") #Generate a random number from 1-6 and send it to the server.


                #4th command, print a tree using ASCII characters with specified height:
                case "tree":                                    
                    tree_height = int(actual_message[14:])      #Hard-code to get the specified tree height from "actual message" at index 14.
                    num_star = 1

                    for _ in range(0, tree_height):                         #For loop to construct tree (number of iterations = height of tree)
                        num_spaces = int((tree_height*2 -1 - num_star)/2)   #Calculate the number of spaces before constructing a layer of the tree based on a formula.
                        await message.channel.send("-"*num_spaces + "^"*num_star + "-"*num_spaces)  #Print out each layer of the tree.
                        num_star += 2                                                               #Increment number of starts by 2.
                

                #5th command, check if a number is happy. This command is based on google's frequently asked interview question (https://leetcode.com/problems/happy-number/description/). 
                case "happynumber":                 
                    num = actual_message[12:]       #Hard-code to get the specified number from "actual_message" at index 12.
                    bad_nums = []                   #Array to store bad numbers.
                    current_num = int(num)          #Convert num from string to integer.

                    while current_num not in bad_nums:      #Loop to continuosly check if number is happy if it is not in bad_nums.
                        summ = 0
                        for digit in str(current_num):      #Loop to loop through the digits that makes up the number:
                            summ += int(digit)**2           #Sum the digits squared.
                        if summ == 1:                       #If sum is 1, print message and return:
                            await message.channel.send("This number is happy!")
                            return
                        else:                               #Else, append that number to bad nums, and set current num to the sum.
                            bad_nums.append(summ)
                            current_num = summ
                    await message.channel.send("This number is not happy!") #If the while loop exits, this number cannot be happy.

               
                #6th command, calculate the number of ways you can reach a staircase with specified steps using the fibonacci sequence.
                case "staircase":                       
                    steps = int(actual_message[10:])    #Hard-code to get the specified steps from "actual_message".
                    if steps == 0 or steps == 1:        #If give a staricase with only 0 or 1 steps, there is only 1 solution.
                        await message.channel.send("There is only 1 way to reach the top of the staircase of length 0 or 1!")
                        return
                    prev, curr = 0, 1           #First 2 numbers of the Fibonacci sequence.
                    for i in range(0, steps):   #Number of staircase steps = number of iterations. Number of all possible ways = prev + curr.
                        temp = curr
                        curr += prev
                        prev = temp
                    await message.channel.send(f'There are {curr} ways to reach the top of a staircase of length {steps}!')
                

                #7th command, play rock paper scissor.        
                case "/rps":
                    throw = ["rock", "paper", "scissor"]    #Thwroable options from the bot.
                    user_throw = actual_message[5:]         #Hard code to get what user thrown from "actual_message" at index 5.
                    i = random.randrange(0, len(throw))     #Randomly generate an index for the bot to throw something.
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
                

                #8th command, chat with OpenAI's GPT 3.5 Turbo.
                case "/chat":
                    gpt_prompt = actual_message[5:] #Hard code to get the prompt from user in "actual_message" at index 5.
                    gpt_response = openai_client.chat.completions.create(
                        model = "gpt-3.5-turbo",
                        messages = [
                            {"role": "system", "content": "Act as a cat that has been assigned as a butler (You are very knowledgeable and have Ph.Ds in everything). Provide detailed answers, explanations and examples to all questions. Always be concise yet informative."}, #Tuning the model by prompting it to act like a butler cat.
                            {"role": "assistant", "content": gpt_prompt},   #Assisting prompt for the model.
                            {"role": "user", "content": gpt_prompt}         #User's prompt goes here.
                        ]
                    )
                    extracted_gpt_response = gpt_response.choices[0].message.content    #Extract the message from the API's response.
                    await message.channel.send(extracted_gpt_response)                  #Send the message to channel.
                

                #9th command, generate images with OpenAI's DALL-E 3.
                case "/image":
                    try:
                        dalle__prompt = actual_message[7:] #Hard code to get the prompt from user in "actual_message" at index 7.
                        dalle__response = openai_client.images.generate(
                            model = "dall-e-3",         #Set model to DALL-E 3.
                            prompt = dalle__prompt,     #Set prompt.
                            size = "1024x1024",         #Set image size to 1024x1024 pixels.
                            quality = "standard",       #Set standard image quality.
                            n = 1                       #Set number of images to generate.
                        )
                        image_url = dalle__response.data[0].url     #Extract url to the image.
                        await message.channel.send(image_url)       #Send the url to the server.
                    except:
                        await message.channel.send("You must have said something bad, the AI stopped responding.")  #Exception in case model cannot generate the image.
                

                #10th command, print out a list of commands.
                case "help":
                    await message.channel.send("""Here is a list of commands: 
                                               \n/butler ping: View current ping.
                                               \n/butler random: Randomly choose a person (50/50 chance bot private message you!).
                                               \n/butler roll: Roll a dice.
                                               \n/butler tree <height>: Print a tree with specified height.
                                               \n/butler happynumber <num>: Check if number is happy.
                                               \n/butler staircase <steps>: Check how many ways you can reach the top of a staicase with specified steps.
                                               \n/butler /rps <rock/paper/scissor>: Play rock paper scissor! 
                                               \n/butler /chat <prompt>: Enter prompt to chat with GPT 3.5 Turbo.
                                               \n/butler /image <prompt>: Enter prompt to generate an image with Dall_E.
                                               \n/butler help: See list of commands.""")
                #default    
                case _:
                    await message.channel.send("I dont recognize this command, perhaps use \"/butler help\" to check for a list of avaiable commands?")     #Default message if the command is invalid.

    discord_client.run(token) #Run bot when run_bot() method is called.