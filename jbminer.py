from pystyle import Anime, Write, Colorate, Colors, Box, Center
from time import sleep
from multiprocessing import Process, Value, freeze_support, Lock
import requests
import json
import urllib3
from mnemonic import Mnemonic
import bip32utils
import random

def HitWebhook(bal, wallet, WIF, words, webhook_url):
    try:
        data = {
            "content": None,
            "embeds": [
                {
                    "title": "JBWallet",
                    "description": f"HIT! | WIF: {str(WIF)} | Bal: {bal} | Address: {str(wallet)} | Seed: {str(words)}",
                    "color": 6749952,
                    "author": {"name": "Miner Started!"}
                }
            ],
            "username": "JBWallet",
            "avatar_url": "https://cdn.discordapp.com/attachments/1062796452885188670/1068636566605537330/image.png",
            "attachments": []
        }
        headers = {'Content-type': 'application/json'}
        response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    except:
        return None

def btcMiner(fails, lock, hits, webhook_url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    while True:
        mnemonic = Mnemonic("english")
        words = mnemonic.generate(strength=256)
        seed = mnemonic.to_seed(words)

        key = bip32utils.BIP32Key.fromEntropy(seed)
        address = key.Address()
        WIF = key.WalletImportFormat()

        # Check Balance
        response = requests.get(f"https://api-r.bitcoinchain.com/v1/address/{address}")
        lol = response.text

        if "balance" in lol:
            try:
                ls = json.loads(lol)
                for balance in ls:
                    bal = balance["balance"]
                    if bal > 0:
                        try:
                            hits.value += 1
                        except:
                            continue
                        f = open("hits.txt", "a")
                        data = f'New Hit! | balance: {bal} | Wallet: {address} | WIF: {WIF} | Phrase: {words}'
                        f.write(str(data) + "\n")
                        f.close()
                        print(Colorate.Color(Colors.green, data))
                        try:
                            if webhook_url:
                                HitWebhook(bal, address, WIF, words, webhook_url)
                        except:
                            print("Webhook Error!")
                            continue
                        input("")
                    else:
                        print(Colorate.Color(Colors.red, f"[+] {address} > 0.00 BTC ($0.00)"))
                        fails.value += 1
                else:
                    print(Colorate.Color(Colors.red, f"[+] {address} > 0.00 BTC ($0.00)"))
                    fails.value += 1
            except:
                print("Blocked...")
        else:
            print(Colorate.Color(Colors.red, f"[+] {address} > 0.00 BTC ($0.00)"))
            fails.value += 1

if __name__ == '__main__':
    freeze_support()

    def header():
        print(Center.XCenter(Colorate.Vertical(Colors.purple_to_red, """
   ____________  ____                 
  |_  | ___ \  \/  (_)                
    | | |_/ / .  . |_ _ __   ___ _ __ 
    | | ___ \ |\/| | | '_ \ / _ \ '__|
/\__/ / |_/ / |  | | | | | |  __/ |   
\____/\____/\_|  |_/_|_| |_|\___|_|   
                                      
        __   _____  __  
       /  | |  _  |/  | 
__   __`| | | |/' |`| | 
\ \ / / | | |  /| | | | 
 \ V / _| |_\ |_/ /_| |_
  \_/  \___(_)___(_)___/
        """)))

    def menu():
        header()

        use_webhook = input("Do you want to use a webhook? (yes/no): ")
        if use_webhook.lower() == "yes":
            webhook_url = input("Enter the Discord webhook URL: ")
        else:
            webhook_url = None

        wallets_per_second = int(input("How many BTC wallets do you want to generate and check per second? "))

        print(Colorate.Horizontal(Colors.green_to_white, "Starting Threads..."))

        fails = Value('i', 0)
        hits = Value('i', 0)
        lock = Lock()

        try:
            for _ in range(wallets_per_second):
                thread = Process(target=btcMiner, args=(fails, lock, hits, webhook_url))
                thread.start()
        except Exception as e:
            print(e)

    menu()
