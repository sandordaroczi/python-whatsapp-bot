import json
from dotenv import load_dotenv
import os
import requests
import aiohttp
import asyncio

class WhatsAppMessenger:
    def __init__(self):
        load_dotenv()
        self.ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
        self.RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
        self.PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
        self.VERSION = os.getenv("VERSION")
        
    def send_whatsapp_template_message(self):
        url = f"https://graph.facebook.com/{self.VERSION}/{self.PHONE_NUMBER_ID}/messages"
        headers = {
            "Authorization": "Bearer " + self.ACCESS_TOKEN,
            "Content-Type": "application/json",
        }
        data = {
            "messaging_product": "whatsapp",
            "to": self.RECIPIENT_WAID,
            "type": "template",
            "template": {"name": "hello_world", "language": {"code": "en_US"}},
        }
        response = requests.post(url, headers=headers, json=data)
        return response
    
    def send_whatsapp_text_message(self, text):
        data = self._get_text_message_input(self.RECIPIENT_WAID, text)
        response = self._send_message(data)
        return response
    
    async def send_whatsapp_text_message_async(self, text):
        data = self._get_text_message_input(self.RECIPIENT_WAID, text)
        await self._send_message_async(data)
    
    def _get_text_message_input(self, recipient, text):
        return json.dumps(
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient,
                "type": "text",
                "text": {"preview_url": False, "body": text},
            }
        )

    def _send_message(self, data):
        headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {self.ACCESS_TOKEN}",
        }
        url = f"https://graph.facebook.com/{self.VERSION}/{self.PHONE_NUMBER_ID}/messages"
        response = requests.post(url, data=data, headers=headers)
        return response

    async def _send_message_async(self, data):
        headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {self.ACCESS_TOKEN}",
        }
        url = f"https://graph.facebook.com/{self.VERSION}/{self.PHONE_NUMBER_ID}/messages"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, data=data, headers=headers) as response:
                    if response.status == 200:
                        print("Status:", response.status)
                        print("Content-type:", response.headers["content-type"])
                        html = await response.text()
                        print("Body:", html)
                    else:
                        print(response.status)
                        print(response)
            except aiohttp.ClientConnectorError as e:
                print("Connection Error", str(e))

# Example usage:
whatsapp_messenger = WhatsAppMessenger()
whatsapp_messenger.send_whatsapp_template_message()
whatsapp_messenger.send_whatsapp_text_message("Hello, this is a test message.")