import json
import random
import time
import aiohttp
import asyncio
import sys
import os
from colorama import Fore, Style
from time import strftime, localtime

sent, errored = 0, 0

with open("config.json") as config:
   data = json.load(config)
   delay = data["delay"]

class Console:
   @staticmethod
   def Logger(content: str, status: bool) -> None:
     green = "[" + Fore.GREEN + Style.BRIGHT + "+" + Style.RESET_ALL + "] "
     red = "[" + Fore.RED + Style.BRIGHT + "-" + Style.RESET_ALL + "] "
     yellow = "[" + Fore.YELLOW + Style.BRIGHT + "!" + Style.RESET_ALL + "] "
     if status == "g":
         sys.stdout.write(f'{green}{content}\n')
     elif status == "r":
         sys.stdout.write(f'{red}{content}\n')
     elif status == "y":
         sys.stdout.write(f'{yellow}{content}\n')

   @staticmethod
   def clear() -> None:
     os.system("cls" if os.name == "nt" else "clear")

async def main(username, message, deviceid):
   global errored, sent
   headers = {
      "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
    }
   async with aiohttp.ClientSession(headers=headers) as session:
     try:
       async with session.post(f"https://ngl.link/api/submit",data={"username": username,"question": message,"deviceId": deviceid}) as resp:
         if resp.status == 200:
           sent += 1
           Console.Logger(f"Sent: {sent} | Errored: {errored}", status="g")
         elif resp.status == 404:
           Console.Logger(f"User {username} does not exist", status="r")
           exit()
         elif resp.status == 429:
           Console.Logger(f"User {username} is rate limited", status="r")
           await asyncio.sleep(10)
         else:
           Console.Logger(f"{await resp.text()} {resp.status}", status="r")
     except Exception as e:
       errored += 1
       print(str(e))
       Console.Logger(f"Error: {e}", status="y")

def deviceid():
   return "".join(random.choice("0123456789abcdefghijklmnopqrstuvwxyz") for i in range(36))

async def Main():
   Console.clear()
   print(Fore.LIGHTRED_EX+ f"""
 __    __   ______   __                 
/  \  /  | /      \ /  | {Fore.GREEN}NGL Spammer {Fore.LIGHTRED_EX}    
$$  \ $$ |/$$$$$$  |$$ |       __    __ 
$$$  \$$ |$$ | _$$/ $$ |      /  \  /  |
$$$$  $$ |$$ |/    |$$ |      $$  \/$$/ 
$$ $$ $$ |$$ |$$$$ |$$ |       $$  $$<  
$$ |$$$$ |$$ \__$$ |$$ |_____  /$$$$  \ 
$$ | $$$ |$$    $$/ $$       |/$$/ $$  |
$$/   $$/  $$$$$$/  $$$$$$$$/ $$/   $$/ 
"""
        + Fore.GREEN
        + "Created by Brainless Dip\n"
        + f"Current delay: {delay}\n"
        + Fore.BLUE
        + "Change the delay from config.json\n"
        + Style.RESET_ALL)
   while True:
    username = input("[~] Enter username: ").strip()
    if username:
       break
    Console.Logger(f"Username cannot be empty. Please enter a valid username", status="y")
   while True:
     try:
       messagecount = int(input("[~] Enter message count: "))
       break
     except ValueError:
       Console.Logger(f"Invalid input. Please enter a valid integer", status="y")
   while True:
    message = input("[~] Enter message: ").strip()
    if message:
       break
    Console.Logger(f"Message cannot be empty", status="y")
   tasks = []
   for x in range(messagecount):
     tasks.append(main(username, message, deviceid()))
     await asyncio.sleep(delay)
   await asyncio.gather(*tasks)
   Console.Logger(f"Sent {sent} messages to {username}", status="g")

if __name__ == "__main__":
   asyncio.run(Main())
