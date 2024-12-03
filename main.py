# os library to use environment variables
# discord and ec2_metadata (They allow us to interact with AWS EC2 & Discord)
# dotenv so we can import the .env file into python
# random to generate random numbers and sequences

import discord
import os
import random
from ec2_metadata import ec2_metadata
from dotenv import load_dotenv

# load the env file
load_dotenv("token.env")

# set the client to the discord client
client = discord.Client()

# get the otken from the env file
token = os.getenv('TOKEN')

#Ensure that the bot has the proper gateway intents, otherwise we can't read user messages
intents = discord.Intents.default()
intents.message_content = True  # Make sure the bot has the proper permissions
intents.messages = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
    username = str(message.author.display_name).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(f'Message {user_message} by {username} on {channel}')

    if message.author == client.user:
        return
# Locates the channel and provides a response only in that channel
# Some features are responsing to hi or hello, bye, tell me a joke, and provides the ec2 meta data (region, IP, and availability zone)
    if channel == "bot":
        if user_message.lower() == "hello" or user_message.lower() == "hi":
            await message.channel.send(f'Hello {username}')
            return
        elif user_message.lower() == "bye":
            await message.channel.send(f'Bye {username}')
        elif user_message.lower() == "tell me a joke":
            jokes = [" Can someone please shed more light on how my lamp got stolen?",
                     "Why is she called llene? She stands on equal legs.",
                     "What do you call a gazelle in a lions territory? Denzel."]
            await message.channel.send(random.choice(jokes))
        elif user_message.lower() == "region":
            await message.channel.send(f'Your EC2 region is {ec2_metadata.region}')
            return
        elif user_message.lower() == "ip":
            await message.channel.send(f'Your public ip is {ec2_metadata.public_ipv4}')
            return
        elif user_message.lower() == "zone":
            await message.channel.send(f'Your availbility zone is {ec2_metadata.availability_zone}')
            return
        elif user_message.lower() == "tell me about my server":
            await message.channel.send(f'Your EC2 region is {ec2_metadata.region}, Your public ip is {ec2_metadata.public_ipv4}, Your availbility zone is {ec2_metadata.availability_zone} ')
            return


client.run(token)











