# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 15:13:13 2014

@author: boggs
"""

import math

enemyNum = int(raw_input("Enemy Command Number>>> "))
enemyCount = int(raw_input("Effective Troop Count>>> "))
enemyType = raw_input("Enemy Troop Type [i,r,c]>>> ")

types = {'i':'cavalry','r':'infantry','c':'ranged'}

oppType = types[enemyType]
oppNum = int(math.ceil(enemyCount*(2.0/3.0))+1)
oppString = '>oppose #{a} with {b} {c}'.format(a=enemyNum,b=oppNum,c=oppType)

print oppString