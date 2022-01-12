# Telegram Media Downloader

Python script to sync media (gifs, videos and photos) in a Telegram chat with a local folder (one-way download).

## How to

1. Register new api id and hash at [https://my.telegram.org](https://my.telegram.org)

2. Make a virtualenv and install all the needed package

```
pip3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

3. Set credentials in file `./config.toml` (file is ignored via .gitignore)

```
[APP]
telegram_api_id = <api_id>
telegram_api_hash = <api_hash>
telegram_phone = <phone_number>
telegram_download_folder = <download_folder_path>
telegram_chats = [<chat_name>] # list of chat names
```

4. Start downloading:

```
usage: download.py [-h] [--config CONFIG] [--telegram_api_id APP.TELEGRAM_API_ID] [--telegram_api_hash APP.TELEGRAM_API_HASH] [--telegram_phone_number APP.TELEGRAM_PHONE_NUMBER]
                   [--telegram_download_folder APP.TELEGRAM_DOWNLOAD_FOLDER] [--telegram_chats APP.TELEGRAM_CHATS [APP.TELEGRAM_CHATS ...]]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Path of the configuration file (default: config.toml)
  --telegram_api_id APP.TELEGRAM_API_ID
                        The Telegram api id of your application (default: )
  --telegram_api_hash APP.TELEGRAM_API_HASH
                        The Telegram api hash of your application (default: )
  --telegram_phone_number APP.TELEGRAM_PHONE_NUMBER
                        The Telegram phone number used for connect to your account. A password will be asked (default: )
  --telegram_download_folder APP.TELEGRAM_DOWNLOAD_FOLDER
                        The download folder where documents will be downloaded (default: )
  --telegram_chats APP.TELEGRAM_CHATS [APP.TELEGRAM_CHATS ...]
                        The list of chat names from where to download documents (default: )
```

And if you dont want to launch the virtual each time just replace `python` in the previous command by the path where the virtualenv python binary is.
So from the root of the folder's project use `.venv/bin/python`.

You will be prompted to enter the PIN you received in telegram (another device/app) and password (if enabled). After that the download starts.