#!/usr/bin/env python
import argparse
import glob
import json
import logging
import os
import sys
from argparse import ArgumentDefaultsHelpFormatter

from colored import attr, bg, fg
from telethon import TelegramClient, sync

from utils import Config, Status, contains_key, get_id

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    '--config', default="config.toml", help="Path of the configuration file"
)
parser.add_argument(
    "--telegram_api_id", dest="app.telegram_api_id", default="",
    help="The Telegram api id of your application"
)
parser.add_argument(
    "--telegram_api_hash", dest="app.telegram_api_hash", default="",
    help="The Telegram api hash of your application"
    )
parser.add_argument(
    "--telegram_phone_number", dest="app.telegram_phone_number", default="",
    help="The Telegram phone number used for connect to your account. A password will be asked"
)
parser.add_argument(
    "--telegram_download_folder", dest="app.telegram_download_folder", default="",
    help="The download folder where documents will be downloaded"
)
parser.add_argument(
    "--telegram_chats", nargs="+", dest="app.telegram_chats", default="",
    help="The list of chat names from where to download documents"
)
parser.add_argument(
    "--telegram_channels", nargs="+", dest="app.telegram_channels", default="",
    help="The list of channel names from where to download documents"
)

args = parser.parse_args()
config = Config(vars(args))

client = TelegramClient('session_name', config.app.telegram_api_id, config.app.telegram_api_hash)
client.start(config.app.telegram_phone_number)

dialogs = client.get_dialogs()

status = Status()


def dl_file(msg, path, retry=False):

    if retry:
        print('{}BETTER QUALITY FOUND..{}'.format(fg('yellow'), attr('reset')), end=' ')
        status.redl += 1
        paths = glob.glob(path+'*')
        for _path in paths:
            os.remove(_path)
    msg.download_media(file=path)
    if retry:
        print('{}REDOWNLOADED{}'.format(fg('green'), attr('reset')))
    else:
        print('{}OK{}'.format(fg('green'), attr('reset')))
        status.dls += 1

def dl():

    chats = []
    chats.extend(config.app.telegram_chats)
    chats.extend(config.app.telegram_channels)

    for chat in chats:
        chat = get_id(client, chat)
        for msg in client.iter_messages(chat, None):
            if msg.gif:
                gif_id = str(msg.gif.id)
                path = config.app.telegram_download_folder + '/' + gif_id
                print('Download gif {}...'.format(gif_id), end=' ')
                gif_paths = glob.glob(path+'*')
                status.total += 1
                if not gif_paths:
                    dl_file(msg, path)
                else:
                    dl_size = os.stat(gif_paths[0]).st_size
                    try:
                        size = msg.gif.size
                    except AttributeError:
                        print('{}CHECK ERROR{}'.format(fg('red'), attr('reset')))
                        status.error += 1
                        continue
                    if dl_size < size:
                        dl_file(msg, path, retry=True)
                    else:
                        print('{}OK. NOTHING TO DO{}'.format(fg('green'), attr('reset')))
                status.gif += 1
            elif msg.video:
                video_id = str(msg.video.id)
                path = config.app.telegram_download_folder + '/' + video_id
                print('Download video {}...'.format(video_id), end=' ')
                video_paths = glob.glob(path+'*')
                status.total += 1
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
                status.video += 1
            elif msg.photo:
                photo_id = str(msg.photo.id)
                path = config.app.telegram_download_folder + '/' + photo_id
                print('Download image {}...'.format(photo_id), end=' ')
                photo_paths = glob.glob(path+'*')
                status.total += 1
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
                        status.error += 1
                        continue
                    if dl_size < size:
                        dl_file(msg, path, retry=True)
                    else:
                        print('{}OK. NOTHING TO DO{}'.format(fg('green'), attr('reset')))
                status.photo += 1
    print(status)

dl()
