import sys
import os
import urllib.request
from tinydb import TinyDB, Query
import time
import datetime as dt
import json
import re
from synopy.base import Connection
from synopy.api import DownloadStationTask
import config as config

db = TinyDB(config.db_file)
table = db.table('tv_table')
tvs = []
def load_tvs_id():
    global tvs
    with open(config.movie_id_file) as movieid_data_file:
        tvs = json.load(movieid_data_file)

# Set up a connection
conn = Connection('http', config.synology_addr, port=config.synology_port)
# Authenticate and get an 'sid' cookie
conn.authenticate(config.synology_user, config.synology_pwd)

# Create an instance of the DownloadStationInfo API
dstask_api = DownloadStationTask(conn, version=3)

def get_data(tv,page):
    try:
        tvid = tv["resourceid"]
        tvname = tv["title"]
        print('tvid:'+tvid+' name:'+tvname+' page:'+str(page))
        url = 'https://eztv.re/api/get-torrents?limit=100&imdb_id='+tvid+'&page='+str(page)
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        u = urllib.request.urlopen(req, timeout=10).read()
        doc = json.loads(u)
        check_and_download(tv, doc)
        print(int(doc["torrents_count"]))
        if(int(doc["torrents_count"]) > page * 100):
            nextpage = page + 1
            get_data(tv,nextpage)
    except Exception as e:
        print("Unexpected error:", e)

def check_and_download(tv, doc):
    tvid = tv["resourceid"]
    tvname = tv["title"]
    for item in doc["torrents"]:
        try:
            filename = item["filename"]
            format = tv["format"].upper()
            if filename.upper().find(format) != -1:
                season = int(item["season"])
                episode = int(item["episode"])
                TV_Query = Query()
                tv_info = table.get((TV_Query.tvid == tvid) & (TV_Query.season == season) & (TV_Query.episode == episode))
                if tv_info is None:
                    magnet = item["magnet_url"]
                    if magnet is not None:
                        print('download '+tvname +' season:'+str(season)+' episode'+str(episode))
                        resp = dstask_api.create(uri=magnet,destination=config.synology_dest+tvname)
                        if resp.payload['success'] == True:
                            table.insert({'tvid':tvid,'tvname':tvname,'season':season,'episode':episode})
                        else:
                            print('download '+tvname +' season:'+str(season)+' episode'+str(episode)+' faile')
                    else:
                        print(tvname +' season:'+str(season)+' episode'+str(episode)+'has no magnet link, skip.')
                        table.insert({'tvid':tvid,'tvname':tvname,'season':season,'episode':episode,'status':'skip'})
        except Exception as e:
            print("Unexpected error:", e)
            continue

load_tvs_id()
while True:
    try:
        load_tvs_id()
        for tv in tvs:
            get_data(tv,1)
        now = dt.datetime.now()
        time.sleep(60*60)
    except Exception as e:
        print("Unexpected error:", e)
        time.sleep(60*60)
