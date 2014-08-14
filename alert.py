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
import config
import AIlogging as l
log = l.log()
cfg = config.Config()
log.log_status("Finished Imports")
from requests.exceptions import HTTPError
#END IMPORTS#

class alertBot(object):
    """Only use checkForGo(), other methods are internal and idk what the hell
    to do with them."""
    def __init__(self):
        self.r = cfg.redditInstance
    
    def getUsers(self):
        r = self.r
        signupThread = r.get_submission(submission_id=cfg.alert_thread)
        log.write(str(signupThread)+"\n")
        signupThread.replace_more_comments()
        log.write('Replaced more comments'+"\n")
        signUps = signupThread.comments
        log.write(str(signUps)+"\n")
        troopList = []
        for signUp in signUps:
            if self.detect_ORed(signUp.author):
                print("Orangered "+str(signUp.author)+" ignored!")
                log.write("Orangered "+str(signUp.author)+" ignored!")
                continue
            recruit = signUp.author.__str__()
            log.write(str(signUp)+"\n")
            try:
                if not (recruit in troopList):
                    troopList.append(recruit)
                    log.write("Added user "+recruit+"to troopList.\n")
                    log.flush()
            except:
                log.write("ERROR:"+"\n")
                log.write(str(recruit)+"\n")
                pass
        log.write("Retrieved Majors"+"\n")
        log.write(str(troopList)+"\n")
        print troopList
        return troopList

    def checkForGo(self):
        r = self.r
        troopList = self.getUsers(self)
        PMs = r.get_unread(True, True)
        if PMs != None:
            log.write("New messages!"+"\n")
            for PM in PMs:
                PM.mark_as_read()
                sLine = PM.subject.strip().upper()
                if (sLine == "SEND MESSAGE") and (PM.author.__str__() in cfg.generals):
                    sent_to = ''
                    for troops in troopList:
                        try:
                            r.send_message(troops,"Battle Reminder",PM.body)
                            sent_to += troops+'\n\n'
                            log.write("Message: "+PM.body+" sent to "+troops+"\n")
                        except:
                            log.write("Error with " + troops+"\n")                  
                    PM.reply("Message sent to "+sent_to+"!")
        else:
            log.write("No new messages!"+"\n")
        log.flush()

    def detect_ORed(self,user):
        subReddit = self.r.get_subreddit(cfg.enemy_sub)
        mods = subReddit.get_moderators()
        for mod in mods:
            try:
                if mod == user:
                    return True
            except HTTPError:
                print ("User no longer exists?")
                log.write("HTTPError again, with user "+str(user)+"\n")
                continue
        return False