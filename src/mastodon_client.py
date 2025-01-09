# mastodon_api.py
import requests
import numpy as np

class MastodonClient:
    def __init__(self, api_token, instance_url, hashtag):
        self.api_token = api_token
        self.instance_url = instance_url
        self.hashtag = hashtag

    def post_to_mastodon(self, content):
        requests.post(
            self.instance_url,
            headers={"Authorization": f"Bearer {self.api_token}"},
            data={"status": content}
        )

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
            print(f"Found {len(data)} latest statuses")
            statuses = data
            for status in statuses:
                content = status['content']
                if "predict" in content.lower():
                    try:
                        input_data = np.array(eval(content.split("predict:")[1].strip()))
                        prediction = input_data @ model
                        self.post_to_mastodon(f"Prediction: {prediction.tolist()}")
                    except Exception as e:
                        self.post_to_mastodon(f"Error processing request: {str(e)}")
        else:
            print(f"Error: {response.status_code}")
            return None
