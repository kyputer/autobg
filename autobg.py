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

    p1 = subprocess.Popen(["xrandr"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", regex_search], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    output = p2.communicate()[0]

def download_new_images():
    if(internet_on()):
        print("Downloading latest flickr images based  on keyword")
    else:
        print("Using local downloads")

def change_bg():
    print("Change Background image")

if __name__ == '__main__':
    #schedule daily data download
    download_new_images()
    #schedule timely bg change
    change_bg()
    while True:
        schedule.run_pending();
        time.sleep(1)
