# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 12:40:07 2014

Module for PrimeAI for it to tally up battle scores.

@author: boggs
"""
import numpy

class BattleEye(object):
    
    def __init__(self,cfg,log,arenaBot):
        """A module that lets Prime evaluate the battlefield and comment on it.
        Takes the name of the bot (either chromabot or valkyribot) as a string."""
        self.cfg = cfg
        self.log = log
        self.r = self.cfg.redditInstance
        self.arenaBot = self.r.get_redditor(arenaBot)
        self.log.log_status('Got '+str(arenaBot)+' as the arena bot')
        self.activeBattle = {"exists":False}
        
    def check_for_go(self):
        """Checks if there is an on-going battle. 
        Currently in progress, and needs to be able to sense if a battle is started
        and who started it and when it will end."""
        if self.activeBattle['exists']:
            self.log.log_status('There is an active battle. Parsing it now')
            self.parseBattle()
        overview = [item for item in self.r.get_content(url=self.arenaBot._url)]
        self.log.log_status('Got arena bot overview')
        comments = [o for o in self.overview if str(type(o))=="<class 'praw.objects.Comment'>"]
        self.log.log_status('Got arena bot comments')
        submissions = [o for o in overview if str(type(o))=="<class 'praw.objects.Submission'>"]
        self.log.log_status('Got arena bot submissions')
        latestSubmission = submissions[0]
        self.log.log_status("Got arena bot's latest submission")
        #This section will let Prime determine whether a battle is active.
        #The aggressor var will be a string either 'orangered' or 'periwinkle that indicates which side began the battle.
        #The is_active var will be a boolean determining its namesake
        #The time var will be a standard mktime() float
        if "[Invasion]" in latestSubmission.title or "The Eternal Battle Rages On" in latestSubmission.title:
            self.log.log_status('Latest submission is an invasion')
            self.activeBattle['exists'] = True
            self.activeBattle['thread'] = latestSubmission
            self.activeBattle['subBody'] = latestSubmission.selftext
            self.activeBattle['aggressor'] = latestSubmission.title[15:latestSubmission.title.index(' armies')]
            self.activeBattle['is_active'] = ('The conflict will soon be upon you' not in subBody) and ('The battle is complete...' not in subBody)
            self.activeBattle['time'] = self.get_bTime(subBody)
            self.log.log_status('There is an active battle. Parsing it now')
            self.parseBattle()
            
    def parseBattle(self):
        """Examine the battle thread, and see what Prime should respond to."""
        #This is the real core of this function. Later I might make a more broad
        #speech module that this will then tap into, but for now this will be 
        #the extent of Prime's chatting capabilities. This module will follow
        #different protocols depending on whether the battle hasn't started, has
        #started, or has finished.
        #PRE-GAME + POST-GAME PROTOCOLS
        if not self.activeBattle['is_active']:
            if 'The conflict will soon be upon you' in self.activeBattle['subBody']:
                #PRE-GAME PROTOCOL
                if self.activeBattle['commented']:
                    #Since the bot has already posted a comment, commence bantering
                else:
                    thread = self.activeBattle['thread'].add_comment(self.initial_comment())
                    self.activeBattle['commented'] = True
                    
                
    def get_bTime(self,subBody):
        """Examines the body of a post an extracts either its start or end time,
        then returns it as a float in seconds from the epoch."""
        self.log.log_status('Getting battle time')
        raw_etime = subBody[subBody.find('[')+1:subBody.find(']')]
        time = [int(raw_etime[0:4]),int(raw_etime[5:7]),int(raw_etime[8:10]),int(raw_etime[11:13])-4,int(raw_etime[14:16]),int(raw_etime[17:20]),0,0,-1]
        if 'PM' in raw_etime:
            time[3] += 12
        self.log.log_status('Returned battle time')
        return time.mktime(time)