# mastodon_api.py
import requests

class MastodonClient:
    def __init__(self, api_token, api_url, hashtag):
        self.api_token = api_token
        self.api_url = api_url
        self.hashtag = hashtag

    def post_to_mastodon(self, content):
        requests.post(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_token}"},
            data={"status": content}
        )

    def fetch_and_respond_to_mastodon_requests(self, model):
        response = requests.get(
            f"{self.api_url}/timeline/tag/{self.hashtag.strip('#')}?limit=5",
            headers={"Authorization": f"Bearer {self.api_token}"}
        )
        for status in response.json():
            content = status['content']
            if "predict" in content.lower():
                try:
                    input_data = np.array(eval(content.split("predict:")[1].strip()))
                    prediction = input_data @ model
                    self.post_to_mastodon(f"Prediction: {prediction.tolist()}")
                except Exception as e:
                    self.post_to_mastodon(f"Error processing request: {str(e)}")
