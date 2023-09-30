import asyncio
from telethon.sync import TelegramClient
from colorama import Fore, Back, Style
import pandas as pd

def main(phone,api,hash):
    GreenColor = Fore.GREEN
    whiteColor=Fore.WHITE
    try:
        print(GreenColor +f'{phone}', end=' ')
        client = TelegramClient(f"sessions/{phone}", api, hash)
        client.connect()
        if not client.is_user_authorized(): 
            client.send_code_request(phone)
            client.sign_in(phone, input    (Style.BRIGHT + Fore.GREEN + 'Enter the code: '))    
        
        print(whiteColor + 'authenticated properly \U0001F44D')  # Thumbs up emoji
    except:
        pass


def authenticatePhones():
    df = pd.read_csv('SessionData.csv')
    
    for index, row in df.iterrows():
        phone=row['Phone']
        api=row['API']
        hash=row['Hash']
        main(phone,api,hash)