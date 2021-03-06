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
        print "Usage: python Test.py Mode [fault|non-adapt|full-adapt|semi-adapt]"
        print "mode 0: correct table"
        print "mode 1: missing rule"
        print "mode 2: priority fault"
        exit(1)
    mode = sys.argv[1]
    option = sys.argv[2]
    if not mode in ["0","1","2"]:
        exit(1)
    if not option in ["fault","none-adapt","full-adapt","semi-adapt"]:
        exit(1)
    print sys.argv
    inputs = {}
    for l in range(level):
        for i in range(l*step,(l+1)*step):
            inputs[i] = [10**(l+1),str(i)]
        #for i in range(step,2*step):
        #    inputs[i] = [100,str(i)]
    #for i in range(2*step,3*step):
    #    inputs[i] = [1000,str(i)]
    #for i in range(3*step,4*step):
    #    inputs[i] = [10000,str(i)]

    #generate(inputs)
    inputs0 = {}
    inputs0[0] = [10,"fig1"+str(0)]
    inputs0[1] = [20,"fig1"+str(1)]
    inputs0[2] = [40,"fig1"+str(2)]
    inputs0[3] = [80,"fig1"+str(3)]
    inputs0[4] = [160,"fig1"+str(4)]
    inputs0[5] = [320,"fig1"+str(5)]

    inputs1 = {}
    inputs1[0] = [10,"fig1"+str(0)]
    inputs1[1] = [20,"fig1"+str(1)]
    inputs1[2] = [40,"fig1"+str(2)]
    inputs1[3] = [80,"fig1"+str(3)]
    inputs1[4] = [160,"fig1"+str(4)]
    inputs1[5] = [320,"fig1"+str(5)]
    inputs1[6] = [640,"fig1"+str(6)]
    inputs1[7] = [1280,"fig1"+str(7)]

    total = 0
    right = 0
    times = ["calc","solver","send","total"]
    time = {}
    for i in range(level):
        time[i] = {}
        for ts in times:
            time[i][ts] = 0

    inputs = {}
    if option == "fault":
        inputs = inputs0
    else:
        inputs = inputs1

    for key in inputs:
        case = inputs[key]
        size= case[0]
        name = case[1]
        print "case: ",case
        if mode == "0":
            if option == "fault":
                ret = launcher.launcherA("./data/"+name)
            elif option == "none-adapt":
                ret = launcher.launcherB("./data/"+name)
            elif option == "full-adapt":
                ret = launcher.launcherC("./data/"+name)
            elif option == "semi-adapt":
                ret = launcher.launcherD("./data/"+name)
        elif mode == "1":
            if option == "fault":
                ret = launcher.launcherAWithWrongTable("./data/"+name,"./data/"+name+".miss")
            elif option == "none-adapt":
                ret = launcher.launcherBWithWrongTable("./data/"+name,"./data/"+name+".miss")
            elif option == "full-adapt":
                ret = launcher.launcherCWithWrongTable("./data/"+name,"./data/"+name+".miss")
            elif option == "semi-adapt":
                ret = launcher.launcherDWithWrongTable("./data/"+name,"./data/"+name+".miss")
            pass
        elif mode == "2":
            if option == "fault":
                ret = launcher.launcherAWithWrongTable("./data/"+name,"./data/"+name +".order")
            elif option == "none-adapt":
                ret = launcher.launcherBWithWrongTable("./data/"+name,"./data/"+name +".order")
            elif option == "full-adapt":
                ret = launcher.launcherCWithWrongTable("./data/"+name,"./data/"+name +".order")
            elif option == "semi-adapt":
                ret = launcher.launcherDWithWrongTable("./data/"+name,"./data/"+name +".order")
            pass
        if ret[0] == True:
            right += 1
        total += 1
        for ts in times:
            time[key/step][ts] += ret[1][ts]
        #time[key/step] += ret[1]["total"]
    print right,"/",total
    for i in range(0,level):
        print "Setting, mode: ",mode,"option: ",option
        print "set:",i,"with",step,"inputs, size:",10**(i+1)
        if step > 0:
            for ts in times:
                print ts+":",time[i][ts]/step


