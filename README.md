# Ethereum Deposit Tracker with MongoDB and Telegram Alerts

This project is a Python application that monitors the Ethereum blockchain for deposits made to a specific address, stores transaction details in MongoDB, and sends real-time alerts to a Telegram channel. It leverages Web3 for Ethereum interaction, MongoDB for data storage, and the Telegram API for notifications.


## Technologies Used

- **Python**: Core programming language used to implement the logic.
- **Web3.py**: A Python library for interacting with Ethereum.
- **MongoDB**: Stores transaction and block data for tracking and analysis.
- **Telegram Bot API**: Sends notifications to a specified Telegram group/chat when a deposit is made.

## Prerequisites

To run this project, ensure you have the following set up:

- Python 3.x
- MongoDB (running locally or remotely)
- An Ethereum node provider (like [Alchemy](https://www.alchemy.com/)) to interact with the Ethereum blockchain.
- A Telegram bot with its token and a chat ID where alerts will be sent.

## Setup and Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/eth-deposit-tracker.git
    cd eth-deposit-tracker
    ```

2. **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Update the configuration:**

    In the main Python file, update the following variables with your own values:
    - `MONGO_URI`: MongoDB connection string.
    - `DATABASE_NAME` and `COLLECTION_NAME`: Name of your MongoDB database and collection.
    - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
    - `TELEGRAM_CHAT_ID`: The chat ID of the group/channel where notifications will be sent.
    - `ALCHEMY_API_URL`: The URL of your Ethereum node provider.
    - `DEPOSIT_ADDRESS`: The Ethereum address you want to monitor for incoming deposits.

4. **Run the program:**

    ```bash
    python main.py
    ```

## How It Works

- **Blockchain Monitoring**: The script connects to the Ethereum blockchain using Web3. It continuously listens for new blocks and checks all transactions within those blocks.
- **Deposit Detection**: When it identifies a transaction sent to the specified `DEPOSIT_ADDRESS`, it calculates the gas fee and stores relevant details (block number, timestamp, transaction hash, etc.) in MongoDB.
- **Telegram Notification**: Once a deposit is detected, a message containing transaction details is sent to your Telegram chat.

## Example Telegram Message

When a deposit is detected, you'll receive a message similar to this:

```
New deposit detected! 
Tx Hash: 0x12345abcd..., 
Amount: 1.5 ETH
```

## Customization

You can easily modify the script to suit your needs. For example:
- **Tracking multiple addresses**: Expand the `DEPOSIT_ADDRESS` logic to monitor multiple addresses.
- **Adding more transaction details**: Customize the MongoDB deposit data to include more or fewer fields as needed.

## Troubleshooting

- **Connection Issues**: If the script fails to connect to Ethereum, ensure your Alchemy (or other provider) URL is correct and your node is active.
- **Telegram Messages Not Sending**: Verify that your bot has permission to post in the target chat. Ensure the `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are correct.

