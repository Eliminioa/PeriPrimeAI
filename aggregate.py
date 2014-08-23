# -*- coding: utf-8 -*-
"""
A helper module that lets Prime collect/aggregate text data from around Chroma 
into a corpus. Required the Natural Language ToolKit
"""
#BEGIN IMPORTS
import json
import time as t
import nltk
from praw.errors import RedirectException
from requests.exceptions import HTTPError
#END IMPORTS


class Aggregator(object):
    """Has functions that help aggregate text on chroma into a central 
    database/repository
    """
    
    def __init__(self,log,reddit,corpusFile='./config/chromaCorpus.txt'):
        self.log = log
        self.r = reddit
        self.cf = json.load(open(corpusFile,'r'))
        
    def get_sub_content(self,sub,limit=1000):
        """Gets post content from a subreddit and collectes it into a single JSON
        object organized by author, with a total corpus for the sub as well."""
        r = self.r
        self.log.log_status("Getting the content of /r/"+str(sub))
        sub = self.r.get_subreddit(sub)
        sName = str(sub)
        self.log.log_var("sub",sub)
        getters = (sub.get_new,sub.get_hot,sub.get_top_from_all,sub.get_top_from_year,sub.get_controversial_from_all,sub.get_controversial_from_year)
        for getter in getters: #thanks to GitHub user KevOrr for this bit of code!
            stuff = [p for p in getter(limit=limit)]
            fulltext = ''
            authors={}
            x=0
            init_time = t.time()
            try:
                for post in stuff:
                    if post.id in self.cf['readIDs']:
                        continue
                    self.log.log_var("post",post)
                    aName = str(post.author)
                    posttext = post.selftext.strip()
                    try:
                        authors[aName] += posttext + ' '
                    except:
                        authors[aName] = posttext + ' '
                    fulltext += posttext.strip()+" "
                    cmtData = self.get_comment_data(post)
                    fulltext += cmtData[1]
                    replyData = cmtData[0]
                    for cmnter in replyData:
                        try:
                            authors[cmnter] += replyData[cmnter]
                        except:
                            authors[cmnter] = replyData[cmnter]                
                    x+=1
                    self.cf['readIDs'].append(post.id)
                    print '{} out of {} done after {} seconds ({}%)'.format(x,limit,t.time()-init_time,(float(x)/limit)*100)
            except HTTPError as E:
                self.log.log_status("It is likely that the sub "+sName+" is unavavailable due to being private or deleted.")
                self.log.log_error(E)
                return False
            except RedirectException as E:
                self.log.log_status("The sub name " + str(sub)+" is probably spelled wrong.")
                self.log.log_error(E)
                return False
            self.log.log_status("Returning sub name and authors")
            try:
                self.cf['subs'][sName] += fulltext
            except:
                self.cf['subs'][sName] = fulltext
            for author in authors:
                try:
                    self.cf['auths'][author] += authors[author]
                except:
                    self.cf['auths'][author] = authors[author]
            self.update_corpus((sName,authors,fulltext))
            return (sName,authors,fulltext)
        
    def get_comment_data(self,post):
        """Aggregates all the comment data and returns it as a JSON by author"""
        self.log.log_status("Getting comment data from post "+str(post))
        cmntData = {}
        post.replace_more_comments()
        comments = [c for c in post.replace_more_comments()]
        fulltext = ''
        for cmnt in comments:
            self.log.log_var("cmnt",cmnt)
            bodytext = cmnt.body
            fulltext += bodytext.strip() + " "
            aName = str(cmnt.author)
            try:
                cmntData[aName] += bodytext.strip() + " "
            except:
                cmntData[aName] = bodytext.strip() + " "
        self.log.log_status("Returning comment data from post "+str(post))
        return (cmntData,fulltext)
        
    def update_corpus(self,subData):
        try:
            self.cf['subs'][subData[0]] += subData[2]
        except:
            self.cf['subs'][subData[0]] = subData[2]
        for auth in subData[1]:
            try:
                self.cf['auths'][auth] += subData[1][auth]
            except:
                self.cf['auths'][auth] = subData[1][auth]
        self.cf['total'] += subData[2]

    def store_corpus(self,corpusFile = './config/chromaCorpus.txt'): 
        json.dump(self.cf,open(corpusFile,'w'))