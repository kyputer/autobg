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
import time
import requests
import random
import json
from crontab import CronTab

parser = argparse.ArgumentParser(description='New daily backgrounds from flickr.')
parser.add_argument('-k', '--keyword', help='Set keyword')
parser.add_argument('-d', '--download-bg', help='Download new image from flickr', action="store_true")
parser.add_argument('-c','--change-bg', help='Change Background to Downloaded Image', action="store_true")
parser.add_argument('-s','--stop-job', help='Stop periodicaly downloading new images', action="store_true")
parser.add_argument('-i','--interval', type=int, help='Interval for change, in minutes')

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
        requests.get('https://google.com', timeout=4)
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
        configs["updated_at"] = str_time = time.strftime("%m.%d.%y-%H:%M", time.localtime())
        configs["filename"] = filename = '%s.jpg' % str_time
        urllib.request.urlretrieve(str(img), os.path.join(TMP_PATH, filename))
        CONFIGS = configs
        set_configs(configs)
    else:
        print("Unable to download new image")

def change_bg():
    """ Change background"""
    global CONFIGS
    if CONFIGS and CONFIGS["filename"]:
        handle_bg_change(CONFIGS["filename"], TMP_PATH)
        print("Change Background image")
    sys.exit()

def handle_bg_change(filename, filepath):
    #subprocess.call(["feh", os.path.join(filepath, filename), "--bg-fill"])
    subprocess.call(["gsettings", "set", "org.gnome.desktop.background",
                    "picture-uri", "file://" + os.path.join(filepath, filename)])

def a_interval_old(s_time):
    """ Check if time is a day hold"""
    global INTERVAL
    tm = time.strptime(s_time, "%m.%d.%y-%H:%M")
    if (time.mktime(time.localtime()) - time.mktime(tm)) >= (INTERVAL * 60):
        return True
    return False

def change_bg_if_old():
    """ Change background on first run or after a day """
    global CONFIGS
    if not(CONFIGS) or a_interval_old(CONFIGS["updated_at"]):
        download_new_image()
        change_bg()

def schedule_next_download(disable=False):
    global CONFIGS, KEYWORD,INTERVAL
    configs = CONFIGS
    cron = CronTab(user=True)
    if 'job_cmd' in configs.keys():
        cron.remove(cron.find_command((configs['job_cmd'])))
    if not disable:
        configs['job_cmd'] = job_cmd = "%s -k %s -i %i" % (os.path.realpath(__file__), KEYWORD, INTERVAL)
        job = cron.new(command=job_cmd)
        day = (INTERVAL%10080)//1440
        hour = ((INTERVAL%10080)%1440)//60
        minute = ((INTERVAL%10080)%1440)%60
        job.day.every(1 or day)
        job.hour.every(1 or hour)
        job.minute.every(1 or minute)
        job.enable()
        set_configs(configs)
    cron.write()

if __name__ == '__main__':
    global CONFIGS, KEYWORD, INTERVAL
    TMP_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tmp")
    #print(TMP_PATH)
    CONFIGS = load_configs()
    args = parser.parse_args()
    KEYWORD = args.keyword or "nature"
    INTERVAL = args.interval or 1440
    if not(args.download_bg or args.change_bg):
        change_bg_if_old()
    else:
        if args.download_bg:
            download_new_image()
            change_bg()
        if args.change_bg:
            change_bg()
    schedule_next_download(args.stop_job)
