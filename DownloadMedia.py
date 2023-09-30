from datetime import datetime, timezone
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerEmpty
from tqdm import tqdm


api_id = 21897608       # Your API ID
api_hash = '23f8398210b67a6bcedf9c45aa228b28'  # Your API HASH


def download_media(group, cl, name,date_limit):
    messages = cl.get_messages(group ,limit=2000)
    for message in tqdm(messages):
        # if message.date >= date_limit:
        message_date_aware = message.date.replace(tzinfo=timezone.utc)
        x=message_date_aware.strftime('%Y-%m-%d')
        y=date_limit.strftime('%Y-%m-%d')
        print(f'{x} : {y}')
        if message_date_aware.strftime('%Y-%m-%d') >= date_limit.strftime('%Y-%m-%d'):
            message.download_media('./' + name + '/')


with TelegramClient('name', api_id, api_hash) as client:
    result = client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=500,
        hash=0,
    ))

    

    title = 'soamjenan'         # Title for channel
    channel = client(GetFullChannelRequest(title))

    date_obj = datetime(2023, 7, 27, 0, 0)  # Example datetime object

    download_media(channel.full_chat, client, title, date_obj)