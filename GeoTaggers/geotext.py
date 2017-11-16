#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 11:32:43 2017

@author: maryam

http://geotxt.org/api/
"""
import codecs
import urllib
import json

def run_geotext(q):
    """
    Run the query through the GeoTxt API service.
    :param q: Text to analyse. If the query length is more than 3900, the query is submitted in chunks
    :return: a list of toponyms - format: [PLACEHOLDER STRING,,matched name,,lat,,long,,start index,,end index]
    """
    base_url = 'http://geotxt.org/v2/api/geotxt.json?m=stanfords&'
    out = []  # list of tuples as output
    for start in range(0, len(q), 3000):
        query_chunk = q[start: start + 3000]
        response = urllib.urlopen(base_url + urllib.urlencode({'q': query_chunk}))  # contact servers
        if response.code != 200:
            print "Error Response Code =", response.code, " query length=", len(query_chunk)
            print response.info()
            return []
        res = json.loads(response.read())
        for m in res['features']:
            if m['geometry'] is not None:
                lat = m['geometry']['coordinates'][1]
                lon = m['geometry']['coordinates'][0]
                for pos in m['properties']['positions']:
                    name = m['properties']['name']
                    out.append(m['properties']['toponym'] + ",," + name + ",," + str(lat) +
                               ",," + str(lon) + ",," + str(pos + start) + ",," + str(len(name) + pos + start))
    return out



if __name__== '__main__':
    
    filePath = './focus_loc2/spanish_focus_text.txt' 
    out_file = './focus_loc2/spanish_focus_geo.txt'
    
    save = codecs.open(out_file, "w", "utf-8")
    count = 1
    
    with open (filePath , 'r') as fileR: 
        lines = fileR.readlines()
        
        for line in lines: 
            
            outputs = list()
            print count
            count +=1
            try:
                outputs = run_geotext(line.encode('utf8'))
                print outputs
            except:
                pass
            #print outputs
            
            for out in outputs:
                save.write(out + "||")
            save.write("\n")
        save.close()