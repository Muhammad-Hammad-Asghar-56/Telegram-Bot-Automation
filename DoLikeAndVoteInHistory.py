# import asyncio
# from telethon.sync import TelegramClient
# from telethon.tl import functions, types
# from SendReaction import run_SendReaction
# from views import view_main
# timeLap = 300
# async def viewTask(channel,msgId):
#     # task=None
#     # async def close_after_timeout():
#     #     global timeLap
#     #     await asyncio.sleep(timeLap)  
#     #     task.cancel()  # Cancel the main task
    
#     # main_task = asyncio.ensure_future(view_main(channel,msgId))  # Start the main task

#     # loop = asyncio.get_event_loop()
#     # timeout_task = loop.create_task(close_after_timeout())  # Schedule the timeout task

#     # try:
#     #     loop.run_until_complete(main_task)
#     # except asyncio.CancelledError:
#     #     pass
#     # finally:
#     #     loop.stop()


#     global timeLap
#     view_main_task = view_main(channel,msgId)
#     await asyncio.sleep(timeLap)
#      # Cancel the view_main task
#     if view_main_task:
#         view_main_task.cancel()
#         try:
#             await view_main_task
#         except asyncio.CancelledError:
#             print("not working")
#             pass
    
# async def reverseMessages(channel:str,phone: str ,api:int ,hash:str,limit:int):
#     async with TelegramClient(f'sessions/{phone}', api, hash) as client:
#         async for message in client.iter_messages(channel, reverse=False,limit = limit):
#             print(f"{message.id} : {message.text} --- Detected")
#             #  Do Likes
            
#             #  Inc. Views
#             viewTask(channel,message.id)


# async def main():
#     phone = '+923064889750'
#     channelId="ViewTestChannel12"
#     timeLap = 300
#     await reverseMessages(channelId,phone,21578909,'bc7aa963f8f7979344c9ad4aa10d09b5',5)

# if __name__ == '__main__':
#     asyncio.run(main())




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
