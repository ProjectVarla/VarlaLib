import requests
from conf import settings
from Models.Cores import NotificationMessage


class Notify:
    @staticmethod
    def push(message: NotificationMessage):
        try:
            response = requests.post(
                f"{settings.NOTIFICATION_CORE_URL}/push", json=message.dict(), timeout=3
            )
            return response.json()
        except:
            print("Welp 🤷, Notification Core can't be reached!")
