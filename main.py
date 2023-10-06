import asyncio
from SendReaction import run_SendReaction
from AuthenticatePhones import authenticatePhones
import sys
from colorama import Fore
import os
from VoteOnAPoll import run_VoteOnPoll
import time
from chatBot import startBot
def mainMenu():
    header = "MH-Telegram Bot Automation"
    header_color = Fore.YELLOW
    GreenColor = Fore.GREEN
    whiteColor=Fore.WHITE
    redColor=Fore.RED

    header_length = len(header) + 8  # Additional 8 characters for the box

    print(redColor + "+" + "-" * header_length + "+")
    print("|" + " " * ((header_length - len(header)) // 2)+header_color + header + " " * ((header_length - len(header)) // 2) +redColor + "|")
    print(redColor+ "+" + "-" * header_length + "+")

    print(whiteColor + 'Option 1', end='')
    print(GreenColor + ' : Authenticate the Numbers')
    print(whiteColor + 'Option 2', end='')
    print(GreenColor + ' : Send Reaction on Single Message')
    print(whiteColor + 'Option 3', end='')
    print(GreenColor + ' : View Reactions on Single Message')
    print(whiteColor + 'Option 4', end='')
    print(GreenColor + ' : Send Vote on the poll')
    print(whiteColor + 'Option 5', end='')
    print(GreenColor + ' : Start the bot')
    print(whiteColor + 'Option ', end='')
    print(GreenColor + ' : Start the bot')
    print(whiteColor + 'Option 6', end='')
    print(GreenColor + ' : Exit')
    print(header_color + "+" + "-" * header_length + "+")
    option =int(input(whiteColor + 'Enter the option: '))
    return  option if option in range(1,6) else 0


def AskChatIDMsgID():
    GreenColor = Fore.GREEN
    
    chat_Id=input(GreenColor + 'Enter Chat Id :')
    msg_id=input(GreenColor + 'Enter Message Id :')
    
    return chat_Id,msg_id

def printChatHeader():
    header = "Chat-Bot Wroking ........"
    header_color = Fore.YELLOW
    GreenColor = Fore.GREEN
    whiteColor=Fore.WHITE

    header_length = len(header) + 8  # Additional 8 characters for the box

    print(GreenColor+ header_color + "+" + "-" * header_length + "+")
    print("|" + " " * ((header_length - len(header)) // 2) + header + " " * ((header_length - len(header)) // 2) + "|")
    print(GreenColor+ header_color + "+" + "-" * header_length + "+")



if __name__ == '__main__':
    while True:
        os.system('cls')
        try:
            option = mainMenu()
            if option == 0:
                sys.exit()
            elif option==1:
                authenticatePhones()
                pass
            elif option==2:
                chat_Id,msg_Id=AskChatIDMsgID()
                asyncio.run(run_SendReaction(chat_Id,int(msg_Id)))
                pass
            elif option==3:
                # chat_Id,msg_Id=AskChatIDMsgID()
                print(Fore.RED+' Comming Soon Not Available Now',end='')
                print(Fore.WHITE+' ')
                time.sleep(5)
                pass
            elif option==4:
                print()
                try:
                    chat_Id = input('Enter the Chat ID :')
                    message_ID=int(input("Enter message Id :"))
                    asyncio.run(run_VoteOnPoll(chat_Id,message_ID))
                except:
                    print('👾 Error exist on try again ....')
            elif option==5:
                os.system('cls')
                inputStr=input("Enter Target Reaction limit (format : Min-Max)")
                lowerLimit, upperLimit = int(inputStr.split('-')[0]),int(inputStr.split('-')[1])
                asyncio.run(startBot(lowerLimit,upperLimit))
                pass
        except Exception as e:
            print(Fore.RED + f"Error found" + str(e))
            time.sleep(5)
