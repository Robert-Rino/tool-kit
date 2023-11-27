# Produce test stream

ffmpeg \
    -re -f lavfi -i testsrc=size=640x360:rate=30:decimals=3 \
    -re -f lavfi -i sine=f=220:b=8:sample_rate=48000 -shortest \
    -filter_complex "
    [0:v]format=yuv420p[v];
    [v]drawtext=boxcolor=black:text='%{localtime\:%H.%M.%S}':x=(w/2):y=(h/4):fontfile=OpenSans.ttf:fontsize=30:fontcolor=black[v]
    " \
    -force_key_frames 'expr:gte(t,n_forced*1)' \
    -c:v libx264 -r:v 30 -keyint_min 30 -g 30 \
    -preset:v ultrafast -profile:v high -tune zerolatency \
    -b:v:0 2M -b:v:1 1M \
    -c:a aac -r:a 48000 -ac:a 2 \
    -map '[v]' \
    -map 1 \
    -pes_payload_size 0 -f mpegts udp://127.0.0.1:4000


# Play stream
ffplay http://:3333/app/stream_4000/llhls.m3u8

https://4d15-59-124-114-73.ngrok-free.app/app/stream_4000/llhls.m3u8


https://4d15-59-124-114-73.ngrok-free.app/app/stream_4000/llhls.m3u8
