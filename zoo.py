#!/usr/bin/env python
# encoding: UTF-8
import requests
import re
# import sys
import argparse
import json
import base64
import subprocess

parser = argparse.ArgumentParser(prog='Zoo', description='''\
Zoooo
🐼 🐱 🐯 🐠 🚩
''', epilog='方便快捷！')
parser.add_argument('flag', help='douyu/panda/huomao/zhanqi/huya')
parser.add_argument('id', help='room\'s id')
parser.add_argument('-q', '--quality', help='选择视频质量: high/middle/low', default='high')
parser.add_argument('-p', '--player', help='指定播放器: mpv/vlc/iina', default='iina')
args = parser.parse_args()


def playlive(live):
    player = args.player
    print 'live:\n{0}\n'.format(live)
    # os.system('mpv \'{0}\''.format(live))
    try:
        # command_run = subprocess.call([player, live])
        subprocess.call([player, live])
    except Exception as e:
        print '找不到' + player + '，请指定播放器或安装mpv/vlc/iina。'
        raise e


def viewsource(url):
    r = requests.Session().get(url)
    source = r.text
    return source


def getlive_panda(source):
    # reg=r'http:\\/\\/pl-hls.*m3u8'
    # reg_m3u8=re.compile(reg)
    # str=re.search(reg_m3u8, source)
    # live=str.group().replace('\\', '')
    # 被废弃的捉急的正则匹配法
    data = json.loads(source)
    try:
        live = data['data']['videoinfo']['address']
        if args.quality == 'high':
            live = live.replace('_small.m3u8', '.m3u8')
        if args.quality == 'middle':
            live = live.replace('_small.m3u8', '_mid.m3u8')
        if args.quality == 'low':
            live = live.replace('.m3u8', '_small.m3u8')
    except:
        print 'can not found this room!'
        exit()
    return live


def getlive_huomao(source):
    # 另一个获取地址：http://www.huomao.com/outplayer/htmlfive/{0}.html
    reg = r'value=".*"'
    reg_m3u8 = re.compile(reg)
    str = re.search(reg_m3u8, source)
    if str.group() == 'value=""':
        print 'can not found this room!'
        exit()
    if args.quality == 'high':
        quality = ''
        # quality = '_720phd'
    if args.quality == 'middle':
        quality = '_720'
    if args.quality == 'low':
        quality = '_480'
    live = 'http://live-ws-hls.huomaotv.cn/live/' + str.group().replace('"', '').replace('value', '').replace('=', '') + quality + '/playlist.m3u8'
    return live


def getlive_zhanqi(source):
    # http://m.zhanqi.tv/api/static/v2.1/room/domain/{0}.json
    # 解析base64后可查看访客ip
    data = json.loads(source)
    try:
        live_encode = data['data']['flashvars']['VideoLevels']
        live_decode = base64.b64decode(live_encode)
        data = json.loads(live_decode)
        live = data['streamUrl']
    except:
        print 'can not found this room!'
        exit()
    return live


def getlive_douyu(source):
    data = json.loads(source)
    try:
        roomId = data['data']['room_id']
        url = 'http://m.douyu.com/html5/live?roomId={0}'.format(roomId)
        r = requests.Session().get(url)
        content = json.loads(r.text)
        live = content['data']['hls_url']
    except Exception as e:
        raise e
    return live


def getlive_huya(source):
    """
    在 <script> 中匹配 hyPlayerConfig，sStreamName 为直播id，奶奶的腿不会匹配
    拼接 live = sFlvUrl/sHlsUrl + sStreamName + '.m3u8'
    形如 http://ws.streamhls.huya.com/huyalive/90327-2665499004-11448231049700573184-1000255798-10057-A-0-1_[QUALITY].m3u8
    其中 [QUALITY] 为码率，取值 500 - 10000
    """
    try:
        hlsUrl = re.search(r'sHlsUrl":"[^,]*', source).group().replace('sHlsUrl', '').replace('":"', '').replace('\\', '').replace('"', '')
        sStreamName = re.search(r'sStreamName":"[^,]*', source).group().replace('sStreamName', '').replace('"', '').replace('\\', '').replace(':', '')
        live = hlsUrl + '/' + sStreamName + '.m3u8'

        if args.quality == 'high':
            live = live.replace('.m3u8', '_10000.m3u8')
        if args.quality == 'middle':
            live = live.replace('.m3u8', '_1200.m3u8')
        if args.quality == 'low':
            live = live.replace('.m3u8', '_800.m3u8')

    except Exception as e:
        raise e
    return live


if __name__ == '__main__':
    try:
        if args.flag == 'douyu':
            source = viewsource('http://open.douyucdn.cn/api/RoomApi/room/{0}'.format(args.id))
            live = getlive_douyu(source)
            playlive(live)
        if args.flag == 'huya':
            source = viewsource('http://www.huya.com/{0}'.format(args.id))
            live = getlive_huya(source)
            playlive(live)
        if args.flag == 'panda':
            source = viewsource('http://room.api.m.panda.tv/index.php?method=room.shareapi&roomid={0}'.format(args.id))
            live = getlive_panda(source)
            playlive(live)
        if args.flag == 'huomao':
            source = viewsource('http://m.huomao.com/mobile/mob_live/{0}'.format(args.id))
            live = getlive_huomao(source)
            playlive(live)
        if args.flag == 'zhanqi':
            source = viewsource('http://m.zhanqi.tv/api/static/v2.1/room/domain/{0}.json'.format(args.id))
            live = getlive_zhanqi(source)
            playlive(live)
    except:
        pass
