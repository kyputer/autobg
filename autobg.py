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
import schedule 
import time
import requests

def internet_on():
    try:
        requests.get('https://google.com', timeout=1)
        return True
    except requests.ConnectionError:
        return False

def find_resolution():
    res_x = 0
    res_y = 0
    res = str(subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0])
    res_x,res_y = res.split('x')
    res_y = int(res_y[:-3])
    res_x = int(res_x[2:])

    print("X: %s Y: %s" % (res_x, res_y) )

def download_new_images():
    if(internet_on()):
        print("Downloading latest flickr images based  on keyword")
        # wget the enclosed jpg
    else:
        print("Using local downloads")

def change_bg():
    print("Change Background image")
    return

if __name__ == '__main__':
    find_resolution()
    #schedule daily data download
    download_new_images()
    #schedule timely bg change
    change_bg()
    while True:
        schedule.run_pending();
        time.sleep(1)
