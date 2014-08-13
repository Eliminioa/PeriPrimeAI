# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 11:14:09 2014

Logging module for Periwinkle Prime's AI, since, I'll be honest, I have no idea
how to use the module built into python, and I'm fairly sure it doesn't do what
I want it to do anyways. This module will allow the program to transcribe 
variable changes that occur during runtime into a plaintext file for later 
perusal. 

@author: boggs
"""

#BEGIN IMPORTS
import string as s
from time import asctime
#END IMPORTS

class log(object):
"""
Logging module for Periwinkle Prime's AI, since, I'll be honest, I have no idea
how to use the module built into python, and I'm fairly sure it doesn't do what
I want it to do anyways. This module will allow the program to transcribe 
variable changes that occur during runtime into a plaintext file for later 
perusal. __init__ requires a filepath to create the log. log.log(string) writes
string into the log, in the format: 
%(string) @ %(asctime)+15s 
"""

    def __init__(self):
        self.logFile = open('./config/AILog.txt','w')
        return self.logFile
    
    def log_var(self,varName,var):
        """Writes a variable into the log."""
        if not type(varName) is str:
            vName = str(varName)
        vType = str(type(var))[7:len(thing)-2]
        vVal = repr(var)
        report = '{vType} variable {vName} = {vVal} @ {asctime} \n'.format(vType=vType,vName=vName,vVal=vVal,asctime=asctime())
        self.logFile.write(report)
        
    def log_error(self,E):
        """Writes an error into the log."""
        error = str(E)
        eType = error[:error.index('(')]
        eMsg = error[error.index('('):].strip('()')
        