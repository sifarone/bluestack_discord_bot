import discord
import os
from googlesearch import search

import utils
from dbOperations import DatabaseHandlerSQLite

# Create a Discord client
client = discord.Client()

#Create a Database handler object
dbClient = DatabaseHandlerSQLite()

@client.event
async def on_ready():
    print('Bot is ready')

@client.event
async def on_message(msg):
    incomingMsg         = msg.content.strip()
    incomingMsgWords    = incomingMsg.split()
    msgWordCount        = len(incomingMsgWords)

    # To avoid the infinite reply loop
    if msg.author.bot:
        return

    if (msgWordCount == 1) and (incomingMsgWords[0] == 'hi'):
        await msg.channel.send('hey')

    elif (msgWordCount > 1) and (incomingMsgWords[0] == '!google'):
        searchTerm = utils.joinWordsToMakeString(incomingMsgWords[1:])
        print('Search Term : ', searchTerm)
        results = []
        for j in search(searchTerm, num=5, start=0, stop=5, pause=2): 
            print(j)
            results.append(j)
        dbClient.storeUserSearchHistory(str(msg.author), searchTerm)
        await msg.channel.send(results)

    elif (msgWordCount > 1) and (incomingMsgWords[0] == '!recent'):
        searchHistoryTerm = utils.joinWordsToMakeString(incomingMsgWords[1:])
        result = []
        searchHistory =  dbClient.getUserSearchHistory(str(msg.author))
        if len(searchHistory):
            for i in searchHistory:
                if searchHistoryTerm in i:
                    result.append(i)
        await msg.channel.send(set(result) if len(result) else result) 
    else:
        await msg.channel.send('< ' + incomingMsg + ' >' + ' is Not Supported.' + ''' 
        Allowed messages:
            1. hi
            2. !google <search term>
            3. !recent <search term>
        ''')    

if __name__ == '__main__':
    client.run(os.environ['DISCORD_TOKEN'])