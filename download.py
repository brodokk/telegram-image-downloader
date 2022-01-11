#!/usr/bin/env python
import glob
import json
import logging
import os
import sys

from colored import attr, bg, fg
from telethon import TelegramClient, sync

api_id = sys.argv[1]
api_hash = sys.argv[2]
phone = sys.argv[3]
download_folder = sys.argv[4]
chats = sys.argv[5]

chats = chats.split(',')

client = TelegramClient('session_name', api_id, api_hash)
client.start(phone)

dialogs = client.get_dialogs()

error = 0
redl = 0
dls = 0
total = 0
gif = 0
video = 0
photo = 0

def dl_file(msg, path, retry=False):
    global error
    global redl
    global dls
    global total

    if retry:
        print('{}BETTER QUALITY FOUND..{}'.format(fg('yellow'), attr('reset')), end=' ')
        redl += 1
        paths = glob.glob(path+'*')
        for _path in paths:
            os.remove(_path)
    msg.download_media(file=path)
    if retry:
        print('{}REDOWNLOADED{}'.format(fg('green'), attr('reset')))
    else:
        print('{}OK{}'.format(fg('green'), attr('reset')))
        dls += 1

def dl():
    global error
    global redl
    global dls
    global total
    global gif
    global video
    global photo


    for chat in chats:
        for msg in client.iter_messages(chat, None):
            if msg.gif:
                gif_id = str(msg.gif.id)
                path = download_folder + '/' + gif_id
                print('Download video {}...'.format(gif_id), end=' ')
                gif_paths = glob.glob(path+'*')
                total += 1
                if not gif_paths:
                    dl_file(msg, path)
                else:
                    dl_size = os.stat(gif_paths[0]).st_size
                    try:
                        size = msg.gif.size
                    except AttributeError:
                        print('{}CHECK ERROR{}'.format(fg('red'), attr('reset')))
                        error += 1
                        continue
                    if dl_size < size:
                        dl_file(msg, path, retry=True)
                    else:
                        print('{}OK. NOTHING TO DO{}'.format(fg('green'), attr('reset')))
                gif += 1
            elif msg.video:
                video_id = str(msg.video.id)
                path = download_folder + '/' + video_id
                print('Download video {}...'.format(video_id), end=' ')
                video_paths = glob.glob(path+'*')
                total += 1
                if not video_paths:
                    dl_file(msg, path)
                else:
                    dl_size = os.stat(video_paths[0]).st_size
                    try:
                        size = msg.video.size
                    except AttributeError:
                        print('{}CHECK ERROR{}'.format(fg('red'), attr('reset')))
                        error += 1
                        continue
                    if dl_size < size:
                        dl_file(msg, path, retry=True)
                    else:
                        print('{}OK. NOTHING TO DO{}'.format(fg('green'), attr('reset')))
                video += 1
            elif msg.photo:
                photo_id = str(msg.photo.id)
                path = download_folder + '/' + photo_id
                print('Download image {}...'.format(photo_id), end=' ')
                photo_paths = glob.glob(path+'*')
                total += 1
                if not photo_paths:
                    dl_file(msg, path)
                else:
                    dl_size = os.stat(photo_paths[0]).st_size
                    try:
                        if 'sizes' in msg.photo.__dict__:
                            if 'sizes' in msg.photo.sizes[-1].__dict__:
                                size = msg.photo.sizes[-1].sizes[-1]
                            else:
                                size = msg.photo.sizes[-1].size
                        else:
                            print('no')
                            size = msg.photo.size
                    except AttributeError as e:
                        print('{}CHECK ERROR{}'.format(fg('red'), attr('reset')))
                        error += 1
                        continue
                    if dl_size < size:
                        dl_file(msg, path, retry=True)
                    else:
                        print('{}OK. NOTHING TO DO{}'.format(fg('green'), attr('reset')))
                photo += 1
    print('GIF: {}; VIDEO; {}; PHOTO: {}'.format(gif, video, photo))
    print('DL: {}; REDL: {}; ERROR: {}; TOTAL: {}'.format(dls, redl, error, total))

dl()
