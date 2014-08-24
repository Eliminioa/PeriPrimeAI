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
        
    def run(self):
        self.log.log_status('Bot has started!')
        logged_in = self.r.is_logged_in()
        while logged_in:
            self.log.log_status("Bot is still logged in as:")
            self.log.log_var('r',self.r)
            self.log.log_status("Beginning alert phase!")
            self.alerter.checkForGo()
            self.log.log_status("Alert phase complete!")
            self.log.log_status("Beginning aggregation phase!")
            try:
                for sub in self.config.chromaSubs:
                    self.agg.get_sub_content(sub)
                self.agg.store_corpus()
                self.log.log_status("Aggregation phase complete!")
            except:
                e = sys.exc_info()[0]
                print repr(e)
                try:
                    self.log.log_error(e)
                except:
                    self.log.log_status(repr(e))
            t.sleep(10)

if __name__ == '__main__':
    cfg = config.Config()
    AI = primeAI(cfg)
    AI.run()
