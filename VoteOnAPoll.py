import asyncio
from telethon.sync import TelegramClient
from telethon import functions
from colorama import Fore,Style
import pandas as pd
async def send_PollAnswer(client, phone,chat_id, message_id,option):
    try:
        # await client(functions.messages.SendVoteRequest(
        #     peer=chat_id,
        #     msg_id=message_id,
        #     options=[b'0']
        # ))
        encoded_option = option.encode('utf-8')
        await client(functions.messages.SendVoteRequest(
            peer=chat_id,
            msg_id=message_id,
            options=[encoded_option]
        ))
        print(Fore.GREEN + f"{phone} :",end='' )
        print(Fore.WHITE + f"Vote on the {message_id} on Option {option} ")
    except Exception as e:
        print(Fore.GREEN + f"{phone} :",end='' )
        print(Fore.WHITE + f"Error found" + str(e))

    

async def main(phone,api,hash,chat_id,message_id,option):
    try:
        async with TelegramClient(f'sessions/{phone}', api, hash) as client:
            if not await client.is_user_authorized():
                print(f'{phone} needs to be authenticated by OTP')
                return
            await send_PollAnswer(client, phone,chat_id, message_id,option)
    except Exception as e:
        print(f"Error for {phone}: {str(e)}")

def askOptions():
    options=[]
    while True:
        op = input('Do you want to Continue selction (Y/N) :')
        
        if(op.lower() == 'y'):
            accounts=int(input('Enter the Accounts # :'))
            aOp=int(input('Enter the options for that  :')) - 1
            if(aOp < 0): 
                continue
            options.append({'accounts': accounts,'option': str(aOp)})
        else:
            break
    return options



async def run_VoteOnPoll(chat_id,message_id):
    
    df = pd.read_csv('SessionData.csv')
    options=askOptions()
    starting=0
    
    for x in options:
        for index, row in df.iloc[starting:x['accounts']+starting].iterrows():
            phone=row['Phone']
            api=row['API']
            hash=row['Hash']
            await main(phone,api,hash,chat_id,message_id,x['option'])
        starting=x['accounts']+starting
        

