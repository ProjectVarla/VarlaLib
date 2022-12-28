from os import getenv

import requests
from dotenv import load_dotenv
from Models.Cores import NotificationMessage

load_dotenv()

HOST = getenv("NOTIFICATION_CORE_URL")


class Notify:
    @staticmethod
    def push(message: NotificationMessage):
        try:
            response = requests.post(f"{HOST}/push", json=message.dict(), timeout=3)
            return response.json()
        except:
            print("Welp 🤷, Notification Core can't be reached!")
