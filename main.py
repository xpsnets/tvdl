import sys
import os
from urllib.request import urlopen
from tinydb import TinyDB, Query
from xml.etree.ElementTree import parse
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

def check_and_download():
    for tv in tvs:
        try:
            tvid = tv["resourceid"]
            tvname = tv["title"]
            u = urlopen('http://rss.rrys.tv/rss/feed/'+tvid)
            doc = parse(u)
            for item in doc.iterfind('channel/item'):
                try:
                    title = item.findtext('title')
                    format = tv["format"].upper()
                    if title.upper().find(format) != -1:
                        matchObj = re.search( r'S(..)E(..)', title)
                        if matchObj:
                            season = int(matchObj.group(1))
                            episode = int(matchObj.group(2))
                            if is_init == False:
                                table.insert({'tvid':tvid,'tvname':tvname,'season':season,'episode':episode})
                            else:
                                TV_Query = Query()
                                tv_info = table.get((TV_Query.tvid == tvid) & (TV_Query.season == season) & (TV_Query.episode == episode))
                                if tv_info is None:
                                    magnet = item.findtext('magnet')
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
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    continue
        except:
            print("Unexpected error:", sys.exc_info()[0])
            continue

Init_Query = Query()
reuslt = db.get(Init_Query.isInit == True)
load_tvs_id()
is_init = True
if reuslt is None:
    print('not init')
    is_init = False
    db.purge_table('tv_table')
    check_and_download()
    db.insert({'isInit':True})
    is_init = True
    print('init complate')

while True:
    try:
        load_tvs_id()
        check_and_download()
        now = dt.datetime.now()
        time.sleep(30*60)
    except :
        print("Unexpected error:", sys.exc_info()[0])
        time.sleep(30*60)
