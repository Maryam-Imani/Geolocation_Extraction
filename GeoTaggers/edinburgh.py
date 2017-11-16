#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 10:50:31 2017

@author: maryam

http://groups.inf.ed.ac.uk/geoparser/documentation/v1.1/html/quickstart.html

"""
import codecs
import subprocess
import xml.etree.ElementTree as et

def format_edinburgh(xml):
    """
    Take the raw output of the Edinburgh parser and extract the properly formatted toponyms for later analysis.
    :param xml: the xml as a STRING to be parsed
    :return: a list of toponyms in format: [PLACEHOLDER STRING,,matched name,,lat,,long,,start index,,end index]
    """
    if len(xml) == 0:  # sometimes no xml string is returned due to no entities found in parsing the output
        return []
    root = et.fromstring(xml)
    toponyms, targets = [], []
    for ent in root.findall("./standoff/ents[@source='ner-rb']/ent[@type='location']"):
        name = ent.find("./parts/part")
        lat = ent.attrib['lat'] if 'lat' in ent.attrib else "0.0"    # Any locations which remain NIL (0.0) must
        lon = ent.attrib['long'] if 'long' in ent.attrib else "0.0"  # be removed before evaluation for fairness
        targets.append((name.text, name.attrib, lat, lon))           # This happens only in around 2-4% of cases
    for target in targets:
        index, start, end = 0, 0, 0
        for word in root.findall("./text/p/s/w"):
            if word.attrib['id'] == target[1]['sw']:
                start = index
            index += len(word.text)
            if word.attrib['id'] == target[1]['ew']:
                end = index
            if word.attrib['pws'] != "no":
                index += 1
        if start == 0 and end == 0:
            print xml, targets
        toponyms.append(
            "No Gaz" + ",," + target[0] + ",," + target[2] + ",," + target[3] + ",," + str(start) + ",," + str(end))
    return toponyms


def run_edinburgh(path):
    """
    Opens a process and runs the Edinburgh Parser on the file specified by PATH and the output is returned.
    :param path: to the text file to be processed - THIS IS A VERY SLOW PROCESS, COMMAND LINE RUN MUCH FASTER!!!
    :return: A list of toponyms - format: [PLACEHOLDER STRING,,matched name,,lat,,long,,start index,,end index]
    """
    sp = subprocess.Popen("cat " + path + " |  /data/maryam/Documents/geoparsers/geoparser-v1.1/scripts/run " +
                          "-t plain -g unlock -top", shell=True, stdout=subprocess.PIPE)
    return format_edinburgh(sp.stdout.read())


if __name__== '__main__':

    filePath = './focus_loc2/spanish_focus_text.txt' 
    out_file = './focus_loc2/spanish_focus_edinburgh.txt'
    
    save = codecs.open(out_file, "w", "utf-8")
    count = 1
    
    with open (filePath , 'r') as fileR: 
        lines = fileR.readlines()
        
        for line in lines: 
            
            outputs = list()
            print count
            count +=1
            
            path = 'temp.txt'
            f = open(path, 'w')
            f.write(line)
            f.flush()
            f.close()
            
            try:
                outputs = run_edinburgh(path)
                #print outputs
            except:
                pass
            
            
            for out in outputs:
                save.write(out + "||")
            save.write("\n")
        save.close()