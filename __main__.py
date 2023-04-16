from multiprocessing.connection import wait
from time import sleep
from randomNumberGenerator import *
from matplotlibGraphics import *
from turtle import color
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from numpy import append
import numpy as np

def main():
    deleteFiles() #If we want to delete our files used for our graphs. We can put in the beggining
    #This will give us the numbers we want
    revRandomNumberGenerator() 
    valveNumberGenerator()
    plotGraphs()
    

if __name__ == "__main__":
    main()