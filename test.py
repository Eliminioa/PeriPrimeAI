# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 16:28:05 2014

@author: boggs
"""

import praw
r = praw.Reddit('Eliminioa testing')
r.login('Eliminioa','KeilHallAwesome')
arenaBot = r.get_redditor('valkyribot')
overview = [item for item in r.get_content(url=arenaBot._url)]
comments = [o for o in overview if str(type(o))=="<class 'praw.objects.Comment'>"]
submissions = [o for o in overview if str(type(o))=="<class 'praw.objects.Submission'>"]