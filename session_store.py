#if gonna do logout, delete session

import os, base64

class SessionStore:

    def __init__(self):
        #this is your file cabinet
        #will contain many dictionaries, one per session
        self.sessions = {}
        return

    def generateSessionID(self):
        randomNumber = os.urandom(32)
        randomString = base64.b64encode(randomNumber).decode("utf-8")
        return randomString

    def createSession(self):
        sessionID = self.generateSessionID()
        #add a new session (dictionary) to the "file cabinet"
        #use the new generated sessionID
        self.sessions[sessionID] = {}
        return sessionID
    
    def getSession(self, sessionID):
        if sessionID in self.sessions:
            #return existing session by ID
            return self.sessions[sessionID]
        else:
            #return nothing if ID is invalid 
            return None

    