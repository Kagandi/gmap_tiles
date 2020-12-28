#!/usr/bin/python

import urllib.request as urllib
from urllib.error import HTTPError
import os, sys
from gmap_utils import *
from tqdm import tqdm
import time
import random

def download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, output_folder, satellite=True):

    start_x, start_y = latlon2xy(zoom, lat_start, lon_start)
    stop_x, stop_y = latlon2xy(zoom, lat_stop, lon_stop)
    

    counter = 0
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
    headers = { 'User-Agent' : user_agent }
    title_count = (stop_x-start_x)*(stop_y-start_y)
    with tqdm(total=title_count) as pbar:
        for x in range(start_x, stop_x):
            for y in range(start_y, stop_y):
                counter+=1
                pbar.update(1)
                url = None
                filename = None

                if satellite:        
    #                 http://khms1.google.com/kh/v=878?x=4888&y=3345&z=13
                    url = "http://khms0.google.com/kh/v=878?hl=en&x=%d&y=%d&z=%d" % (x, y, zoom)
    #                 print(url)
                    filename = "%d_%d_%d_s.jpg" % (zoom, x, y)
                else:
                    url = "http://mt1.google.com/vt/lyrs=h@162000000&hl=en&x=%d&s=&y=%d&z=%d" % (x, y, zoom)
                    filename = "%d_%d_%d_r.png" % (zoom, x, y)    

                if not os.path.exists(f"{output_folder}/{filename}"):

                    bytes = None

                    try:
                        req = urllib.Request(url, data=None, headers=headers)
                        response = urllib.urlopen(req)
                        bytes = response.read()
                    except HTTPError as e:
                        print(f"Http error: {e.code}")
                        time.sleep(60*5)
                    except Exception as e:
                        print( "--", filename, "->", e)
                        sys.exit(1)
                        
                    if bytes.startswith(b"<html>"):
                        print("-- forbidden", filename)
                        sys.exit(1)

#                     print( "-- saving", filename)

                    f = open(f"{output_folder}/{filename}",'wb')
                    f.write(bytes)
                    f.close()

                    time.sleep(1 + random.random() + (2*counter)/title_count)

if __name__ == "__main__":
    
    zoom = 15

    lat_start, lon_start = 46.53, 6.6
    lat_stop, lon_stop = 46.49, 6.7
        
    download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True)
