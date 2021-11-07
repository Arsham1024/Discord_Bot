# discord api
import discord
import os
# for working with apis 
import requests
import json
# make a server that runs replit constantly
from KeepAlive import keep_alive
# database
from replit import db


client = discord.Client()


# returns a fortune from the online api
def get_fortune():
  response = requests.get('https://zenquotes.io/api/random').text
  json_data = json.loads(response)
  quote = json_data[0]['q'] + ' \n\t-' + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
  print(f'Hello {client.user}, I\'m online and ready!')


@client.event
async def on_message(message):
  # if the message is from the bot itself ignore
  if message.author == client.user:
    return
  # if message starts with $ it is a command
  if message.content.startswith('$'):
    # return fortune
    await message.channel.send(get_fortune())


# This is the uptimerobot.com . keeps this script running all the time.
keep_alive()

# Environment variable is a variable that is private. because this repil is public
# need to hide the TOKEN of the bot.
client.run(os.environ['TOKEN'])