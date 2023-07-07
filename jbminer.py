import random
import requests
from termcolor import colored
import threading
import time
import discord
from discord_webhook import DiscordWebhook

def generate_wallet():
    # Generate a random private key
    private_key = ''.join(random.choice('0123456789abcdef') for _ in range(64))
    
    # Calculate the corresponding Bitcoin address (public key)
    public_key = private_key_to_public_key(private_key)
    bitcoin_address = public_key_to_bitcoin_address(public_key)
    
    return private_key, bitcoin_address

def private_key_to_public_key(private_key):
    # Here, you should use the appropriate algorithms and libraries to calculate a public key
    # This is a simplified version and not a real implementation
    return private_key

def public_key_to_bitcoin_address(public_key):
    # Here, you should use the appropriate algorithms and libraries to calculate a Bitcoin address
    # This is a simplified version and not a real implementation
    return public_key

def check_balance(bitcoin_address):
    # Make an API call to check the balance of the Bitcoin address
    api_url = f"https://api.blockcypher.com/v1/btc/main/addrs/{bitcoin_address}/balance"
    response = requests.get(api_url)
    data = response.json()
    balance = data.get('balance', 0)
    
    return balance

def send_discord_message(webhook_url, content):
    webhook = DiscordWebhook(url=webhook_url, content=content)
    webhook.execute()

def generate_and_check(webhook_url=None):
    # Generate a new wallet
    private_key, bitcoin_address = generate_wallet()
    balance = check_balance(bitcoin_address)

    # Prepare the message and adjust the text color
    if balance > 0:
        message = f"Found a Bitcoin wallet with balance!\n\n"
        message += colored(f"Private Key: {private_key}\n", 'green')
        message += colored(f"Bitcoin Address: {bitcoin_address}\n", 'green')
        message += colored(f"Balance: {balance} BTC\n", 'green')
        
        # Check if Discord webhook usage is desired
        if webhook_url:
            send_discord_message(webhook_url, message)
    else:
        message = f"Found a Bitcoin wallet without balance.\n\n"
        message += colored(f"Private Key: {private_key}\n", 'red')
        message += colored(f"Bitcoin Address: {bitcoin_address}\n", 'red')
        message += colored(f"Balance: {balance} BTC\n", 'red')

    print(message)

def main():
    print(colored('''
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
  \_/  \___(_)___(_)___/''', 'red'))

    use_webhook = input("Do you want to use a webhook? (yes/no): ")
    if use_webhook.lower() == 'yes':
        webhook_url = input("Enter the Discord webhook URL: ")
    else:
        webhook_url = None
    
    wallets_per_second = int(input("How many BTC wallets do you want to generate and check per second? "))
    
    threads = []
    while True:
        for _ in range(wallets_per_second):
            thread = threading.Thread(target=generate_and_check, args=(webhook_url,))
            thread.start()
            threads.append(thread)
        time.sleep(1)
        for thread in threads:
            thread.join()
        threads.clear()

if __name__ == "__main__":
    main()
