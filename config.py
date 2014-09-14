# -*- coding: utf-8 -*-
#BEGIN IMPORTS
from json import load, dump
import praw
import AIlogging

#END IMPORTS

class Config(object):
    """Configuration and log-in for PrimeAI"""
    
    def __init__(self, conffile='/config/',ua="Periwinkle Prime AI"):
        """Grab the config data and a logged-in reddit instance"""
        self.log = AIlogging.log()
        try:
            self.confData = load(open(conffile,'r'))
            self.log.log_status("Configuration data loaded from "+conffile+"!")
        except:
            conffile = './config/config.json'
            self.confData = load(open(conffile,'r'))
            self.log.log_status("Resorted to default conffile!")
        self.log.log_var("confData",self.confData)
        self.r = praw.Reddit(ua)
        self.log.log_var("r",self.r)
        self.r.login(self.confData['reddit'],self.confData['password'])
        self.log.log_status("Logged into reddit successfully!")
        
    def add_major(self,major):
        if major not in self.majors:
            self.confData['majors'].append(major)
        
    def save_cfg(self,conffile='./config/config.json'):
        dump(self.confData,open(conffile,'w'))
    
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
    def chromaSubs(self):
        return self.confData['chromaSubs']
    
    @property
    def majors(self):
        return self.confData['majors']
        
    @property
    def redditInstance(self):
        return self.r
        
    @property
    def logInstance(self):
        return self.log