#!/usr/bin/python

DOWNLOAD_PATH = '/tmp/background'
RES_TYPE = 'stretch'
RES_X = 1024
RES_Y = 768
#IMG_DUR = 1200
#SEED_IMAGES = 5
KEYWORDS = "nature"

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
    res = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]

def download_new_images():
    if(internet_on()):
        print("Downloading latest flickr images based  on keyword")
        url = "https://api.flickr.com/services/feeds/photos_public.gne?tags=" + KEYWORDS+"&tagmode=ANY&format=json&nojsoncallback=?"
        r = requests.get(url)
        for item in r.json()["items"]:
            img = item["media"]["m"][:-6] + "_b.jpg"
            print(img)
    else:
        print("Using local downloads")

def change_bg():
    res_x = RES_X
    res_y = RES_Y
    print("Change Background image")
    return int(res_x), int(res_y)

if __name__ == '__main__':
    #schedule daily data download
    download_new_images()
    #schedule timely bg change
    change_bg()
    while True:
        schedule.run_pending();
        time.sleep(1)
