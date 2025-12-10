import requests
import uuid
from django.conf import settings
from django.urls import reverse

class ChapaService:
    BASE_URL = "https://api.chapa.co/v1"

    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

    def initialize_payment(self, email, amount, first_name, last_name, tx_ref, return_url):
        """
        Initializes a payment request with Chapa.
        Returns the checkout URL if successful.
        """
        url = f"{self.BASE_URL}/transaction/initialize"
        
        payload = {
            "email": email,
            "amount": str(amount),
            "currency": "ETB",
            "first_name": first_name,
            "last_name": last_name,
            "tx_ref": tx_ref,
            # We will build the webhook logic in the next step
            # "callback_url": "https://your-domain.com/api/webhook/chapa/", 
            "return_url": return_url,
            "customization[title]": "SaaS Subscription",
            "customization[description]": "Payment for plan subscription"
        }

        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status() # Raise error if status is 4xx or 5xx
            data = response.json()
            
            if data['status'] == 'success':
                return data['data']['checkout_url']
            else:
                raise Exception(f"Chapa Error: {data['message']}")
                
        except requests.exceptions.RequestException as e:
            print(f"Payment Initialization Failed: {e}")
            return None

    @staticmethod
    def generate_tx_ref():
        """Generates a unique transaction reference"""
        return f"tx-{uuid.uuid4().hex[:12]}"