#!/usr/bin/python
from probe import launcher

import random
import os

#level = 2
#step = 10
from settings import level
from settings import step

def generate(inputs):
    for key in inputs:
        case = inputs[key]
        size= case[0]
        name = case[1]
        cmd = "cd rule;sh generator.sh "+name+" "+str(size)
        print cmd
        os.system(cmd)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print "Usage: python Test.py Mode [fault|full-adapt|semi-adapt]"
        print "mode 0: correct table"
        print "mode 1: missing rule"
        print "mode 2: priority fault"
        exit(1)
    print sys.argv
    mode = sys.argv[1]
    option = sys.argv[2]
    if not mode in ["0","1","2"]:
        exit(1)
    if not option in ["fault","none-adapt","full-adapt","semi-adapt"]:
        exit(1)

    total = 0
    right = 0
    times = ["calc","solver","send","total"]
    time = {}
    for i in range(level):
        time[i] = {}
        for ts in times:
            time[i][ts] = 0

    for i in xrange(0,9):
        size= 320
        name = "fig15."+str(i+1)
        name_pre = "fig15."+str(i)
        #print name
        if mode == "0":
            if option == "fault":
                ret = launcher.launcherE("./data/"+name, "./data/"+name_pre)
            elif option == "full-adapt":
                ret = launcher.launcherF("./data/"+name, "./data/"+name_pre)
            elif option == "semi-adapt":
                ret = launcher.launcherG("./data/"+name, "./data/"+name_pre)
        elif mode == "0":
            if option == "fault":
                ret = launcher.launcherA("./data/"+name)
            elif option == "full-adapt":
                ret = launcher.launcherC("./data/"+name)
            elif option == "semi-adapt":
                ret = launcher.launcherD("./data/"+name)
        if ret[0] == True:
            right += 1
        total += 1
        #for ts in times:
        #    time[key/step][ts] += ret[1][ts]
        #time[key/step] += ret[1]["total"]
    #print right,"/",total
    #for i in range(0,level):
    #    print "Setting, mode: ",mode,"option: ",option
    #    print "set:",i,"with",step,"inputs, size:",10**(i+1)
    #    if step > 0:
    #        for ts in times:
    #            print ts+":",time[i][ts]/step


