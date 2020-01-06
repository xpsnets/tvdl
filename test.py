from synopy.base import Connection
from synopy.api import DownloadStationTask
import config_test as config

# Set up a connection
conn = Connection('http', config.synology_addr, port=config.synology_port)
# Authenticate and get an 'sid' cookie
conn.authenticate(config.synology_user, config.synology_pwd)

# Create an instance of the DownloadStationInfo API
dstask_api = DownloadStationTask(conn, version=3)
magnet = "magnet:?xt=urn:btih:030dee20833d64f60f1c03978419cae49314e39f&tr=udp://9.rarbg.to:2710/announce&tr=udp://9.rarbg.me:2710/announce&tr=http://tr.cili001.com:8070/announce&tr=http://tracker.trackerfix.com:80/announce&tr=udp://open.demonii.com:1337&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://p4p.arenabg.com:1337&tr=wss://tracker.openwebtorrent.com&tr=wss://tracker.btorrent.xyz&tr=wss://tracker.fastcast.nz"
resp = dstask_api.create(uri=magnet,destination=config.synology_dest+"Work.in.Progress")
print(resp.payload)