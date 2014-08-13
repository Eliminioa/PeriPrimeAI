# -*- coding: utf-8 -*-
#BEGIN IMPORTS
from json import load
import praw
#END IMPORTS

class Config(object):
    """Configuration and log-in for PrimeAI"""
    
    def __init__(self):
        #grab the config data
        conffile = './config/config.json'
        self.confData = load(open(conffile,'r'))
        
    def login_reddit(self, ua):
        """Return a logged-in praw.Reddit object."""
        r = praw.Reddit(ua)
        r.login(self.confData['reddit'],self.confData['password'])
        return r
    
    @property
    def email_username(self):
        return self.confData['email']