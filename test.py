import config_test as config
import qbittorrentapi

conn_info = dict(
    host=config.server_addr,
    port=config.server_port,
    username=config.server_user,
    password=config.server_pwd,
)

magnet = "magnet:?xt=urn:btih:030dee20833d64f60f1c03978419cae49314e39f&tr=udp://9.rarbg.to:2710/announce&tr=udp://9.rarbg.me:2710/announce&tr=http://tr.cili001.com:8070/announce&tr=http://tracker.trackerfix.com:80/announce&tr=udp://open.demonii.com:1337&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://p4p.arenabg.com:1337&tr=wss://tracker.openwebtorrent.com&tr=wss://tracker.btorrent.xyz&tr=wss://tracker.fastcast.nz"

# qbt_client = qbittorrentapi.Client(**conn_info)

# try:
#     qbt_client.auth_log_in()
# except qbittorrentapi.LoginFailed as e:
#     print(e)

# print(f"qBittorrent: {qbt_client.app.version}")
# print(f"qBittorrent Web API: {qbt_client.app.web_api_version}")

with qbittorrentapi.Client(**conn_info) as qbt_client:
    if qbt_client.torrents_add(urls=magnet,savepath="/vol1/1000/Download") != "Ok.":
        raise Exception("Failed to add torrent.")


# dwn = downloadstation.DownloadStation(config.server_addr,config.server_port,config.server_user,config.server_pwd,dsm_version=7)
# print(dwn.get_info())
# # params = dict()
# # params['destination'] = config.synology_dest+"Tyrant"
# resp = dwn.create_task(uri=magnet)
# print(resp)