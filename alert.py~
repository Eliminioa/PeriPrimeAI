#-------------------------------------------------------------------------------
# Name:        Alert Module
# Purpose:      Allows Prime to send out pre-battle alert messages
#
# Author:      James Boggs
#
# Created:     11/03/2014
# Copyright:   (c) James Boggs 2014
# Licence:     GNU shit
#-------------------------------------------------------------------------------

"""Module with the class for letting Periwinkle Prime send out battle alerts at
the command of a general. """

#IMPORTS:#
from requests.exceptions import HTTPError
#END IMPORTS#

class alertBot(object):
    """Only use checkForGo(), other methods are internal and idk what the hell
    to do with them."""
    def __init__(self,cfg,log):
        self.cfg = cfg
        self.log = log
        self.r = cfg.redditInstance
    
    def getUsers(self):
        r = self.r
        signupThread = r.get_submission(submission_id=self.cfg.alert_thread)
        self.log.log_status(str(signupThread))
        signupThread.replace_more_comments()
        self.log.log_status('Replaced more comments')
        signUps = signupThread.comments
        self.log.log_var("signUps",signUps)
        troopList = []
        for signUp in signUps:
            if self.detect_ORed(signUp.author):
                print("Orangered "+str(signUp.author)+" ignored!")
                self.log.log_status("Orangered "+str(signUp.author)+" ignored!")
                continue
            recruit = signUp.author.__str__()
            self.log.log_var("signUp",signUp)
            try:
                if not (recruit in troopList):
                    troopList.append(recruit)
                    self.log.log_status("Added user "+recruit+"to troopList.")
            except:
                self.log.log_status("ERROR:")
                self.log.log_var("recruit",recruit)
                pass
        self.log.log_status("Retrieved Majors")
        self.log.log_var("troopList",troopList)
        print troopList
        return troopList

    def checkForGo(self):
        """Checks Prime's inbox for messages to send out."""
        r = self.r
        troopList = self.getUsers()
        PMs = r.get_unread(True, True)
        if PMs != None:
            self.log.log_status("New messages!")
            for PM in PMs:
                PM.mark_as_read()
                sLine = PM.subject.strip().upper()
                if (sLine == "SEND MESSAGE") and (PM.author.__str__() in self.cfg.generals):
                    sent_to = ''
                    for troops in troopList:
                        try:
                            r.send_message(troops,"Battle Reminder",PM.body)
                            sent_to += troops+'\n\n'
                            self.log.log_status("Message: "+PM.body+" sent to "+troops)
                        except:
                            self.log.log_status("Error with " + troops)                  
                    PM.reply("Message sent to "+sent_to+"!")
        else:
            self.log.log_status("No new messages!")

    def detect_ORed(self,user):
        subReddit = self.r.get_subreddit(self.cfg.enemy_sub)
        mods = subReddit.get_moderators()
        for mod in mods:
            try:
                if mod == user:
                    return True
            except HTTPError as E:
                print ("User no longer exists?")
                self.log.log_error(E)
                self.log.log_status("HTTPError again, with user "+str(user))
                continue
        return False