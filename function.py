import pandas as pd
from telethon.sync import TelegramClient
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetMessagesViewsRequest,GetHistoryRequest,SendReactionRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputPeerChannel
import pandas as pd
phones=[]




async def getMessage(client, chat_id):
    try:
        messages = await client(GetHistoryRequest(
            peer=chat_id,
            limit=100,  # Adjust the number of messages to retrieve
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        return messages.messages
    except Exception as e:
        print(f'Error while getting messages: {str(e)}')
        return []
    

    
async def sendReaction(client):
    # Get the entity of the channel
    channel_username = 'ViewTestChannel12'
    
    input_peer = InputPeerChannel('1909605348','1548603126711280704')
    
    await client(SendReactionRequest(
        peer=input_peer,
        msg_id=9,
        reaction=client.get_input_entity('❤️')
    ))


async def ViewMessages(client):
    channelName = 'ViewTestChannel12'  # Enter te channel name
    msg_ids = [9]  # enter the Msg ID here
    try:
        for msgId in msg_ids:
            client(GetMessagesViewsRequest(
                peer=channelName,
                id=msgId,
                increment=True
            ))
            print('Vieweds')
    except:
        return
    """"""

async def AddIntoGroup(client):
    channelName = 'ViewTestChannel12'  # Enter the channel name
    await client(JoinChannelRequest(channelName))


async def getInfo(client):
    me = await client.get_me()
    print(me.stringify())
    username = me.username
    print(username)
    print(me.phone)

async def GetChannelInfo(client, channel_username):
    try:
        entity = await client.get_entity(channel_username)
        print(entity)
        return entity
    except Exception as e:
        print(f"Error getting channel info: {e}")
        return None

# async def sendReaction(client):
#     try:
#         # Get the entity of the channel
#         channel_username = 'ViewTestChannel12'
#         entity = await client.get_entity(channel_username)
        
#         # Create an input peer for the channel
#         input_peer = InputPeerChannel(entity.id, entity.access_hash)
        
#         # Specify the correct message ID for the reaction
#         msg_id = 9  # Replace with the correct message ID
        
#         # Call the coroutine and await the result
#         reaction_entity = await client.get_input_entity('❤️')
        
#         # Send the reaction
#         await client(SendReactionRequest(
#             peer=input_peer,
#             msg_id=msg_id,
#             reaction=reaction_entity
#         ))
#         print('Reaction sent successfully')
#     except Exception as e:
#         print(f"Error sending reaction: {e}")



#                           Check the ChannelID & access Hash
# with TelegramClient(f'+92 306 4889750', 2392599, '7e14b38d250953c8c1e94fd7b2d63550') as client:
#     client.loop.run_until_complete(GetChannelInfo(client,'ViewTestChannel12'))

df = pd.read_csv('SessionData.csv')

# for phone in phones:

for index,row in df.iloc[1:].iterrows():
    phone=row['Phone']
    api=row['API']
    hash=row['Hash']
    print(f"{phone} : {api} : {hash}")
    with TelegramClient(f'sessions/{phone}', api, hash) as client:
        client.start()
        if not client.is_user_authorized():
            print(f'{phone} needs to be authenticated by OTP')
            # client.send_code_request(phone)
            # client.sign_in(phone, input('Enter the code: '))
            continue
        client.loop.run_until_complete(sendReaction(client))





