#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 14:54:43 2017

@author: maryam
"""

import codecs
import re
import json, sys
import requests

#reload(sys)
#sys.setdefaultencoding("utf-8")


def Mordecai(text):

    headers = {'Content-Type': 'application/json'}
    place=list()
        
    data = {'text': text}
        
    data = json.dumps(data)    
    out = requests.post('http://localhost:5000/places', data=data, headers=headers)
    parsed_json = json.loads(out.text)
    try:
        for e in parsed_json:
            #print e
            index = [m.start() for m in re.finditer(e['placename'].strip(), text)]
            for ind in index:    
                
                en = e['searchterm'] + ",," + e['placename'] + ",," + str(e['lat']) + ",," + str(e['lon']) + ",,"+ str(ind) +',,'+ str(ind +len(e['placename'].strip()) ) 
                if ( en not in place):
                    place.append(en)
            
    except:
        print "error"     
    
    return place



if __name__ == '__main__':
      
    filePath = './focus_loc2/spanish_focus_text.txt' 
    out_file = './focus_loc2/spanish_focus_mordecai.txt'
    
    save = codecs.open(out_file, "w", "utf-8")
    count = 1
    
    with open (filePath , 'r') as fileR: 
        lines = fileR.readlines()
        
        for line in lines: 
            
            outputs = list()
            print count
            count +=1
            
            try:
                outputs = Mordecai(line.encode('utf8'))
                print outputs
            except:
                pass
            
            for out in outputs:
                save.write(out + "||")
            save.write("\n")
        save.close()