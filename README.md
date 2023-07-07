BTC Wallet Miner

This repository contains a Python script that generates and checks Bitcoin (BTC) wallets for balances. It utilizes the BlockCypher API to check the balance of the generated wallets.

Prerequisites:

Before running the script, ensure that you have the following prerequisites installed:

- Python 3.x: The script is written in Python and requires Python 3.x to be installed on your system.

Installation:

1. Clone the repository:
   `git clone https://github.com/coder026jb/btc-wallet-miner.git`

2. Navigate to the project directory:
   `cd btc-wallet-miner`

3. Install the required dependencies by running the following command:
  `pip install -r requirements.txt`
   This will install the necessary modules (requests, termcolor, discord, discord_webhook) required by the script.

Usage:

1. Open a command-line interface (CLI) or terminal.

2. Navigate to the project directory:
   `cd btc-wallet-miner`

3. Run the script using the following command:
   `python jbminer.py`

4. The script will prompt you with a series of questions:
   - Do you want to use a webhook? (yes/no): If you want to receive notifications via Discord webhook, enter "yes" and provide the Discord webhook URL when prompted. Otherwise, enter "no".
   - How many BTC wallets do you want to generate and check per second?: Enter the number of wallets you want to generate and check per second.

5. Sit back and let the script generate and check the BTC wallets. The script will display the results in the console and, if a webhook URL is provided, it will send notifications to the specified Discord channel.

Contributing:

Contributions to this repository are welcome. If you encounter any issues or have suggestions for improvements, please create a new issue or submit a pull request.

License:

This project is licensed under the MIT License.

