# encoding: UTF-8
import requests
import re
import os,sys
import argparse
import json
import base64

parser=argparse.ArgumentParser(prog='WebMap', description='''\
Zoooo
🐼 🐱 🐯 🐠 🚩
''', epilog='方便快捷！')
parser.add_argument('flag', help='douyu/panda/huomao/zhanqi/huya')
parser.add_argument('id', help='room\'s id')
parser.add_argument('-q', '--quality', help='选择视频质量: high/middle/low', default='middle')
args=parser.parse_args()

def viewsource(url):
    r=requests.Session().get(url)
    source=r.text
    return source
    
def getlive_panda(source):
    # reg=r'http:\\/\\/pl-hls.*m3u8'
    # reg_m3u8=re.compile(reg)
    # str=re.search(reg_m3u8, source)
    # live=str.group().replace('\\', '')
    # 被废弃的捉急的正则匹配法
    data=json.loads(source)
    try:
        live=data['data']['videoinfo']['address']
    except:
        print 'can not found this room!'
        exit()
    print live
    return live

def getlive_huomao(source):
    reg=r'value=".*"'
    reg_m3u8=re.compile(reg)
    str=re.search(reg_m3u8, source)
    if str.group()=='value=""':
        print 'can not found this room!'
        exit()
    if args.quality=='high':
        quality=''
    if args.quality=='middle':
        quality='_720'
    if args.quality=='low':
        quality='_480'
    live='http://live-ws-hls.huomaotv.cn/live/' + str.group().replace('"','').replace('value','').replace('=', '') + quality + '/playlist.m3u8'
    print live
    return live

def getlive_zhanqi(source):
    # http://m.zhanqi.tv/api/static/v2.1/room/domain/{0}.json
    # 解析base64后可查看访客ip
    data=json.loads(source)
    try:
        live_encode=data['data']['flashvars']['VideoLevels']
        live_decode=base64.b64decode(live_encode)
        data=json.loads(live_decode)
        live=data['streamUrl']
    except:
        print 'can not found this room!'
        exit()
    print live
    return live

def playlive(live):
    os.system('vlc {0}'.format(live))

if __name__ == '__main__':
    try:
        if args.flag=='douyu':
            # m3u8系動態地址，尚未找到規律
            print '暂不支持'
            exit()
        if args.flag=='huya':
            # blob協議，不知如何播放
            print '暂不支持'
            exit()
        if args.flag=='panda':        
            source=viewsource('http://room.api.m.panda.tv/index.php?method=room.shareapi&roomid={0}'.format(args.id))
            live=getlive_panda(source)
            playlive(live)
        if args.flag=='huomao':
            source=viewsource('http://m.huomao.com/mobile/mob_live/{0}'.format(args.id))
            live=getlive_huomao(source)
            playlive(live)
        if args.flag=='zhanqi':
            source=viewsource('http://m.zhanqi.tv/api/static/v2.1/room/domain/{0}.json'.format(args.id))
            live=getlive_zhanqi(source)
            playlive(live)
    except:pass
