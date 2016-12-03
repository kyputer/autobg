#!/usr/bin/python

DOWNLOAD_PATH = '/tmp/background'
RES_TYPE = 'stretch'
RES_X = 1024
RES_Y = 768
#IMG_DUR = 1200
#SEED_IMAGES = 5

from PIL import Image
from sys import stdout
from sys import exit
from datetime import datetime, timedelta

def find_resolution():
    res_x = 0
    res_y = 0

    p1 = subprocess.Popen(["xrandr"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", regex_search], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    output = p2.communicate()[0]

