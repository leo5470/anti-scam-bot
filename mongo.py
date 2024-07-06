from pymongo.mongo_client import MongoClient

import os

from dotenv import load_dotenv

class MongoDBClient:
    def __init__(self):
        # DEBUG
        load_dotenv()

        self.mongo_password = os.environ['MONGO_PASSWORD']
        print(self.mongo_password)
        self.mongo_uri = f"mongodb+srv://leo5470:{self.mongo_password}@sitcon24.7letp2e.mongodb.net/?appName=SITCON24"
        print(self.mongo_uri)
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client['anti-fraud']
        self.collection = self.db['data']
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def newUser(self, userID):
        document = self.findByUserID(userID)
        if document == None:
            return
        new_document = {
        "user_id": userID,  # Replace with your desired id
        "groups": {},
        "chat_history": []
        }
        result = self.collection.insert_one(new_document)
        print(f"Inserted document ID: {result.inserted_id}")
    
    def findByUserID(self, userID):
        document = self.collection.find_one({"user_id": userID})
        return document
    
    def updateDocument(self, userID, updated_document):
        self.collection.update_one({"user_id": userID}, {"$set": updated_document})
    
    def insertGroup(self, userID, groupID):
        document = self.findByUserID(userID)
        document["groups"].update(
            {
                groupID: []
            }
        )
        self.updateDocument(userID, document)
    
    def updateChatHistory(self, userID, user, assistant):
        document = self.findByUserID(userID)
        document["chat_history"].append(
            {
                "role": "user",
                "content": user
            }
        )
        document["chat_history"].append(
            {
                "role": "assistant",
                "content": assistant
            }
        )
        self.updateDocument(userID, document)
    
    def updateGroupHistory(self, userID, groupID, user=None, counter=None):
        document = self.findByUserID(userID)
        if user:
            document["groups"][groupID].append(
                {
                    "role": "user",
                    "content": user
                }
            )
        if counter:
            document["groups"][groupID].append(
                {
                    "role": "counterpart",
                    "content": counter
                }
            )
        self.updateDocument(userID, document)
    
    def clearChatHistory(self, userID):
        document = self.findByUserID(userID)
        document["chat_history"] = []
        self.updateDocument(userID, document)
    
    def clearGroupHistory(self, userID, groupID):
        document = self.findByUserID(userID)
        document["groups"][groupID] = []
        self.updateDocument(userID, document)