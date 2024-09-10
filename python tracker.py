from pymongo import MongoClient
from datetime import datetime
from web3 import Web3
import time
import requests

# MongoDB connection details
MONGO_URI = 'mongodb://localhost:27017/'
DATABASE_NAME = 'luganodes'
COLLECTION_NAME = 'deposits'
TELEGRAM_BOT_TOKEN = '7540784588:AAE-AoEHcVhIvaxoFOD1VvOzgpmGxoX4fWg'
TELEGRAM_CHAT_ID = '-1002364709349'

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Function to store deposit in MongoDB
def store_deposit(transaction, block):
    blockTimestamp = datetime.fromtimestamp(block['timestamp'])
    fee = transaction['gas'] * transaction['gasPrice']
    
    deposit = {
        'blockNumber': block['number'],
        'blockTimestamp': blockTimestamp,
        'fee': fee,
        'hash': transaction['hash'].hex(),
        'pubkey': 'example-public-key'
    }
    collection.insert_one(deposit)
    print('Deposit stored successfully')

# Web3 and Alchemy API details
ALCHEMY_API_URL = 'https://eth-mainnet.g.alchemy.com/v2/45QMzgUgIGsuOKSIQhK5paAd5f98V8gB'
DEPOSIT_ADDRESS = '0xdac17f958d2ee523a2206206994597c13d831ec7'
web3 = Web3(Web3.HTTPProvider(ALCHEMY_API_URL))

if web3.is_connected():
    print("Connected to Ethereum")
else:
    print("Connection failed")

# Function to send a message via Telegram bot
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    print(response.json())

# Function to get the latest block and check transactions
def get_block():
    i = 1
    while True:
        try:
            block = web3.eth.get_block('latest')
            print("New block found", i)
            i += 1
            
            for tx_hash in block.transactions:
                tx = web3.eth.get_transaction(tx_hash)
                if tx.to and tx.to.lower() == DEPOSIT_ADDRESS.lower():
                    store_deposit(tx, block)
                    message = f"New deposit detected! Tx Hash: {tx.hash.hex()}, Amount: {web3.from_wei(tx.value, 'ether')} ETH"
                    print(message)
                    send_telegram_message(message)
            
            time.sleep(10)
        except Exception as e:
            print(f"Error fetching block: {e}")

# Start fetching block details
get_block()
