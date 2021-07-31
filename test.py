import config_test as config
from synology_api import downloadstation

dwn = downloadstation.DownloadStation(config.synology_addr,config.synology_port,config.synology_user,config.synology_pwd,dsm_version=7)
print(dwn.get_info())
magnet = "magnet:?xt=urn:btih:030dee20833d64f60f1c03978419cae49314e39f&tr=udp://9.rarbg.to:2710/announce&tr=udp://9.rarbg.me:2710/announce&tr=http://tr.cili001.com:8070/announce&tr=http://tracker.trackerfix.com:80/announce&tr=udp://open.demonii.com:1337&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://p4p.arenabg.com:1337&tr=wss://tracker.openwebtorrent.com&tr=wss://tracker.btorrent.xyz&tr=wss://tracker.fastcast.nz"
params = dict()
params['destination'] = config.synology_dest+"Work.in.Progress"
resp = dwn.create_task(uri=magnet,additional_param=params)
print(resp)