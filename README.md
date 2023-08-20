# IP-change detector Telegram bot

This is a simple Telegram bot that sends a message to a Telegram chat when the IP address of the host changes.

## Installation

1. Clone this repository

2. Prepare virtual environment with Pipenv

```bash
pipenv install
```

3. Create a Telegram bot and get the API token

    - Go to Telegram and search for the "BotFather".
    - Start a chat with BotFather and follow the steps to create a new bot.
    - After the bot is created, BotFather will give you a token which looks something like this: `221312654:ABHdqTcvDH1vGWJxgSeofSAs1K5PALDsaw+`


4. Get the chat ID

    - Start a chat with your bot.
    - Go to the following URL: `https://api.telegram.org/bot<yourtoken>/getUpdates`
    - Look for the "chat" object:
    ```json
    "chat": {
        "id": -123456789,
        "title": "My Chat",
        "type": "group",
        "all_members_are_administrators": true
    }
    ```
    - The `id` field is your chat ID.

5. Use the token in the `main.py` script:

```bash
python3 main.py --token <your-token> --chat-id <your-chat-id> --period <seconds> --logpath <log-file>
```

6. Make the script executable:

```bash
chmod +x /path/to/your/script.py
```

7. Add the script to the crontab:

```bash
crontab -e
```

Add the following line to the crontab:

```bash
* * * * * /path/to/python /path/to/ip-change-detector-telegram-bot/main.py --token <your-token> --chat-id <your-chat-id> --working-dir /path/to/ip-change-detector-telegram-bot/work
```

### Optional: enable Crontab logging for debugging

You can enable logging for cron jobs in order to track problems. 

First, create your log file in `/var/log`:
```bash
cd /var/log
sudo mkdir mylogs
sudo chmod 750 mylogs
sudo chown -R marcofavorito:marcofavorito mylogs
```

Append the following to the cron command:
```
... >> /var/log/mylogs/ip-change-detector-telegram-bot-log 2>&1
```

Then restart the service:
```bash
sudo service cron restart
```

You can then view the logs with:
```bash
sudo tail -f /var/log/mylogs/ip-change-detector-telegram-bot-log
```
