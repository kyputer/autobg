#!/usr/bin/python

DOWNLOAD_PATH = '/tmp/background'
RES_TYPE = 'stretch'
RES_X = 1024
RES_Y = 768
#IMG_DUR = 1200
#SEED_IMAGES = 5

import subprocess
import PIL
from PIL import Image
from sys import stdout
from sys import exit
from datetime import datetime, timedelta

def find_resolution():
    res_x = 0
    res_y = 0

    res = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]

    res_x = RES_X
    res_y = RES_Y
    
    print (output)

    return int(res_x), int(res_y)
find_resolution()
