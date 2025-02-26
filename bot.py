import logging
import asyncio

from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import time
import configparser
import os
import sys

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

def banner():
    print(f"""{re}╔╦╗┌─┐┌─┐┌─┐┌─┐┌─┐┬ ┬┬┌─┐┌─┐┬─┐┬┌─┐┌─┐┌┬┐┌─┐┬  ┌┬┐┌─┐┌─┐┌─┐┬┌─┐
  ║║├┤ │  ├┤ ├┤ │ │├┬┘├┴┐├┤ ├┬┘│├┤ │  │││├┤ │  │││├┤ │  ├┤ │├┤ 
  ╩ └─┘└─┘└─┘└─┘└─┘┴└─┴ ┴└─┘┴└─┴└─┘└─┘┴ ┴└─┘┴  ┴ ┴└─┘┴  └─┘┴└─┘ """)

# This is the name of the file where the config is stored.
config_file = 'config.data'
# This is the name of the section in the config file that contains the details.
config_section = 'cred'

# This function reads the config file and gets the details.
def read_config():
    parser = configparser.ConfigParser()
    parser.read(config_file)
    return parser.items(config_section)

# This function writes the config file with the details.
def write_config(api_id, api_hash):
    parser = configparser.ConfigParser()
    parser.add_section(config_section)
    parser.set(config_section, 'api_id', api_id)
    parser.set(config_section, 'api_hash', api_hash)
    with open(config_file, 'w') as configfile:
        parser.write(configfile)


# This function checks if the config file exists. If it does, it reads the details from the file.
def check_config():
    if os.path.isfile(config_file):
        return read_config()
    else:
        api_id = input(f"{cy}[+] Enter your API ID: {re}")
        api_hash = input(f"{cy}[+] Enter your API Hash: {re}")
        write_config(api_id, api_hash)
        return api_id, api_hash

# This is the main function. It runs the program.
async def main():
    # This is the banner that is displayed at the beginning of the program.
    banner()

    # This is the section of the code that gets the API ID and API Hash from the user.
    api_id, api_hash = check_config()

    # This is the section of the code that creates the client.
    client = TelegramClient('Anup', api_id, api_hash)

    # This is the section of the code that logs in the client.
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(client.phone)
        client.sign_in(client.phone, input(f"{cy}[+] Enter the code: {re}"))

    # This is the section of the code that logs a message to the console.
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger.info('Telethon client started.')

    # This is the section of the code that runs the bot.
    try:
        print(f"{gr}[+] Bot is running... Manage forwarding via Telegram commands!")
        await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await client.disconnect()

    # This is the section of the code that logs a message to the console.
    logger.info('Telethon client disconnected.')

# This is the section of the code that runs the main function.
if __name__ == '__main__':
    asyncio.run(main())