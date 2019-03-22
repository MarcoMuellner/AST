#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as pl
from os import path
import argparse
"""
A short little script that plots 2-D ASCII files
"""

pl.rc('font', family='serif')
pl.rc('xtick', labelsize='x-small')
pl.rc('ytick', labelsize='x-small')

parser = argparse.ArgumentParser(description="A small little script to plot 2D datasets")
parser.add_argument('file',type=str,help="Filename")
parser.add_argument('-f','--fmt',type=str,help='Type of plot. Dots and so on',default='o')
parser.add_argument('-xs','--xscale',type=str,help="Scale of x-Axis",default='linear')
parser.add_argument('-ys','--yscale',type=str,help="Scale of y-Axis",default='linear')
parser.add_argument('-c','--colour',type=str,help="Colour",default='k')

args = parser.parse_args()

if not path.isfile(args.file):
    raise IOError(f"File {args.file} does not exist!")

if len(args.file.split(".")) > 1 and args.file.split(".")[1]  == 'npy':
    data = np.load(args.file)
else:
    data = np.loadtxt(args.file)

if data.shape[0] > data.shape[1]:
    data = data.T

pl.figure(figsize=(14,10))
pl.plot(data[0],data[1],args.fmt,markersize=1,linewidth=1,color=args.colour)
pl.xscale(args.xscale)
pl.yscale(args.yscale)
pl.title(args.file)
pl.tight_layout()
try:
    def quit_figure(event):
        if event.key == 'q':
            pl.close(event.canvas.figure)


    cid = pl.gcf().canvas.mpl_connect('key_press_event', quit_figure)
    pl.show()
except:
    pass