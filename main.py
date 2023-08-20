#!/usr/bin/env python3

import argparse
import datetime
import logging
import time
from pathlib import Path
from tempfile import TemporaryDirectory

import requests




def configure_logger(path: str):
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(str(path)), logging.StreamHandler()],
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Check public IP address and send notification through Telegram bot if it has changed"
    )
    parser.add_argument(
        "--token", type=str, required=True, help="Your Telegram bot token"
    )
    parser.add_argument(
        "--chat-id", type=int, required=True, help="Your Telegram chat id"
    )
    parser.add_argument(
        "--working-dir", type=str, default="work", help="Path to working directory"
    )
    return parser.parse_args()


# Endpoint for sending messages through the bot
TELEGRAM_SEND_MESSAGE_URL = "https://api.telegram.org/bot{TOKEN}/sendMessage"


# Check public IP address
def get_public_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    return response.json()["ip"]


def send_telegram_notification(message, token, chat_id):
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    response = requests.post(
        TELEGRAM_SEND_MESSAGE_URL.format(TOKEN=token), data=payload
    )
    response.raise_for_status()
    return response.json()


def main(token: str, chat_id: str, working_dir: Path):
    logfile = working_dir / "ip_checker.log"
    last_datetime_notified_file = working_dir / "last_datetime_notified.txt"
    old_ip_file = working_dir / "old_ip_file.txt"
    if not working_dir.exists():
        working_dir.mkdir()
        last_datetime_notified_file.touch()
        old_ip_file.touch()

    configure_logger(logfile)

    logging.info("*" * 125)
    logging.info("Starting IP address checker...")
    logging.info(f"Telegram bot token: {token}")
    logging.info(f"Telegram chat id: {chat_id}")
    logging.info(f"Working dir: {working_dir}")

    # Read last notified datetime
    last_datetime_notified_content = last_datetime_notified_file.read_text()
    if last_datetime_notified_content:
        last_datetime_notified = datetime.datetime.strptime(last_datetime_notified_content, "%Y-%m-%d %H:%M:%S.%f")
    else:
        last_datetime_notified = datetime.datetime.now()

    # Read old IP address
    old_ip_content = old_ip_file.read_text()
    if old_ip_content:
        old_ip = old_ip_content
    else:
        old_ip = None

    try:
        logging.info("Checking IP address...")
        current_ip = get_public_ip()
        logging.info(f"Current IP address: {current_ip}")

        if current_ip != old_ip:
            message = f"IP address has changed to: {current_ip}"
            logging.info(message)
            send_telegram_notification(message, token, chat_id)
            last_datetime_notified_file.write_text(str(last_datetime_notified))
            old_ip_file.write_text(current_ip)
        else:
            logging.info("IP address has not changed.")
            # Send notification every hour, even if IP address has not changed
            if (datetime.datetime.now() - last_datetime_notified).seconds > 3600:
                message = (
                    f"IP address is {old_ip} and has not changed since {last_datetime_notified}"
                )
                logging.info(message)
                send_telegram_notification(message, token, chat_id)
                last_datetime_notified_file.write_text(str(datetime.datetime.now()))

        old_ip = current_ip
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    args = parse_args()
    token = args.token
    chat_id = args.chat_id
    working_dir = Path(args.working_dir).resolve()

    main(token, chat_id, working_dir)
