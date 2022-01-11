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

3. Set Credentials in file `./credentials.env` (file is ignored via .gitignore)

```
TELEGRAM_API_ID=<API_ID>
TELEGRAM_API_HASH=<API_HASH>
TELEGRAM_PHONE=<PHONE_NUMBER>
TELEGRAM_DOWNLOAD_FOLDER=<DOWNLOAD_FOLDER_PATH>
TELEGRAM_CHATS=<CHAT_LIST> # comma separated list of chat names
```

4. Source the file

```
source credentials.env
```

5. Start downloading:

```
python download.py $TELEGRAM_API_ID $TELEGRAM_API_HASH $TELEGRAM_PHONE_NUMBER $TELEGRAM_DOWNLOAD_FOLDER "$TELEGRAM_CHATS"
```

And if you dont want to launch the virtual each time just replace `python` in the previous command by the path where the virtualenv python binary is.
So from the root of the folder's project use `.venv/bin/python`.

You will be prompted to enter the PIN you received in telegram (another device/app) and password (if enabled). After that the download starts.