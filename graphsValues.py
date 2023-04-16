from numpy import append
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
  

def valuesRev():
   
    #REV
    graph_dataRev = open('valuesRev.txt','r').read()
    linesRev = graph_dataRev.split('\n')
    xRev = []
    yRev = []
    xRev.append(float(0))
    yRev.append(float(0))
    for line in linesRev:
        if len(line) > 1:
            yRevtxt,timeOnRev,timeChangeRev = line.split(',')
            xRev.append(float(xRev[-1])+float(timeChangeRev))
            yRev.append(float(yRevtxt))
            xRev.append(float(xRev[-1])+float(timeOnRev))
            yRev.append(float(yRevtxt))
    return xRev,yRev
    #ax[0].clear()
    #ax[0].plot(xRev,yRev)
    #X axis
    #major_ticksx1 = np.arange(0, 101, 5)
    #minor_ticksx1 = np.arange(0, 101, 1)
    #ax[0].set_xticks(major_ticksx1)
    #ax[0].set_xticks(minor_ticksx1, minor=True)
    #ax[0].grid(which='minor', alpha=0.2)
    #ax[0].grid(which='major', alpha=0.5, color='black')
    #Y axis
    #major_ticksy1 = np.arange(0, 3001, 500)
    #minor_ticksy1 = np.arange(0, 3001, 100)
    #ax[0].set_yticks(major_ticksy1)
    #ax[0].set_yticks(minor_ticksy1, minor=True)
    #ax[0].grid(which='minor', alpha=0.2)
    #ax[0].grid(which='major', alpha=0.5, color='black')
    #ax[0].set_ylabel('Rev/min', fontsize=20)


def valuesValve():
    #VALVE
    graph_dataValve = open('valuesValve.txt','r').read()
    linesValve = graph_dataValve.split('\n')
    xValve = []
    yValve = []
    xValve.append(float(0))
    yValve.append(float(0))
    for line in linesValve:
        if len(line)>1:
            yValvetxt,timeOnValve,timeChangeValve = line.split(',')
            xValve.append(float(xValve[-1])+float(timeChangeValve))
            yValve.append(float(yValvetxt))
            xValve.append(float(xValve[-1])+float(timeOnValve))
            yValve.append(float(yValvetxt))
    return xValve,yValve
    #ax[1].clear()
    #ax[1].plot(xValve,yValve)
    #ax[1].grid(True, color ="black")
    #X axis
    #major_ticksx2 = np.arange(0, 401, 20)
    #minor_ticksx2 = np.arange(0, 101, 5)
    #ax[1].set_xticks(major_ticksx2)
    #ax[1].set_xticks(minor_ticksx2, minor=True)
    #ax[1].grid(which='minor', alpha=0.2)
    #ax[1].grid(which='major', alpha=0.5, color='black')
    #ax[1].set_xlabel('Time', fontsize=30)
    #Y axis
    #major_ticksy2 = np.arange(0, 101, 25)
    #minor_ticksy2 = np.arange(0, 101, 5)
    #ax[1].set_yticks(major_ticksy2)
    #ax[1].set_yticks(minor_ticksy2, minor=True)
    #ax[1].grid(which='minor', alpha=0.2)
    #ax[1].grid(which='major', alpha=0.5, color='black')
    #ax[1].set_ylabel('Valve(%)', fontsize=20)

def plotGraphs():
    ani = animation.FuncAnimation(fig, animate,interval=1000)
    plt.show()


    