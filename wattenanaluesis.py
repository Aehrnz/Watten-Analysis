#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 12:11:42 2020

@author: Aehrnz Ärger
"""
# scrapes user statistics from watten.org
# to stop and save, enter "0" with keyboard


# import different libraries

from datetime import datetime
from lxml import html
import requests
import re
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv


workingdir = "."

# initialize classes and objects

class Dataset:
    def __init__(self, timestamp, visitors, players, readstr):
        self.timestamp = timestamp
        self.visitors = visitors
        self.players = players
        self.readstr=readstr
        
cData=[]  
       


class Statemachine:
    def gather(self):
        
        # get data from website
        page = requests.get('https://www.watten.org/')
        tree = html.fromstring(page.content)      # retrieved data
        

        List=tree.xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[2]/text()')    # extract wanted data with xPath from tree    
        Datn=re.findall(r'\d+', List[0])        # extract Visitors- and Player- number from string
    

        #assembling vectors
        
        iData=Dataset(datetime.now(),int(Datn[0]),int(Datn[1]),str(List[0]))        #ith dataset       
        cData.append(iData)             # append to entire collected Data
        
        Timevec = [z.timestamp for z in cData]
        visitorsvec = [z.visitors for z in cData] 
        playersvec = [z.players for z in cData]
        indexvec=range(0, len(cData))
        
        # saving obtained data to file
        with open('SavedData.csv', 'w') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(zip(indexvec,Timevec,visitorsvec,playersvec,[z.readstr for z in cData]))
  
    
        # for debugging purposes
        print('collected and saved new dataset')
        now=datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
    
        # plot developement
        
        fig1 = plt.figure(1)
        ax1 = fig1.gca()
        ax1.plot(Timevec, visitorsvec, Timevec, playersvec)
        plt.xlabel("Time")
        plt.ylabel("Visitors- and Playernumbers on watten.org")
        plt.show()
        plt.draw()
        fig1.savefig('Plot.png')             # saving the plot  
        
        
    def idle(self):
        
        t=10
        while t>0:
            time.sleep(1)
            t -= 1

  
def main():
    
    SM=Statemachine()      #Statemachine SM
    while 1:
        SM.gather()
        SM.idle()
            
if __name__== "__main__" :
    main()        
    
    
    
    

    

