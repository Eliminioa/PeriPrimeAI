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

class alertBot(object):
    """Only use checkForGo(), other methods are internal and idk what the hell
    to do with them."""
    def __init__(self,cfg,log):
        self.cfg = cfg
        self.log = log
        self.r = cfg.redditInstance
        self.badMods = [str(m) for m in self.r.get_subreddit(self.cfg.enemy_sub).get_moderators()]
    
    def getUsers(self,majors='default'):
        r = self.r
        if majors != 'default':
            return majors
        majors = self.cfg.majors
        signupThread = r.get_submission(submission_id=self.cfg.alert_thread)
        self.log.log_status(str(signupThread))
        signupThread.replace_more_comments()
        self.log.log_status('Replaced more comments')
        signUps = [sp for sp in signupThread.comments]
        self.log.log_var("signUps",signUps)
        troopList = majors
        for signUp in signUps:
            recruit = signUp.author.__str__()
            if self.detect_ORed(signUp.author) and not (recruit in troopList):
                troopList.append(recruit)
                self.replyToSignup(signUp,False)
                print("Orangered "+str(signUp.author)+" ignored!")
                self.log.log_status("Orangered "+str(signUp.author)+" ignored!")
                continue
            self.log.log_var("signUp",signUp)
            try:
                if not (recruit in troopList):
                    troopList.append(recruit)
                    self.replyToSignup(signUp)
                    self.log.log_status("Added user "+recruit+" to troopList.")
                    print "Added user "+recruit+" to troopList. ",len(troopList)
            except:
                self.log.log_status("ERROR:")
                self.log.log_var("recruit",recruit)
                pass
            self.log.log_status("Retrieved Majors")
            self.log.log_var("troopList",troopList)
            for major in troopList:
                self.cfg.add_major(major)
            self.cfg.save_cfg()
        return troopList

    def checkForGo(self):
        """Checks Prime's inbox for messages to send out."""
        r = self.r
        troopList = self.getUsers()
        troopList = [user for user in troopList if not self.detect_ORed(user)]
        PMs = [pm for pm in r.get_unread(True, True)]
        if len(PMs) != 0:
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
                    self.log.log_status("Message sent to "+sent_to+"!")
                    PM.reply("Message sent to "+sent_to+"!")
        else:
            self.log.log_status("No new messages!")
            
    def replyToSignup(self,signUp,PW=True):
        if not PW:
            signUp.reply("""    ORANGERED SCUM DETECTED
                LETHAL FORCE ACTIVATED""")
        else:
            message = 'AFFIRMATIVE. USER ' + str(signUp.author).upper() + " HAS BEEN ENTERED INTO THE DATABASE."
            keys = self.keywords(signUp.body)
            if 'h' in keys:
                message = "GREETINGS USER " + str(signUp.author).upper() + ". YOU HAVE BEEN ENTERED INTO THE DATABASE."
            if ('s' in keys) or ('w' in keys):
                message = message.replace('. ', '. AS DESIRED, ',1)
            if 'a' in keys:
                message += ' I AGREE, PERIWINKLE IS THE SUPERIOR RACE.'
            if 'b' in keys:
                message += ' INDEED, ORANGREDS ARE A MENACE!'
            if 'p' in keys:
                message += ' YOU HAVE BEEN DETECTED AS A TRUE PERIWINKLE PATRIOT!'
            signUp.reply(message)
            
    def keywords(self,text):
        positiveAdj = [u'fantastic', u'grand', u'howling', u'marvelous', u'marvellous', u'rattling', u'terrific', u'tremendous', u'wonderful', u'wondrous', u'excellent', u'first-class', u'fantabulous', u'splendid', u'amazing', u'awe-inspiring', u'awesome', u'awful', u'awing', u'good', u'estimable', u'good', u'honorable', u'respectable','best','better']
        negativeAdj = ['bad','unfit','unsound','evil','immoral','wicked','vicious','malefic','malevolent','malignant','menance','threat','trash','scum','villain','scoundrel']
        positiveVbs = []
        negativeVbs = []
        periWords = ['periwinkle','periwinkles','pw','pws','peri','peris','prime']
        orWords = ['orangered','orangereds','or','ors','ored','oreds']
        positivePeris = [adj+" "+peri for adj in positiveAdj for peri in periWords]+[peri+" is "+adj for adj in positiveAdj for peri in periWords]
        badORed = [adj+" "+ored for adj in negativeAdj for ored in orWords]+[ored+" is "+adj for adj in negativeAdj for ored in orWords]
        sents = [k.lower() for i in text.split('.') for j in i.split('!') for k in j.split('?')]
        keys = ''
        for sent in sents:
            if ('sign up' in sent) or ('sign me up' in sent):
                keys += 's'
            if ('hi' in sent) or ('hello' in sent) or ('greetings' in sent):
                keys += 'h'
            if ('better dead than orangered' in sent):
                keys += "p"
            if ('want' in sent) or ('wish' in sent) or ("i'd like" in sent):
                keys += "w"
            for positive in positivePeris:
                if positive in sent:
                    keys += "a"
            for bad in badORed:
                if bad in sent:
                    keys += "b"
        return keys
    
    def cleanse_list(self):
        for user in self.cfg.majors:
            if user in self.cfg.orangereds:
                self.cfg.confData['majors'].remove(user)
                self.cfg.save_cfg()
        
    def detect_ORed(self,user):
        if str(user) in self.cfg.orangereds:
            return True
        return False
