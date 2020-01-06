# zmzDLer

### Docker 环境变量

- SYNOLOGY_ADDR //群晖web地址
- SYNOLOGY_PORT //群晖web端口
- SYNOLOGY_USERNAME //群晖username
- SYNOLOGY_PWD //群晖密码

- SYNOLOGY_DEST //download station 目标地址

### Docker 文件

#### 目录 /data

- tv_db.json 下载记录
- movieid.json 需要下载剧集ID

movieid.json文件格式
```
[
  {
    "resourceid":"35113",
    "format":"MP4",
    "title":"Taken"
  }
]
```

### 脚本

```
docker run -d 
    -v /your/data/path:/data 
    -e "SYNOLOGY_ADDR=your_syno_addr" 
    -e "SYNOLOGY_PORT=5000" 
    -e "SYNOLOGY_USERNAME=your_syno_user" 
    -e "SYNOLOGY_PWD=your_syno_pwd"
    -e "SYNOLOGY_DEST=Video/TV/"
    xpsnets/zmzdler
```
