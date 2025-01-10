# mastodon_api.py
import requests
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO)

class MastodonClient:
    def __init__(self):
        self.api_token = os.getenv("MASTODON_API_KEY")
        self.instance_url = os.getenv("MASTODON_INSTANCE_URL")
        self.hashtag = os.getenv("NUTRIAL_TAG")

    def post_status(self, status_text):
        url = f"{self.instance_url}/api/v1/statuses"
        payload = {'status': status_text}
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logging.info(f"Posted to Mastodon: {status_text}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error posting status: {e}")
            return None

    def fetch_and_respond_to_mastodon_requests(self, model):
        base_url = f"{self.instance_url}/api/v1"

        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Accept': 'application/json'
        }

        params = {
            'type': 'statuses',
            'tag': self.hashtag,
            'limit': 30
        }

        response = requests.get(f"{base_url}/timelines/tag/{self.hashtag}",
                                headers=headers,
                                params=params)

        if response.status_code == 200:
            data = response.json()
            logging.info(f"Found {len(data)} latest statuses")
            statuses = data
            messages = []
            for status in statuses:
                content = status['content']
                messages.append(content)
            return messages
        else:
            logging.error(f"Error: {response.status_code}")
            return None

    def answerUserFeedback(self):
        feedback = 10
        return feedback
