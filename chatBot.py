import os
import random
import time
import asyncio
import threading
from telethon.sync import TelegramClient
from colorama import Fore, Back, Style
from telethon import functions, types
from SendReaction import run_SendReaction

threads=[]

async def getClient(phone):
    try:
        print(f'Authenticating phone number: {phone}')
        client = TelegramClient(f'sessions/{phone}', 2392599, '7e14b38d250953c8c1e94fd7b2d63550')
        await client.start()

        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            await client.sign_in(phone, input(f'Phone # ({phone}) Enter the code: '))
        return client
    except Exception as e:
        print(f'Error: {str(e)}')
        return None

async def getMessagesID(client):
    try:
        async for message in client.iter_messages('ViewTestChannel12'):
            print(f'Message from {message.sender_id}: {message.text} : link https://t.me/ViewTestChannel12/{message.id}')
            return message.id,message.text
    except Exception as e:
        print(f'Error while getting messages: {str(e)}')

async def startBot():
    phone = '+923064889750'
    chat_id = 'ViewTestChannel12'
    client = await getClient(phone)
    lastMessage = None
    
    if client is not None:
        print('Bot started.')
        while True:
            msg_id, text = await getMessagesID(client)
            if lastMessage == None or lastMessage != msg_id:
                task = asyncio.create_task(run_SendReaction( chat_id,msg_id))  # Run in the event loop concurrently
                lastMessage = msg_id
            await asyncio.sleep(10)


async def startBot(lowerLimit:int,upperLimit:int)->None:
    phone = '+923064889750'
    chat_id = 'ViewTestChannel12'
    client = await getClient(phone)
    lastMessage = None
    
    if client is not None:
        print('Bot started.')
        while True:
            msg_id, text = await getMessagesID(client)
            if lastMessage == None or lastMessage != msg_id:
                reactionNum = random.randint(lowerLimit, upperLimit)
                await run_SendReaction(chat_id,msg_id,reactionNum)  # Run in the event loop concurrently
                lastMessage = msg_id
            time.sleep(2)
