#!/usr/bin/python

DOWNLOAD_PATH = '~/Pictures/nasa/'
RES_TYPE = 'stretch'
RES_X = 1024
RES_Y = 768
#IMG_DUR = 1200
#SEED_IMAGES = 5
KEYWORDS = "nature"

import subprocess
import urllib.request
import PIL
import os
import sys
from PIL import Image
from sys import exit, stdout
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

def download_new_images():
    if(internet_on()):
        print("Downloading latest flickr images based  on keyword")
        url = "https://api.flickr.com/services/feeds/photos_public.gne?tags=" + KEYWORDS+"&tagmode=ANY&format=json&nojsoncallback=?"
        r = requests.get(url)
        for item in r.json()["items"]:
            img = item["media"]["m"][:-6] + "_b.jpg"
            print(img)
            #TODO urllib (where is it downloading the temp file?. Needs "dir+filename"
            filename = img.split('/')[-1]
            urllib.request.urlretrieve(str(img), filename)
    else:
        print("Using local downloads")

def change_bg():
    realpath = os.path.dirname(os.path.realpath(__file__))
    subprocess.call(["feh", "--randomize", "--bg-fill", realpath])
    print("Change Background image") 
    sys.exit()
    return

if __name__ == '__main__':
    #find_resolution()
    #schedule daily data download
    download_new_images()
    #schedule timely bg change
    change_bg()
    while True:
        schedule.run_pending();
        time.sleep(1)
