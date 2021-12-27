import discord
import os
import random
from keep_alive import keep_alive
from replit import db
from discord.ext import tasks

client = discord.Client()
# used in dailyMessage(), determines how often to send a message
if "freq" not in db.keys():
    db["freq"] = 5


def updateFacts(fact):
    if "facts" in db.keys():
        facts = db["facts"]
        facts.append(fact)
        db["facts"] = facts
    else:
        db["facts"] = [fact]


def deleteFacts(index):
    index = int(index)
    facts = db["facts"]
    if len(facts) > index:
        del facts[index]
        db["facts"] = facts
        return True


def editFacts(index, edit):
    index = int(index)
    facts = db["facts"]
    if len(facts) > index:
        facts[index] = edit
        return True


def changeFrequency(freq):
    db["freq"] = freq
    dailyMessage.change_interval(seconds=db["freq"])


@client.event
# Display bot is logged on
async def on_ready():
    print("Logged in as {0.user}".format(client))
    dailyMessage.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    # Assume theres always at least one fact in database
    # !fact - Display a random fact
    if msg.startswith("!fact"):
        await message.channel.send("```{}```".format(random.choice(db["facts"])))

    # !add - Add a fact to the database
    elif msg.startswith("!add"):
        try:
            fact = msg.split("!add ", 1)[1]
            await message.channel.send("Fact added")
            updateFacts(fact)
        except IndexError:
            await message.channel.send("Something went wrong, try again.")

    # !delete - Delete a fact from the database
    elif msg.startswith("!delete"):
        try:
            index = msg.split("!delete ", 1)[1]
            facts = db["facts"]
            if deleteFacts(index):
                await message.channel.send("Fact deleted")
            else:
                await message.channel.send("Index out of range")
        except IndexError:
            await message.channel.send("Something went wrong, try again.")

    # !listall - lists all the facts form the database
    elif msg.startswith("!listall"):
        facts = db["facts"]
        if len(facts) == 0:
            await message.channel.send("```There are no facts. Add a fact using !add {string}```")
        else:
            for i in range(len(facts)):
                await message.channel.send("```[{}] {}```".format(i, facts[i]))

    # !help - Display all comands
    elif msg.startswith("!help"):
        await message.channel.send("```!fact - Display a random fact from database \n" +
                                   "!add {string} - Add a fact to the database \n" +
                                   "!delete {index} - Delete selected index from database \n" +
                                   "!listall - Lists all facts from the database \n" +
                                   "!edit {index} {string} - Edit a specified index of the database. The string will completely override the original.\n" +
                                   "!size - Displays the number of facts in the database \n" +
                                   "!freq {int} - Changes the frequency of the daily messages (in seconds) \n" +
                                   "!help - Display list of commands```")

    # !edit - Overwrite a specified index
    elif msg.startswith("!edit"):
        index = msg.split("!edit ", 1)[1]
        try:
            edit = index.split(" ", 1)[1]
            index = index.split(" ", 1)[0]
        except IndexError:
            await message.channel.send("Something went wrong, try again.")
        else:
            await message.channel.send("Editting Fact {}".format(index))
            if (editFacts(index, edit)):
                await message.channel.send("Editting successful")
            else:
                await message.channel.send("Index out of range")

    # !size - Display how many facts are in the database
    elif msg.startswith("!size"):
        await message.channel.send("There are {} facts in my database".format(len(db["facts"])))

    # !freq - Change how often facts are relayed
    elif msg.startswith("!freq"):
        try:
            freq = msg.split("!freq ", 1)[1]
            freq = int(freq.split(" ", 1)[0])
        except IndexError:
            await message.channel.send("Something went wrong, try again.")
        else:
            changeFrequency(freq)
            await message.channel.send("Frequency of daily messages changed to: {} seconds".format(freq))


# Display a random fact every frequency seconds
@tasks.loop(seconds=db["freq"])
async def dailyMessage():
    print(db["freq"])
    # CHANNELID - Channel Id contained in .env
    channel = client.get_channel(int(os.getenv('CHANNELID')))
    await channel.send("```{}```".format(random.choice(db["facts"])))


# Webserver to keep bot constantly running
keep_alive()
client.run(os.getenv('TOKEN'))