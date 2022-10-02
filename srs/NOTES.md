ffmpeg -f avfoundation -framerate 30 -pix_fmt yuyv422 -i "0" \
-filter_complex "[0:0]boxblur=luma_radius=10:luma_power=1[base-video]" -map "[base-video]" -f matroska - | ffplay -i -


ffmpeg -f avfoundation -framerate 30 -pix_fmt yuyv422 -i "0" -f h264 rtmp://localhost/live/livestream


ffplay rtmp://localhost/live/livestream

ffmpeg -rtmp_buffer 3000  -rtmp_live  live -f live_flv -i rtmp://localhost/live/livestream \
-filter_complex "[0]copy[base]" -map "[base]" -f matroska - | ffplay -i -
