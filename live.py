# encoding: UTF-8
import requests
import re
import os,sys

def usage():
    print 'usage: {0} 10027'.format(sys.argv[0])
    exit()

def viewsource(url):
    r=requests.Session().get(url)
    source=r.text
    return source
    
def getlive(source):
    reg=r'http:\\/\\/pl-hls.*m3u8'
    reg_m3u8=re.compile(reg)
    str=re.search(reg_m3u8, source)
    live=str.group().replace('\\', '')
    return live

def playlive(live):
    os.system('vlc {0}'.format(live))

if len(sys.argv) < 2:
    usage()
try:
    source=viewsource('http://room.api.m.panda.tv/index.php?method=room.shareapi&roomid={0}'.format(sys.argv[1]))
    live=getlive(source)
    playlive(live)
except:pass
