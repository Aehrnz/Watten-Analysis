# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 12:11:42 2020

@author: Dominik Gruber
"""
# scrapes user statistics from watten.org
# to stop and save, enter "0" with keyboard


# import different libraries

from datetime import datetime
from lxml import html
import requests
import re
import time
import matplotlib.pyplot as plt
import csv
import numpy as np


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
        
        visitorsHandle, = plt.plot(Timevec, visitorsvec, label='Visitors')
        playersHandle, = plt.plot(Timevec, playersvec, label='Players')
        plt.legend(handles=[visitorsHandle, playersHandle])
        plt.xlabel("Time")
        plt.ylabel("Visitor and player numbers on watten.org")
        plt.draw()
        fig1.savefig('/var/www/html/watten.png')             # saving the plot  
        
        
    def idle(self):
        
        t=3
        while t>0:
            time.sleep(1)
            t -= 1
            
    def analuesis(self):
        
        visitorsvec = [z.visitors for z in cData] 
        playersvec = [z.players for z in cData]        
        minvisitors = np.amin(visitorsvec)
        minplayers = np.amin(playersvec)
            
            
        with open('Output.txt', 'w') as f:
            f.write(str( minvisitors  ))
            f.write("\t" )
            f.write(str( minplayers ))
            f.close()
            
def main():
    
    SM=Statemachine()      #Statemachine SM
    global checker  
    checker=0   
    
    while 1:
        SM.gather()
        SM.idle()
        
        now=datetime.now()
        
        
        if now.hour==7 and now.minute==30 and checker==0:  #checker checks if the analysis has been run already
            
            SM.analuesis()
                  
            checker=1
            
        elif  now.hour==8 and checker!=0:
            
            checker=0
            
    
            
if __name__== "__main__" :
    main()        
    
    
    
    

    

