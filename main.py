import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import scipy as sp
import networkx as nx
from cgshop2021_pyutils import InstanceDatabase, Instance, Solution, SolutionStep, SolutionZipWriter, Direction, validate, ZipReaderError, InvalidSolutionError, SolutionEncodingError
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import random
from matplotlib.ticker import MaxNLocator

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Palatino"],
})


def generate_pixel(coods, pixtype):
    
    if pixtype == 'obstacle':
        facecolor = 'black'
        alpha = 1.0

    elif pixtype == 'free':
        facecolor = 'white'
        alpha = 0.0

    elif pixtype == 'start' :
         facecolor = 'red'
         alpha = 0.5

    elif pixtype == 'target':
          facecolor = 'green'
          alpha = 0.5
    
    xc, yc     = coods
    xllc, yllc = xc-0.5, yc-0.5
    pixel      = Rectangle((xllc, yllc),1.0,1.0, facecolor=facecolor, edgecolor='k', alpha=alpha)

    return pixel


def generate_pixel_grid (ax, instance):

    i          = instance
    xmin, xmax = np.inf, -np.inf
    ymin, ymax = np.inf, -np.inf
    
    for r in range(i.number_of_robots):
        start    = i.start_of(r)
        target   = i.target_of(r)

        if start[0] < xmin:
            xmin = start[0]
        if start[0] > xmax:
            xmax = start[0]
        if start[1] < ymin:
            ymin = start[1]
        if start[1] > ymax:
            ymax = start[1]

        pixel1 = generate_pixel(start,pixtype='start')
        pixel2 = generate_pixel(target,pixtype='target')
        ax.add_patch(pixel1)
        ax.add_patch(pixel2)

    for o in i.obstacles:
        pixel = generate_pixel(o,pixtype='obstacle')
        ax.add_patch(pixel)


    ax.set_aspect(1.0)
    ax.set_xlim([xmin-1,xmax+1])
    ax.set_ylim([ymin-1,ymax+1])
    ax.set_title("Number of robots: "+str(i.number_of_robots))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

from colorama import Fore, Style
import time

idb     = InstanceDatabase("cgshop_2021_instances_01.zip")
counter = 0
for i in idb:
   print(Fore.YELLOW, "Writing plot of instance ", i, "Number of robots: ", i.number_of_robots, Style.RESET_ALL)
   counter += 1
   fig, ax = plt.subplots()
   generate_pixel_grid(ax,i)
   
   print("...pixel grid generated!", Style.RESET_ALL)

   start = time.time()
   plt.savefig('file'+format(counter, '04d')+'_'+'numrobs-'+str(i.number_of_robots),dpi=300,bbox_inches='tight')
   end = time.time()
   
   print(Fore.GREEN, "...Finished!...", (end-start),  "seconds taken for disk write" , Style.RESET_ALL)
   plt.close()
