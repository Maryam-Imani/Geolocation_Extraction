#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:48:31 2017

@author: maryam

https://github.com/Berico-Technologies/CLAVIN
https://github.com/Berico-Technologies/CLAVIN-NERD
"""
import codecs
import subprocess



def run_clavin(path):
    """
    Opens a process and runs CLAVIN on the file specified by PATH. Java is run (CLAVIN) and the output is returned.
    THIS IS A VERY SLOW PROCESS, COMMAND LINE RUN MUCH FASTER!!!
    :param path: to the text file to be processed
    :return: A list of toponyms - format: [geoname,,matched name,,lat,,long,,start index,,end index]
    """
    out = []
    sp = subprocess.Popen("MAVEN_OPTS=\"-Xmx4g\" mvn exec:java -Dexec.mainClass=\"com.bericotech.clavin.WorkflowDemo\" "
                          " -Dexec.args=\"" + path + "\" -f /data/maryam/Documents/geoparsers/CLAVIN-Server-master/pom.xml",
                          shell=True, stdout=subprocess.PIPE)
    for line in iter(sp.stdout.readline, ''):
        if not line.startswith("[INFO]"):
            out.append(line.strip("\n").decode('utf-8'))
    return out


if __name__== '__main__':

    filePath = './data/spanish_text.txt' 
    out_file = './data/spanish_clavin.txt'
    
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
                outputs = run_clavin(path)
                print outputs
            except:
                pass
            
            
            for out in outputs:
                save.write(out + "||")
            save.write("\n")
        save.close()