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
        self.overview = [item for item in self.r.get_content(url=arenaBot._url)]
        self.comments = [o for o in self.overview if str(type(o))=="<class 'praw.objects.Comment'>"]
        self.submissions = [o for o in overview if str(type(o))=="<class 'praw.objects.Submission'>"]
        
    def check_for_go(self):
        """Checks if there is an on-going battle. """
        latestSubmission = self.submissions[0]
        if "[Invasion]" in latestSubmission.title or "The Eternal Battle Rages On" in latestSubmission.title: