# main.py
import threading
from federated_learning import FederatedLearning
from mastodon_client import MastodonClient

def start_training():
    federated_learning = FederatedLearning()
    federated_learning.train()

def start_mastodon_interaction():
    mastodon_api = MastodonClient()
    mastodon_api.post_status("Ready for requests.")
    mastodon_api.fetch_and_respond_to_mastodon_requests(model=None)  # Provide the model here if needed

if __name__ == "__main__":
    threading.Thread(target=start_training).start()
    threading.Thread(target=start_mastodon_interaction).start()
    print("Baby Fungus instance started and collaborating...")
