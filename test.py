# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 20:37:03 2014

@author: boggs
"""

import time as t
import config
import aggregate
cfg = config.Config()
log = cfg.logInstance
r =cfg.redditInstance
agg = aggregate.Aggregator(log,r)

print t.asctime()
for sub in ['councilofkarma','periwinkle','orangered','goodmorningperiwinkle','chromalore']:
    print sub
    test = agg.get_sub_content(sub,1000)
agg.store_corpus()