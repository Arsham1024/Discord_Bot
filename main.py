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
async def on_message(message1):
  # for parsing the message1
  message = message1.content
  channel = message1.channel

  # if the message is from the bot itself ignore
  if message1.author == client.user:
    return
  # if message starts with $ it is a command
  if message.startswith('$f'):
    # return fortune
    await channel.send(get_fortune())

  elif message.startswith('$p'):
    parsed_msg = message.split('-')
    prompt = parsed_msg[1]
    options = parsed_msg[2:]

    # output prompt that user specified
    await channel.send('taking a poll now!\n' + prompt)
    #print out all the options that the user inputed
    bot_msg = ''
    for i in range(len(options)):
      bot_msg += str("\n\t" + str(i+1) + f") {options[i]}")

    reactto = await channel.send(bot_msg)

    # add reaction to own bot's message
    for i in range(10):
      await reactto.add_reaction('\U0001F43D')



# use uptimerobot.com . keeps this script running all the time.
keep_alive()

# Environment variable is a variable that is private. because this repil is public
# need to hide the TOKEN of the bot.
client.run(os.environ['TOKEN'])