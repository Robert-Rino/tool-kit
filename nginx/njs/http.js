// const MASTER_HLS = (group) =>`
// #EXTM3U
// ## Generated with https://github.com/google/shaka-packager version v2.5.1-9f11077-release

// #EXT-X-INDEPENDENT-SEGMENTS

// #EXT-X-MEDIA:TYPE=AUDIO,URI="audio.m3u8",GROUP-ID="default-audio-group",NAME="stream_1",AUTOSELECT=YES,CHANNELS="2"

// #EXT-X-STREAM-INF:BANDWIDTH=1325841,AVERAGE-BANDWIDTH=423202,CODECS="avc1.f4001f,mp4a.40.2",RESOLUTION=960x400,FRAME-RATE=30.000,VIDEO-RANGE=SDR,AUDIO="default-audio-group",CLOSED-CAPTIONS=NONE
// preview-b30-${group}.m3u8`

const fs = require('fs');
const querystring = require('querystring');

// function getSlotInfo() {
//     const SEGMENT_DURATION = 3
//     const BLUROUT_CYCLE = 30

//     var mpd = fs.readFileSync('/statics/public-b30.mpd', {encoding: 'utf8'});

//     const regex = new RegExp('availabilityStartTime="([\\d\\-T\\:Z]+)"');
//     const startTimeStr = mpd.match(regex)[1];
//     const startTime = new Date(startTimeStr);
//     const currentTime = Date.now();
//     const duration = Math.floor((currentTime - startTime) / 1000);
    
//     const n = Math.floor(duration / $(SEGMENT_DURATION)) % (BLUROUT_CYCLE / $(SEGMENT_DURATION));
//     const expires = $(SEGMENT_DURATION) - (duration % $(SEGMENT_DURATION))

//     return {slot: n, expires: expires}

// }

function hello(r) {
    r.error(appendQueryString(r.uri, {100}))
    // r.return(200, `Hello world!, ${info}, ${expires}`);
    r.return(200, 'ok')
}

function now(r) {
    var seconds = Math.floor(new Date().getTime() / 1000);
    r.return(200, seconds);
}

function appendQueryString (url, params) {
    let parts = url.split('?');
    let path = parts[0];
    let qs = Object.assign({}, querystring.parse(parts[1]), params);
    // return `${path}?${querystring.stringify(qs)}`;
    return querystring.stringify(qs)
  }

async function start(r){
    let mpd = await r.subrequest(
        '/public-b30.mpd',
    ).then((reply) => {return reply.responseBody})
    
    let now = Math.floor(new Date().getTime() / 1000);
    let startTimeString = mpd.match(/ailabilityStartTime=\"([\dT\-:]+)Z\"/)[1]
    let startTimeUnix = Math.floor(Date.parse(startTimeString) / 1000)
    r.return(200, startTimeUnix)
}

// async function master(r) {
//     // These value should come from env
//     let CYCLE = 30
//     let SEGMENT_DURATION = 3

//     let mpd = await r.subrequest(
//         '/public-b30.mpd',
//     ).then((reply) => {return reply.responseBody})
    
//     let now = r.args['now'] | Math.floor(new Date().getTime() / 1000);
//     let startTimeString = mpd.match(/ailabilityStartTime=\"([\dT\-:]+)Z\"/)[1]
//     let startTimeUnix = Math.floor(Date.parse(startTimeString) / 1000)
//     let group = Math.floor((now - startTimeUnix) / CYCLE)

//     r.return(200, MASTER_HLS(group));
// }

async function master(r) {
    const CYCLE = 30
    const SEGMENT_DURATION = 3
    const SEGMENTS_ONE_CYCLE = CYCLE / SEGMENT_DURATION

    var data = fs.readFileSync('/statics/public-b30.mpd');

    let mpd = await r.subrequest(
        '/public-b30.mpd',
    ).then((reply) => {return reply.responseBody})

    let hls = await r.subrequest(
        '/public-b30.m3u8',
    ).then((reply) => {return reply.responseBody})

    let startTimeStr = mpd.match(/ailabilityStartTime=\"([\dT\-:]+)Z\"/)[1]

    // const regex = new RegExp('availabilityStartTime=\"([\d\-T\:Z]+)\"');
    // const startTimeStr = data.match(regex)[0];
    // const startTimeStr = data.match(/ailabilityStartTime=\"([\dT\-:]+)Z\"/)
    const startTime = new Date(startTimeStr);
    const currentTime = new Date(r.args['now']*1000) || new Date();
    const duration = Math.floor((currentTime - startTime) / 1000);
    const n = Math.floor(duration / 30) // $(BLUROUT_CYCLE);
    const slot = Math.floor(duration / SEGMENT_DURATION) % SEGMENTS_ONE_CYCLE

    // replace with n
    // mpd = fs.readFileSync('/statics/public-b30.m3u8');
    // hls = hls.replace('preview-b30.m3u8', `preview-b30.m3u8?n=${n}`);
    hls = hls.replace('preview-b30.m3u8', `preview-b30.m3u8?n=${slot}`);
    return r.return(200, hls);
}


// let now = new Date(r.args['now']*1000) || Math.floor(new Date().getTime() / 1000);
function media(r) {
    const BLUROUT_CYCLE = 30
    const SEGMENT_DURATION = 3
    
    let data = ''

    try {
      data = fs.readFileSync('/statics/preview-b30.m3u8', {'encoding': 'utf-8'});
    } catch (e) {
      return r.return(500, e);
    };

    // collect segments
    var segments = [];
    const regex = /#EXTINF\:[\d\.]+,\npreview-b30-(\d+)\.clear.m4s/g;
    while (true) {
      const match = regex.exec(data);
      if (match == null) {break};
      segments.push(match);
    }
    
    // Slice segments
    const slot = parseInt(r.args['n']);
    var tail = -slot + 4;
    if (slot <= 3) {
        tail = tail - (BLUROUT_CYCLE / SEGMENT_DURATION);
    }
    const head = tail - (BLUROUT_CYCLE / SEGMENT_DURATION);

    if (tail != 0) {
        segments = segments.slice(head, tail);
    }
    else {
        segments = segments.slice(head);
    }

      // calculate media sequence
      var media_sequence = Infinity;
      segments.map((x) => {
        const val = parseInt(x[1]);
        media_sequence = val < media_sequence ? val : media_sequence;
      });
      
      // Construct payload
      const payload = [
      '#EXTM3U',
      '#EXT-X-VERSION:6',
      '#EXT-X-TARGETDURATION:4',
      `#EXT-X-MEDIA-SEQUENCE:${media_sequence}`,
      '#EXT-X-MAP:URI="preview-b30-00000.clear.mp4'
      ]
      segments.map((x) => {
        payload.push(x[0]);
      })
      r.return(200, payload.join('\n'));
}

export default {hello, now, master, media, start};



