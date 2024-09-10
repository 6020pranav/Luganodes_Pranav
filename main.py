from pymongo import MongoClient
from datetime import datetime
from web3 import Web3
import time
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Environment variables
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
ALCHEMY_API_URL = os.getenv('ALCHEMY_API_URL')
DEPOSIT_ADDRESS = os.getenv('DEPOSIT_ADDRESS')

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
print("1")
db = client[DATABASE_NAME]
print("2")
collection = db[COLLECTION_NAME]
print("3")

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

# Create a Web3 connection
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
