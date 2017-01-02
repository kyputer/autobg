#!/usr/bin/python

TMP_PATH = None
RES_TYPE = 'stretch'
RES_X = 1024
RES_Y = 768
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
import random
import json
#import PIL
#from PIL import Image
#import schedule

parser = argparse.ArgumentParser(description='New daily backgrounds from flickr.')
parser.add_argument('-k', '--keyword', help='Set keyword')
parser.add_argument('-d', '--download-bg', help='Download new image from flickr', action="store_true")
parser.add_argument('-c','--change-bg', help='Change Background to Downloaded Image', action="store_true")

def load_configs():
    """ Retrieve configs from .autobg file """
    dotautobg_path = os.path.join(TMP_PATH, ".autobg")
    if os.path.isfile(dotautobg_path):
        with open(dotautobg_path) as dotautobg:
            return json.load(dotautobg)
    else:
        return {}

def set_configs(configs):
    """ Update autobg file """
    dotautobg_path = os.path.join(TMP_PATH, ".autobg")
    with open(dotautobg_path, 'w') as dotautobg:
        json.dump(configs, dotautobg)

def internet_on():
    """ Check if connected to Internet """
    try:
        requests.get('https://google.com', timeout=1)
        return True
    except requests.ConnectionError:
        return False

def download_new_image():
    """ Download a new image from flickr """
    global CONFIGS, KEYWORD
    if(internet_on()):
        if CONFIGS and CONFIGS["filename"]:
            os.remove(os.path.join(TMP_PATH, CONFIGS["filename"]))

        print("Downloading latest flickr images based  on keyword")
        url = "https://api.flickr.com/services/feeds/photos_public.gne?tags=" + KEYWORD+"&tagmode=ANY&format=json&nojsoncallback=?"
        r = requests.get(url)
        item = r.json()["items"][random.randint(0, len(r.json()["items"]) -1)]
        img = item["media"]["m"][:-6] + "_b.jpg"
        #TODO urllib (where is it downloading the temp file?. Needs "dir+filename"
        configs = {}
        configs["updated_at"] = str_time = time.strftime("%m.%d.%y %H:%M", time.localtime())
        configs["filename"] = filename = '%s.jpg' % str_time
        urllib.request.urlretrieve(str(img), filename)
        CONFIGS = configs
        set_configs(configs)
    else:
        print("Unable to download new image")

def change_bg():
    """ Change background"""
    global CONFIGS
    filepath = os.path.join(TMP_PATH, CONFIGS["filename"])
    subprocess.call(["feh", "", "--bg-fill", TMP_PATH])
    print("Change Background image")
    sys.exit()

def a_dayold(s_time):
    """ Check if time is a day hold"""
    tm = time.strptime(s_time, "%m.%d.%y %H:%M")
    if (time.mktime(time.localtime()) - time.mktime(tm)) >= 86400000:
        return True
    return False

def change_bg_if_old():
    """ Change background on first run or after a day """
    global CONFIGS
    if not(CONFIGS) or a_dayold(CONFIGS["updated_at"]):
        download_new_image()
        change_bg()
    #schedule_next run for when a day old

if __name__ == '__main__':
    global CONFIGS, KEYWORD
    TMP_PATH = os.path.dirname(os.path.realpath(__file__))
    CONFIGS = load_configs()
    args = parser.parse_args()
    KEYWORD = args.keyword or "nature"
    if not(args.download_bg or args.change_bg):
        change_bg_if_old()
    else:
        if args.download_bg:
            download_new_image()
            change_bg()
        if args.change_bg:
            change_bg()
