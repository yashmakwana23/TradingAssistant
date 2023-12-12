import requests
from datetime import datetime
import json

def dcMessage(message,channelid):
    # Define your Discord bot token and channel ID
    with open('E_tokens\othertokne.json', 'r') as file:
        token_data = json.load(file)
    Discord = token_data.get("Discord")
    BOT_TOKEN = Discord
    CHANNEL_ID = channelid  # Replace with your channel ID

    # Define the URL to send a message to a channel
    url = f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages'

    # Define the headers (including the Authorization header with the bot token)
    headers = {
        'Authorization': f'Bot {BOT_TOKEN}',
        'Content-Type': 'application/json'
    }

    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Define the payload (the message you want to send)
    payload = {
        'content': f'{current_datetime}: **{message}**'
    }

    # Send the message
    response = requests.post(url, headers=headers, json=payload)

    # Check the response
    if response.status_code == 200:
        pass
        # print('Message sent successfully!')
    else:
        print(f'Error sending message. Status code: {response.status_code}')

def PosdcMessage(message,channelid):
    with open('E_tokens\othertokne.json', 'r') as file:
        token_data = json.load(file)
    Discord = token_data.get("Discord")
    BOT_TOKEN = Discord
    CHANNEL_ID = channelid  # Replace with your channel ID

    # Define the URL to send a message to a channel
    url = f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages'

    # Define the headers (including the Authorization header with the bot token)
    headers = {
        'Authorization': f'Bot {BOT_TOKEN}',
        'Content-Type': 'application/json'
    }

    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Define the payload (the message you want to send)
    payload = {
        'content': f'**{current_datetime}:** \n{message}'
    }

    # Send the message
    response = requests.post(url, headers=headers, json=payload)

    # Check the response
    if response.status_code == 200:
        pass
        # print('Message sent successfully!')
    else:
        print(f'Error sending message. Status code: {response.status_code}')