#!/usr/bin/python

TMP_PATH = None
RES_TYPE = 'stretch'
RES_X = 1024
RES_Y = 768
KEYWORD = "nature"
CONFIGS = {}
#IMG_DUR = 1200
#SEED_IMAGES = 5

import argparse
import subprocess
import urllib.request
import os
import sys
from sys import exit, stdout
from datetime import datetime, timedelta
import time
import requests
#import PIL
#from PIL import Image
#import schedule

parser = argparse.ArgumentParser(description='New daily backgrounds from flickr.')
parser.add_argument('-k', '--keyword', help='Set keyword')
parser.add_argument('-d', '--download-bg', help='Download new image from flickr', action="store_true")
parser.add_argument('-c','--change-bg', help='Change Background to Downloaded Image', action="store_true")

def load_configs():
    pass

def internet_on():
    """ Check if connected to Internet """
    try:
        requests.get('https://google.com', timeout=1)
        return True
    except requests.ConnectionError:
        return False

def download_new_image():
    """ Download a new image from flickr """
    if(internet_on()):
        print("Downloading latest flickr images based  on keyword")
        url = "https://api.flickr.com/services/feeds/photos_public.gne?tags=" + KEYWORD+"&tagmode=ANY&format=json&nojsoncallback=?"
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
    """ Change background"""
    subprocess.call(["feh", "--randomize", "--bg-fill", TMP_PATH])
    print("Change Background image")
    sys.exit()

def change_bg_if_old():
    pass

if __name__ == '__main__':
    TMP_PATH = os.path.dirname(os.path.realpath(__file__))
    CONFIGS = load_configs()
    args = parser.parse_args()
    if args.keyword:
        KEYWORD = args.keyword
    if not(args.download_bg or args.change_bg):
        change_bg_if_old()
    else:
        if args.download-bg:
            download_new_image()
            change_bg()
        if args.change-bg:
            change_bg()
