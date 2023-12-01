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
    -f tee -use_fifo 1 -y \
    "[f=mpegts:onfail=ignore:select=\\'v:0,a:0\\']tcp://127.0.0.1:4000"


# Play stream
- ffplay (seems no llhls support)
`ffplay http://localhost:8000/stream/public-ll/llhls.m3u8`

- ovenMedia player
https://demo.ovenplayer.com/


