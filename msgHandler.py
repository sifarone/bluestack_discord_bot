import utils
from googlesearch import search
from dbOperations import DatabaseHandlerSQLite

class MessageHandler():
    def __init__(self):
        self.supportedMessageTypes  = ['hi', '!google', '!recent']
        self.dbClient               = DatabaseHandlerSQLite()

    def addNewMessageTypes(self, msgType):
        self.allowedMessageTypes.append(str(msgType).strip())

    def getSupportedMsgTypes(self):
        return self.supportedMessageTypes

    def processIncomingMessage(self, msg):
        incomingMsg         = msg.content.strip()
        incomingMsgWords    = incomingMsg.split()
        msgWordCount        = len(incomingMsgWords)

        if msgWordCount and incomingMsgWords[0] not in self.getSupportedMsgTypes():
            return ('Message : < ' + incomingMsgWords[0] + ' >' 
                    + ' is Not Supported.\n' 
                    + 'Supported Messages : ' 
                    + str(self.getSupportedMsgTypes()))

        elif msgWordCount == 1 and incomingMsgWords[0] == 'hi':
            return 'hey'

        elif msgWordCount > 1 and incomingMsgWords[0] == '!google':
            searchTerm = utils.joinWordsToMakeString(incomingMsgWords[1:])
            print('Search Term : ', searchTerm)
            results = []
            for j in search(searchTerm, num=5, start=0, stop=5, pause=2): 
                results.append(utils.decodeUrls(j))
            self.dbClient.storeUserSearchHistory(str(msg.author), searchTerm)
            return "Search results for : <" + searchTerm + '> \n' +  str(results)

        elif msgWordCount > 1 and incomingMsgWords[0] == '!recent':
            searchHistoryTerm = utils.joinWordsToMakeString(incomingMsgWords[1:])
            result = []
            searchHistory =  self.dbClient.getUserSearchHistory(str(msg.author))
            if len(searchHistory):
                result = [term for term in searchHistory if searchHistoryTerm in term]
                
            if result:
                return "Search History for : <" + searchHistoryTerm + '> \n' + str(result)
            else:
                return "No Search History for : <" + searchHistoryTerm + '>'

        else:
            return 'Invalid Message'
