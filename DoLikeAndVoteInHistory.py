import asyncio
from telethon.sync import TelegramClient
from telethon.tl import functions, types
from SendReaction import run_SendReaction
from views import view_main

timeLap = 120
view_main_task = None

async def sendReactionTask(channel, msgId):
    global view_main_task

    view_main_task = asyncio.create_task(run_SendReaction(channel, msgId))

    await asyncio.sleep(timeLap)

    if view_main_task:
        view_main_task.cancel()
        try:
            await view_main_task
        except asyncio.CancelledError:
            print(f"Send_Main_Task on {msgId} was canceled")

async def viewTask(channel, msgId):
    global view_main_task

    view_main_task = asyncio.create_task(view_main(channel, msgId))

    # Sleep for the specified time
    await asyncio.sleep(timeLap)

    # Cancel the view_main task
    if view_main_task:
        view_main_task.cancel()
        try:
            await view_main_task
        except asyncio.CancelledError:
            print(f"view_main_task on {msgId} was canceled")

async def reverseMessages(channel, phone, api, hash, limit):
    async with TelegramClient(f'sessions/{phone}', api, hash) as client:
        async for message in client.iter_messages(channel, reverse=False, limit=limit):
            print(f"{message.id} : {message.text} --- Detected")

            # Do Likes
            await sendReactionTask(channel,message.id)
            # Inc. Views
            # await viewTask(channel, message.id)

async def main():
    phone = '+923064889750'
    channelId = "ViewTestChannel12"
    msgLimit=5
    await reverseMessages(channelId, phone, 21578909, 'bc7aa963f8f7979344c9ad4aa10d09b5', msgLimit)

if __name__ == '__main__':
    asyncio.run(main())
