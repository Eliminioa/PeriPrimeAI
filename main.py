# -*- coding: utf-8 -*-

import config
import AIlogging
import alert

class primeAI(object):
    """The brains of the operation, the head of the beast, the robot's CPU, this
    is the important bit, that collates the modules and makes shit happen. """
    
    def __init__(self,config):
        self.config = config
        self.r = config.redditInstance
        self.log = config.logInstance
        self.alerter = alert.alertBot(self.config,self.log)
        
    def run(self):
        self.log.log_status('Bot has started!')
        logged_in = self.r.is_logged_in()
        while logged_in:
            self.log.log_status("Bot is still logged in as:")
            self.log.log_var('r',self.r)
            self.alerter.checkForGo()
            logged_in = False
            
if __name__ == '__main__':
    cfg = config.Config()
    AI = primeAI(cfg)
    AI.run()