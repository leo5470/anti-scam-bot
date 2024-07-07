from pymongo.mongo_client import MongoClient

import os

from dotenv import load_dotenv
import json

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
        self.groupCollection = self.db['group']
        self.suggestCollection = self.db['suggest']
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def newUser(self, userID):
        document = self.findByUserID(userID)
        if document != None:
            return
        new_document = {
            "user_id": userID,
            "suggestFlag": False,
            "groups": {},
            "chat_history": []
        }
        new_suggest_document = {
            "user_id": userID,
            "history": []
        }
        result = self.collection.insert_one(new_document)
        self.suggestCollection.insert_one(new_suggest_document)
        print(f"Inserted document ID: {result.inserted_id}")
    
    def findByUserID(self, userID):
        document = self.collection.find_one({"user_id": userID})
        return document
    
    def findByGroupID(self, groupID):
        document = self.groupCollection.find_one({"group_id": groupID})
        return document
    
    def findByGroupName(self, groupName):
        document = self.groupCollection.find_one({"group_name": groupName})
        return document
    
    def getSuggestFlag(self, userID):
        document = self.findByUserID(userID)
        return document["suggestFlag"]
    
    def getGroupOwner(self, groupID):
        document = self.groupCollection.find_one({"group_id": groupID})
        return document["owner"]

    
    def getGroupsInfo(self, userID):
        document = self.findByUserID(userID)
        group_keys = list(document["groups"].keys())
        infoList = []
        for key in group_keys:
            groupDocument = self.groupCollection.find_one({"group_id": key})
            infoList.append(groupDocument["group_name"])
        return infoList
    
    def getGroupHistory(self, groupName=None, groupID=None):
        if groupName != None:
            document = self.findByGroupName(groupName)
        else:
            document = self.findByGroupName(groupID)
        if document == None:
            return None
        userID = document["owner"]
        groupID = document["group_id"]
        user_document = self.findByUserID(userID)
        chatList = user_document["groups"][groupID]
        chatList_json = json.dumps(chatList)
        return chatList_json
    
    def getChatHistory(self, userID):
        document = self.findByUserID(userID)
        if document == None:
            return None
        chatList = document["chat_history"]
        chatList_json = json.dumps(chatList)
        return chatList_json
    
    def getLatestSuggest(self, userID):
        document = self.suggestCollection.find_one({"user_id": userID})
        return document["history"][-1]
    
    def updateUserDocument(self, userID, updated_document):
        self.collection.update_one({"user_id": userID}, {"$set": updated_document})

    def updateGroupDocument(self, groupID, updated_document):
        self.collection.update_one({"group_id": groupID}, {"$set": updated_document})
    
    def insertGroup(self, groupID, groupName):
        document = self.findByGroupID(groupID)
        if document != None:
            return
        new_document = {
            "group_id": groupID,
            "group_name": groupName,
            "owner": "",
            "initialized": False
        }
        self.groupCollection.insert_one(new_document)

    def initializeGroup(self, userID, groupID, initMessage):
        groupDocument = self.groupCollection.find_one({"group_id": groupID})
        if groupDocument == None:
            raise Exception("Group has not been inserted.")
        if groupDocument["initialized"]:
            return False # 正常情況，當作每次進行進行一次(應急作法)
        groupDocument["initialized"] = True
        groupDocument["owner"] = userID
        self.updateGroupDocument(groupID, groupDocument)
        document = self.collection.find_one({"user_id": userID})
        document["groups"].update(
            {
                groupID: [
                    {
                        "role": "user",
                        "content": initMessage
                    }
                ]
            }
        )
        self.updateUserDocument(userID, document)
        return True
    
    
    def updateChatHistory(self, userID, user: None, assistant: None):
        document = self.findByUserID(userID)
        if user != None:
            document["chat_history"].append(
                {
                    "role": "user",
                    "content": user
                }
            )
        if assistant != None:
            document["chat_history"].append(
                {
                    "role": "assistant",
                    "content": assistant
                }
            )
        self.updateUserDocument(userID, document)
    
    def updateGroupHistory(self, userID, groupID, message):
        document = self.findByUserID(userID)
        groupDocument = self.findByGroupID(groupID)
        if groupDocument["owner"] == userID:
            document["groups"][groupID].append(
                {
                    "role": "user",
                    "content": message
                }
            )
        else:
            document["groups"][groupID].append(
                {
                    "role": "counterpart",
                    "content": message
                }
            )
        self.updateUserDocument(userID, document)
    
    def updateSuggestHistory(self, userID, suggest):
        document = self.suggestCollection.find_one({"user_id": userID})
        document["history"].append(suggest)

    def setSuggestFlag(self, userID, boolean):
        document = self.findByUserID(userID)
        document["suggestFlag"] = boolean
        self.updateUserDocument(userID, document)

    def clearChatHistory(self, userID):
        document = self.findByUserID(userID)
        document["chat_history"] = []
        self.updateUserDocument(userID, document)
    
    def clearGroupHistory(self, userID, groupID):
        document = self.findByUserID(userID)
        document["groups"][groupID] = []
        self.updateUserDocument(userID, document)