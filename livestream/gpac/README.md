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


## Simulate production behavior

1. `docker compose up`

2. Open 2 terminal
    2.1: `docker compose exec encoder bash`, `docker compose exec gpac bash`

    2.2: encoder command
    ```sh
        ffmpeg \
        -re -f lavfi -i testsrc=size=640x360:rate=30:decimals=3 \
        -re -f lavfi -i sine=f=220:b=8:sample_rate=48000 -shortest \
        -filter_complex "
        [0:v]format=yuv420p[v];
        [v]split=4[v0][v1][v2][v3]
        " \
        -force_key_frames 'expr:gte(t,n_forced*1)' \
        -c:v libx264 -r:v 30 -keyint_min 30 -g 30 \
        -preset:v ultrafast -profile:v high -tune zerolatency \
        -b:v:0 2M -b:v:1 1M \
        -c:a aac -r:a 48000 -ac:a 2 \
        -map '[v0]' \
        -map '[v1]' \
        -map '[v2]' \
        -map '[v3]' \
        -map 1 \
        -f mpegts pipe:1 > stream
    ```

    2.3: gpac command
    ```sh
    gpac \
    --utcs=https://time.akamai.com \
    --segdur=1 \
    --cdur=1 \
    --asto=0 \
    --spd=2000 \
    --tsb=30 \
    --cmaf=cmfc \
    --refresh=15 \
    --buf=0 \
    --info \
    --initext=clear.mp4 \
    --segext=clear.m4s \
    --profile=dashif.ll \
    --dmode=dynamic \
    --hlsc \
    -i  pipe:///usr/src/app/stream:block_size=1024:FID=SOURCE \
    'rfnalu:SID=SOURCE#video1:#Representation=video-ll-ld:#Quality=ld:#HLSPL=$OType$-ll-$pname=Quality$.m3u8:FID=video-public-ld' \
    'rfnalu:SID=SOURCE#video2:#Representation=video-ll-sd:#Quality=sd:#HLSPL=$OType$-ll-$pname=Quality$.m3u8:FID=video-public-sd' \
    'rfadts:SID=SOURCE#audio5:#Representation=audio-ll-ld:#Quality=ld:#HLSPL=$OType$-ll-$pname=Quality$.m3u8:FID=audio-public-sd' \
    'dasher:SID=video-public-ld,video-public-sd,audio-public-sd:title=public-ll:mname=public.mpd:template=$RepresentationID$-$Number%05d$$Init=00000$:FID=dashed-public-dash' \
    -o http://localhost:8080/public.mpd:SID=dashed-public-dash:rdirs=html:cors=on:reqlog=GET \
    'dasher:SID=video-public-ld,video-public-sd,audio-public-sd:mname=public.m3u8:llhls=br:segdur=1.2:cdur=0.6:asto=0.6:template=$OType$-ll-$pname=Quality$-hls-$Number%05d$$Init=00000$:FID=dashed-public-hls' \
    -o http://localhost:8080/public.m3u8:SID=dashed-public-hls \
    'rfnalu:SID=SOURCE#video3:#Representation=video-ll-ld:#Quality=ld:#HLSPL=$OType$-ll-$pname=Quality$-cbcs.m3u8:FID=video-private-ld' \
    'rfnalu:SID=SOURCE#video4:#Representation=video-ll-sd:#Quality=sd:#HLSPL=$OType$-ll-$pname=Quality$-cbcs.m3u8:FID=video-private-sd' \
    'rfadts:SID=SOURCE#audio5:#Representation=audio-ll-ld:#Quality=ld:#HLSPL=$OType$-ll-$pname=Quality$-cbcs.m3u8:FID=audio-private-sd' \
    'cecrypt:SID=video-private-ld,video-private-sd:cfile=/usr/src/app/cenc.xml:FID=videos-private-encrypted-dash' \
    'dasher:SID=videos-private-encrypted-dash,audio-private-sd:pssh=mv:title=private:mname=private.mpd:template=$RepresentationID$-cenc-$Number%05d$$Init=00000$:FID=dashed-private-dash' \
    -o http://localhost:8080/private.mpd:SID=dashed-private-dash \
    'cecrypt:SID=video-private-ld,video-private-sd:cfile=/src/app/cbcs.xml:FID=videos-private-encrypted-hls::#HLSKey=skd://9A04F07998404286AB92E65BE0885F95,KEYFORMAT="com.apple.streamingkeydelivery",KEYFORMATVERSIONS=1' \
    'dasher:SID=videos-private-encrypted-hls,audio-private-sd:mname=private.m3u8:llhls=br:segdur=1.2:cdur=0.6:asto=0.6:template=$OType$-ll-$pname=Quality$-cbcs-$Number%05d$$Init=00000$:FID=dashed-private-hls' \
    -o http://localhost:8080/private.m3u8:SID=dashed-private-hls
    ```

3. 
    - play public mpd
    `ffplay http://localhost:8081/6566fe555202c2571f15cce4/public.mpd\?profile=ll`

    - play private DRMed mpd
    `ffplay -cenc_decryption_key '8704aeedecd6aae0413e3d53d2d1f60e' -i http://localhost:8081/6566fe555202c2571f15cce4/public.mpd\?profile\=ll`

    - play public m3u8
    `http://localhost:8081/6566fe555202c2571f15cce4/public.m3u8?profile=ll`
