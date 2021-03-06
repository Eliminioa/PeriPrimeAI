# -*- coding: utf-8 -*-

import config
import AIlogging
import alert
import sys
import aggregate
import time as t

class primeAI(object):
    """The brains of the operation, the head of the beast, the robot's CPU, this
    is the important bit, that collates the modules and makes shit happen. """
    
    def __init__(self,config):
        self.config = config
        self.r = config.redditInstance
        self.log = config.logInstance
        self.alerter = alert.alertBot(self.config,self.log)
        self.agg = aggregate.Aggregator(self.log,self.r)
        self.majors = config.majors
        
    def run(self):
        self.log.log_status('Bot has started!')
        finding_bot = True #variable to make sure the process of finding Chromabot doesn't time out
        logged_in = self.r.is_logged_in
        while logged_in():
            while finding_bot:
                try:
                    self.config.list_players()
                    finding_bot = False #we're no longer looking for chromabot, we've successfully found it
                except:
                    t.sleep(60) #otherwise, wait and try again
            print "Beginning iteration"
            self.log.log_status("Bot is still logged in as:")
            self.log.log_var('r',self.r)
            self.log.log_status("Beginning alert phase!")
            try:
                self.alerter.checkForGo()
            except KeyboardInterrupt:
                print "Exiting program!"
                self.config.save_cfg()
                self.log.log_status('Exited bot on account of Keyboard Interrupt')
                break
            except:
                e = sys.exc_info()
                self.log.log_status("Alert phase failed!".format)
                self.log.log_status(repr(e))
            self.log.log_status("Alert phase complete!")
            self.log.log_status("Beginning aggregation phase!")
            try:
                for sub in self.config.chromaSubs:
                    self.agg.get_sub_content(sub)
                self.agg.store_corpus()
                self.log.log_status("Aggregation phase complete!")
            except KeyboardInterrupt:
                print "Exiting program!"
                self.config.save_cfg()
                self.log.log_status('Exited bot on account of Keyboard Interrupt')
                break
            except:
                e = sys.exc_info()
                self.log.log_status("Aggregation phase failed!".format)
                self.log.log_status(repr(e))
            t.sleep(10)
            finding_bot = True
        self.log.log_status('Bot has stopped!')
        self.r.send_message('Eliminioa','PRIME ERROR','PERIWINKLE PRIME HAS CEASED TO FUNCTION. INVESTIGATE IMMEDIATELY! NOTE THAT IT RESTARTS AUTOMATICALLY!')
        
            
if __name__ == '__main__':
    cfg = config.Config()
    AI = primeAI(cfg)
    AI.run()
