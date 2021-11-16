# discord api
import discord
from discord.utils import get
import os
import asyncio
# for working with apis 
import requests
import json
# make a server that runs replit constantly
from KeepAlive import keep_alive
# database
from replit import db
import matplotlib.pyplot as plt


client = discord.Client()
sleeptime = 1 # change this to modify how long the bot waites before counting

def makeplot(names , values):
  # make the plot and send it to the chat!
  plt.bar(names, values)
  plt.show()
  plt.savefig(fname='./plooot.png')
  
  

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
  if message.startswith('!f'):
    # return fortune
    await channel.send(get_fortune())

  elif message.startswith('!p'):
    pollmessage = message
    parsed_msg = message.split('-')
    prompt = parsed_msg[1]
    options = parsed_msg[2:]

    # output prompt that user specified
    await channel.send('taking a poll now!\n' + prompt)
    #print out all the options that the user inputed
    bot_msg = ''
    for i in range(len(options)):
      bot_msg += str("\n\t" + str(i+1) + f") {options[i]}")

    # message to react to 
    reactto = await channel.send(bot_msg)
    # numbers for indications
    emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    # add reaction to own bot's message coresponding to the number of options
    for i in range(len(options)):
        await reactto.add_reaction(emoji_numbers[i])

    await asyncio.sleep(sleeptime)  # wait for one minute

    cache_msg = discord.utils.get(client.cached_messages, id=reactto.id)

    # make names and values for plot device
    names = []
    values = []
    print(cache_msg.reactions[:])
    for i in cache_msg.reactions:
      print(i.emoji , i.count)
      names.append(i.emoji)
      values.append(i.count)
    
    plt.bar(options , values)
    plt.savefig("plot.png")
    await channel.send(file=discord.File('plot.png'))
    

# use uptimerobot.com . keeps this script running all the time.
# keep_alive()

# Environment variable is a variable that is private. because this repil is public
# need to hide the TOKEN of the bot.
client.run(os.environ['TOKEN'])