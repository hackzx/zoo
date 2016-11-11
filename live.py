# encoding: UTF-8
import requests
import re
import os,sys
import argparse

parser=argparse.ArgumentParser(prog='WebMap', description='''\
Zoooo
 🐼 🐱 🐅 no 🐠
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
    reg=r'http:\\/\\/pl-hls.*m3u8'
    reg_m3u8=re.compile(reg)
    str=re.search(reg_m3u8, source)
    live=str.group().replace('\\', '')
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

def playlive(live):
    os.system('vlc {0}'.format(live))

if __name__ == '__main__':
    try:
        if args.flag=='douyu':
            print '暂不支持'
            exit()
        if args.flag=='huya':
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
    except:pass
