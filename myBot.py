import discord
import os

from msgHandler import MessageHandler

# Create a Discord client
client = discord.Client()

# Create an instance of MessageHandler
msgHandler = MessageHandler()

@client.event
async def on_ready():
    print('Bot is ready')

@client.event
async def on_message(msg):
    # To avoid the infinite reply loop
    if msg.author.bot:
        return

    response = msgHandler.processIncomingMessage(msg)
    print('Response --> ', response)
    await msg.channel.send(response)
   
if __name__ == '__main__':
    client.run(os.environ['DISCORD_TOKEN'])