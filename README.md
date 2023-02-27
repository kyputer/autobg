# autobg
## TODO work on chrontab
```bash
sudo pip install -r requirements.txt
```
### Run
By default it is scheduled to change daily.
```
./autobg.py
```

### Schedule background change
To schedule background autobg to run a different intervals, pass the interval using the -i flag.
```
./autobg.py -i <Interval in Minutes e.i 2 >
```

### Force background change
```
./autobg.py -d
```

### Window manager example
```
./autobg.py -d -m -k nature
```

### Help
```
usage: autobg.py [-h] [-k KEYWORD] [-d] [-c] [-s] [-i INTERVAL] [-m]

New daily backgrounds from flickr.

optional arguments:
  -h, --help            show this help message and exit
  -k KEYWORD, --keyword KEYWORD
                        Set keyword
  -d, --download-bg     Download new image from flickr
  -c, --change-bg       Change Background to Downloaded Image
  -s, --stop-job        Stop periodicaly downloading new images
  -i INTERVAL, --interval INTERVAL
                        Interval for change, in minutes
  -m, --window-manager  Use feh for window managers
```
![alt tag](https://raw.githubusercontent.com/kylesuero/autobg/master/ss1.png)
