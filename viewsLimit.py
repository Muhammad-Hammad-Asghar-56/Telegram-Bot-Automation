import asyncio
import sys
import requests
from time import sleep
from configparser import ConfigParser
from os import system, name
from threading import Thread, active_count
from re import search, compile

THREADS = 500
PROXIES_TYPES = ('http', 'socks4', 'socks5')
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
REGEX = compile(r"(?:^|\D)?(("+ r"(?:[1-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"):" + (r"(?:\d|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{3}"
                + r"|65[0-4]\d{2}|655[0-2]\d|6553[0-5])")
                + r")(?:\D|$)")

errors = open('errors.txt', 'a+')
cfg = ConfigParser(interpolation=None)
cfg.read("config.ini", encoding="utf-8")
THREADSARR=[]

http, socks4, socks5 = '', '', ''
try: http, socks4, socks5 = cfg["HTTP"], cfg["SOCKS4"], cfg["SOCKS5"]
except KeyError: print(' [ OUTPUT ] Error | config.ini not found!');sleep(3);exit()

http_proxies, socks4_proxies, socks5_proxies = [], [], []
proxy_errors, token_errors = 0, 0
channel, post, time_out, real_views = '', 0, 15, 0
target_views=0

PROXY_URL = "http://tzgpwcyp-rotate:4vz5xwlk449c@p.webshare.io:80/"



def scrap(sources, _proxy_type):
    for source in sources:
        if source:
            try:
                response = requests.get(source, timeout=time_out, proxies={"http": PROXY_URL, "https": PROXY_URL})
            except Exception as e:
                errors.write(f'{e}\n')
            if tuple(REGEX.finditer(response.text)):
                for proxy in tuple(REGEX.finditer(response.text)):
                    if _proxy_type == 'http':
                        http_proxies.append(proxy.group(1))
                    elif _proxy_type == 'socks4':
                        socks4_proxies.append(proxy.group(1))
                    elif _proxy_type == 'socks5':
                        socks5_proxies.append(proxy.group(1))


def start_scrap():
    global THREADSARR
    localthreads=[]
    for i in (http_proxies, socks4_proxies, socks5_proxies): i.clear()
    for i in ((http.get("Sources").splitlines(), 'http'), (socks4.get("Sources").splitlines(), 'socks4'), (socks5.get("Sources").splitlines(), 'socks5')):
        thread = Thread(target=scrap, args=(i[0], i[1]))
        THREADSARR.append(thread)
        localthreads.append(thread)
        thread.start()
    for t in localthreads: t.join()


def get_token(proxy, proxy_type):
    try:
        session = requests.session()
        response = session.get(f'https://t.me/{channel}/{post}', params={'embed': '1', 'mode': 'tme'},
                    headers={'referer': f'https://t.me/{channel}/{post}', 'user-agent': USER_AGENT},
                    proxies={'http': f'{proxy_type}://{proxy}', 'https': f'{proxy_type}://{proxy}'},
                    timeout=time_out)
        return search('data-view="([^"]+)', response.text).group(1), session
    except AttributeError: return 2
    except requests.exceptions.RequestException: 1
    except Exception as e: return errors.write(f'{e}\n')


def send_view(token, session, proxy, proxy_type):
    try:
        cookies_dict = session.cookies.get_dict()
        response = session.get('https://t.me/v/', params={'views': str(token)}, cookies={
            'stel_dt': '-240', 'stel_web_auth': 'https%3A%2F%2Fweb.telegram.org%2Fz%2F',
            'stel_ssid': cookies_dict.get('stel_ssid', None), 'stel_on': cookies_dict.get('stel_on', None)},
                            headers={'referer': f'https://t.me/{channel}/{post}?embed=1&mode=tme',
                                'user-agent': USER_AGENT, 'x-requested-with': 'XMLHttpRequest'},
                            proxies={'http': f'{proxy_type}://{proxy}', 'https': f'{proxy_type}://{proxy}'},
                            timeout=time_out)
        return True if (response.status_code == 200 and response.text == 'true') else False
    except requests.exceptions.RequestException: 1
    except Exception: pass


def control(proxy, proxy_type):
    global proxy_errors, token_errors
    token_data = get_token(proxy, proxy_type)
    if token_data == 2: token_errors += 1
    elif token_data == 1: proxy_errors += 1
    elif token_data:
        send_data = send_view(token_data[0], token_data[1], proxy, proxy_type)
        if send_data == 1: proxy_errors += 1


def start_view():
    global THREADSARR
    localThreads=[]
    c = 0
    start_scrap()
    for i in [http_proxies, socks4_proxies, socks5_proxies]:
        for j in i:
            thread = Thread(target=control, args=(j, PROXIES_TYPES[c]))
            THREADSARR.append(thread)
            localThreads.append(thread)
            while active_count() > THREADS: sleep(0.05)
            thread.start()
        c += 1
        sleep(2)
    for t in localThreads:
        t.join()
        start_view()


# Add a new global variable for the target views

def exit_program():
    print('Exiting the program...')
    sys.exit(0)
import subprocess



def close_cmd(): #  CLose all the generated Threads
    for thread in THREADSARR[::-1]:
        if(thread.is_alive()):
            print("One THREAD Stopped forcefully......")
            thread.terminate()


    
def check_views():
    global real_views
    while True:
        try:
            telegram_request = requests.get(f'https://t.me/{channel}/{post}', params={'embed': '1', 'mode': 'tme'},
                                headers={'referer': f'https://t.me/{channel}/{post}', 'user-agent': USER_AGENT})
            real_views = search('<span class="tgme_widget_message_views">([^<]+)', telegram_request.text).group(1)
            sleep(2)
            
            # Check if the target views are reached
            if int(real_views.replace(',', '')) >= target_views:
                print(f'Target views ({target_views}) reached. Exiting program...')
                close_cmd()# Exit the program gracefully when target views are reached
        except: 
            pass

# ... (Rest of the code remains the same)



logo = '''
    Telegram Auto Views Paid Tool 
     @venomshade  +918708604830
'''


def tui():
    while True:
        print(logo)
        print(f'''
  [ Data ]: {channel.capitalize()}/{post}
  [ Live Views ]: {real_views}
 
  [ Connection Errors ]: {proxy_errors}
  [ Token Errors ]: {token_errors}
 
  [ Threads ]: {active_count()}
        ''')
        sleep(2);system('cls' if name == 'nt' else 'clear')



async def view_main(channelName:str,msgId:int,target:int):
    global target_views
    global channel,post
    target_views =target
    post=msgId
    channel=channelName

    try:
        search('<span class="tgme_widget_message_views">([^<]+)', requests.get(f'https://t.me/{channel}/{post}',
        params={'embed': '1', 'mode': 'tme'}, headers={'referer': f'https://t.me/{channel}/{post}', 'user-agent': USER_AGENT}).text).group(1)
    except: print(' [ OUTPUT ] Error | Channel Or Post Not Found!');sleep(3);exit()
    else:
        print(' [ OUTPUT ] Stated | Wait few seconds to run threads')
        task1 = Thread(target=start_view)
        task2 = Thread(target=check_views)
        THREADSARR.append(task1)
        THREADSARR.append(task2)
        task1.start()
        task2.start()
        sleep(7.5);system('cls' if name == 'nt' else 'clear')
        task3=Thread(target=tui)
        THREADSARR.append(task3)
        task3.start()


asyncio.run(view_main('ViewTestChannel12',48,3000))