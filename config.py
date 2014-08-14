# -*- coding: utf-8 -*-
#BEGIN IMPORTS
from json import load
import praw

#END IMPORTS

class Config(object):
    """Configuration and log-in for PrimeAI"""
    
    def __init__(self, conffile='/config/',ua="Periwinkle Prime AI"):
        """Grab the config data and a logged-in reddit instance"""
        try:
            self.confData = load(open(conffile,'r'))
        except:
            conffile = './config/config.json'
            self.confData = load(open(conffile,'r'))
        self.r = praw.Reddit(ua)
        self.r.login(self.confData['reddit'],self.confData['password'])
        
    
    @property
    def email_username(self):
        return self.confData['email']
        
    @property
    def enemy_sub(self):
        return self.confData['enemy_sub']
        
    @property
    def alert_thread(self):
        return self.confData['alertThread']
        
    @property
    def generals(self):
        return self.confData['generals']
        
    @property
    def redditInstance(self):
        return self.r