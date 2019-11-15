from pymongo import MongoClient
import urllib
import motor.motor_asyncio
import os

password = urllib.parse.quote_plus(os.environ['mongoDbPassword'])
mongo_uri = 'mongodb+srv://naushad:%s@sifarmongodb-pvzgj.mongodb.net/test?retryWrites=true&w=majority' % (password)

class DatabaseHandler():
    def __init__(self):
        #self.dbClient   = MongoClient('mongodb+srv://naushad:%s@sifarmongodb-pvzgj.mongodb.net/test?retryWrites=true&w=majority' % (password))
        self.dbClient = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        self.db         = self.dbClient.blueStackDB
        self.collection = self.db.UserSearchHistory

    async def storeUserSearchHistory(self, userName, searchTerm):
        data = {}
        data.update({
            'name': userName,
            'searchhistory': [searchTerm]
        })
        try:
            record = await self.collection.find_one({"name": userName})
            if record:
                await self.collection.update_one(
                                        {'name': userName},
                                        { '$push' : {"searchhistory": searchTerm}} 
                                    )
            else:
                await self.collection.insert_one(data)
        except Exception as e:
            print('Error: Database insert failed : ', e)

    async def getUserSearchHistory(self, userName):
        try:
            record = await self.collection.find_one({"name": userName})
            if record:
                return record['searchhistory']
        except Exception as e:
            print('Error: Database lookup failed : ', e)
        
        return []