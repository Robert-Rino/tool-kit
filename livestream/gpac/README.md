# GPAC research 

## Generate test stream to named pipe

```shell
mkfifo stream
export STREAM=$(pwd)/stream

ffmpeg \
    -re -f lavfi -i testsrc=size=640x360:rate=30:decimals=3 \
    -re -f lavfi -i sine=f=220:b=8:sample_rate=48000 -shortest \
    -filter_complex "
    [0:v]format=yuv420p[v];
    [v]split=1[v0]
    " \
    -force_key_frames 'expr:gte(t,n_forced*1)' \
    -c:v libx264 -r:v 30 -keyint_min 30 -g 30 \
    -preset:v ultrafast -profile:v high -tune zerolatency \
    -b:v:0 2M -b:v:1 1M \
    -c:a aac -r:a 48000 -ac:a 2 \
    -map '[v0]' \
    -map 1 \
    -f mpegts pipe:1 > $STREAM
    
    
// ffplay $STREAM
```


## Package with gpac
```shell
gpac \
    -log-utc \
    -logs=all@info \
    -graph \
    -dbg-edges \
    -i "pipe:///Users/nino/Repository/tool-kit/stream:block_size=1024:FID=SOURCE" \
    "rfnalu:SID=SOURCE:FID=videos-private" \
    "rfadts:SID=SOURCE:FID=audios-private" \
    "dasher:SID=videos-private,audios-private:segdur=1:cdur=1:tsb=6:buf=0:cmaf=cmfc:refresh=60:info:initext=cbcs.mp4:segext=cbcs.m4s:profile=live:dmode=dynamic:pssh=mv:FID=dashed-private" \
    -o  live.mpd:dmode=dynamic \
    
// ffplay live.mpd
```


## Package with gpac DRMed

```shell
gpac \
 --graph --segdur=1 --cdur=1 --asto=0 --spd=2000 --tsb=30 --cmaf=cmfc --refresh=15 --buf=0 --info --initext=clear.mp4 --segext=clear.m4s --profile=dashif.ll --dmode=dynamic --hlsc \
 -i pipe:///Users/nino/Repository/tool-kit/stream:block_size=1024:FID=SOURCE:block_size=1024:FID=SOURCE \
 'rfnalu:SID=SOURCE#video1:FID=videos-public' \
 'rfadts:SID=SOURCE#audio3:FID=audios-public' \
'dasher:SID=videos-public,audios-public:title=public:mname=public.mpd:template=public-ll/$Type$-$RepresentationID$-$Number%05d$$Init=00000$:FID=dashed-public-dash' \
-o http://localhost:8080/public.mpd:SID=dashed-public-dash:rdirs=/Users/nino/Repository/tool-kit/html:cors=on:reqlog=GET \
rfnalu:SID=SOURCE:FID=videos-private-dash \
'rfadts:SID=SOURCE#audio3:FID=audios-private' \
cecrypt:SID=videos-private-dash:cfile=/Users/nino/Repository/tool-kit/cenc.xml:FID=videos-private-encrypted-dash \
'dasher:SID=videos-private-encrypted-dash,audios-private:pssh=mv:title=private:mname=private.mpd:template=private-ll/$Type$-$RepresentationID$-$Number%05d$$Init=00000$:FID=dashed-private-dash'  \
-o http://localhost:8080/private.mpd:SID=dashed-private-dash:rdirs=/Users/nino/Repository/tool-kit/html:cors=on:reqlog=GET 


```
