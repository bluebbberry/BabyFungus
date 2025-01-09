# main.py
import threading
from src.federated_learning import FederatedLearning
from src.mastodon_client import MastodonClient

def start_training():
    federated_learning = FederatedLearning()
    federated_learning.train()

def start_mastodon_interaction():
    mastodon_api = MastodonClient(api_token="your_mastodon_api_token", api_url="https://mastodon.social/api/v1/statuses", hashtag="#babyfungus")
    mastodon_api.fetch_and_respond_to_mastodon_requests(model=None)  # Provide the model here if needed

if __name__ == "__main__":
    threading.Thread(target=start_training).start()
    threading.Thread(target=start_mastodon_interaction).start()
    print("Baby Fungus instance started and collaborating...")
