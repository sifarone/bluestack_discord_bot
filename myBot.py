import discord
from googlesearch import search
from discord.ext import commands

import utils
from dbOperations import DatabaseHandler

TOKEN = 'NjQ0NzU2NjQ5MjYwODc1Nzg3.Xc4vBQ.l4PFVeZw4cG7UuGuwuZqlKg-Z9E'

client = discord.Client()

dbClient = DatabaseHandler()

@client.event
async def on_ready():
    print('Bot is ready')

@client.event
async def on_message(msg):
    #print('memeber: ', msg.author)

    incomingMsg         = msg.content.strip()
    incomingMsgWords    = incomingMsg.split()
    msgWordCount        = len(incomingMsgWords)

    if msg.author.bot:
        return

    if (msgWordCount == 1) and (incomingMsgWords[0] == 'hi'):
        await msg.channel.send('hey')

    elif (msgWordCount > 1) and (incomingMsgWords[0] == '!google'):
        searchTerm = utils.joinWordsToMakeString(incomingMsgWords[1:])
        print('--> : ', searchTerm)
        results = []
        for j in search(searchTerm, num=5, start=0, stop=5, pause=2): 
            print(j)
            results.append(j)
        await dbClient.storeUserSearchHistory(str(msg.author), searchTerm)
        await msg.channel.send(results)

    elif (msgWordCount > 1) and (incomingMsgWords[0] == '!recent'):
        searchHistoryTerm = utils.joinWordsToMakeString(incomingMsgWords[1:])
        result = []
        searchHistory =  await dbClient.getUserSearchHistory(str(msg.author))
        if len(searchHistory):
            for i in searchHistory:
                if searchHistoryTerm in i:
                    result.append(i)
        await msg.channel.send(set(result)) 
    else:
        await msg.channel.send('< ' + incomingMsg + ' >' + ' is Not Supported.' + ''' 
        Allowed messages:
            1. hi
            2. !google <search term>
            3. !recent <search term>
        ''')    

if __name__ == '__main__':
    client.run(TOKEN)