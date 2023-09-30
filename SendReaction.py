# import asyncio
# from telethon.sync import TelegramClient
# from telethon import functions, types
# from telethon.tl.functions.messages import SendReactionRequest
# from telethon.tl.functions.messages import GetMessagesViewsRequest,SendReactionRequest
# from telethon import utils
# from telethon.tl.functions.channels import JoinChannelRequest
# import random
# import pandas as pd

# async def send_reaction(client, chat_id, message_id):
#     try:
#         result =  await client(SendReactionRequest(
#                         peer=chat_id,
#                         msg_id=message_id,
#                         big=True,
#                         add_to_recent=True,
#                         reaction=[types.ReactionEmoji(
#                             emoticon= '👍'
#                         )]
#                     ))
#         await client(GetMessagesViewsRequest(
#                 peer=chat_id,
#                 id=[message_id],
#                 increment=True
#             ))
#         print(f"Seen and React on the {message_id} message 💯")
#     except Exception as e:
#         print("Error sending reaction:", str(e))


# async def run_SendReaction( chat_id,msg_id):
#     df = pd.read_csv('SessionData.csv')
    
#     for index, row in df.iterrows():
#         phone=row['Phone']
#         api=row['API']
#         hash=row['Hash']
#         await main(phone,api,hash ,msg_id, chat_id)


# async def main(phone,apiID,hash, msg_id, chat_id):
#     try:
#         async with TelegramClient(f'sessions/{phone}', apiID, hash) as client:
#             if not await client.is_user_authorized():
#                 print(f'{phone} needs to be authenticated by OTP')
#                 return
#             chat_id = chat_id
#             message_id = msg_id

#             await send_reaction(client, chat_id, message_id)


#     except Exception as e:
#         print(f"Error for {phone}: {str(e)}")


import asyncio
from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.functions.messages import GetMessagesViewsRequest,SendReactionRequest
from telethon import utils
from telethon.tl.functions.channels import JoinChannelRequest
import random
import pandas as pd

async def send_reaction(client, chat_id, message_id):
    try:
        reactions = ['👍', '👌', '❤️', '😍', '🔥', '👏', '😁', '🤯', '😱', '🎉', '🤩', '🙏', '💯', '🏆', '😇', '🤗']
        random_reaction = random.choice(reactions)
        result =  await client(SendReactionRequest(
                        peer=chat_id,
                        msg_id=message_id,
                        big=True,
                        add_to_recent=True,
                        reaction=[types.ReactionEmoji(
                            emoticon= random_reaction
                        )]
                    ))
        await client(GetMessagesViewsRequest(
                peer=chat_id,
                id=[message_id],
                increment=True
            ))
        print(f"Seen and React on the {message_id} message 💯")
    except Exception as e:
        print("Error sending reaction:", str(e))


async def run_SendReaction( chat_id,msg_id):
    df = pd.read_csv('phone.csv')
    apiDf=pd.read_csv('Api.csv')

    for index, row in df.iterrows():
        num_rows = len(df)
        random_index = random.randint(0, num_rows - 1)

        selected_row = df.iloc[random_index]
        corresponding_api_row = apiDf.iloc[random_index]
        api = corresponding_api_row['API']
        hash_value = corresponding_api_row['Hash']
        phone=row['Phone']
        await main(phone,api,hash_value ,msg_id, chat_id)


async def main(phone,apiID,hash, msg_id, chat_id):
    try:
        async with TelegramClient(f'sessions/{phone}', apiID, hash) as client:
            if not await client.is_user_authorized():
                print(f'{phone} needs to be authenticated by OTP')
                return
            chat_id = chat_id
            message_id = msg_id

            await send_reaction(client, chat_id, message_id)


    except Exception as e:
        print(f"Error for {phone}: {str(e)}")