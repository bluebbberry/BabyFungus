# federated_learning.py
import numpy as np
import time
from rdf_knowledge_graph import RDFKnowledgeGraph
from mastodon_client import MastodonClient
import os
from dotenv import load_dotenv, dotenv_values
# loading variables from .env file
load_dotenv()

class FederatedLearning:
    def __init__(self, model_size=3, learning_rate=0.01):
        self.model = np.random.rand(model_size)
        self.local_gradients = np.zeros_like(self.model)
        self.learning_rate = learning_rate
        self.rdf_kg = RDFKnowledgeGraph(fuseki_server="http://localhost:3030/ds/update", fuseki_query="http://localhost:3030/ds/query")
        self.mastodon_api = MastodonClient(api_token=os.getenv("MASTODON_API_TOKEN"), instance_url=os.getenv("MASTODON_INSTANCE_URL"), hashtag="#" + os.getenv("NUTRIAL_TAG"))

    def train(self):
        while True:
            data = np.random.rand(10, 3)
            labels = (data.sum(axis=1) > 1.5).astype(int)
            predictions = data @ self.model
            gradients = data.T @ (predictions - labels)
            self.local_gradients = gradients
            self.rdf_kg.share_gradients(gradients)
            aggregated_gradients = self.rdf_kg.aggregate_gradients()
            self.local_gradients += sum(aggregated_gradients)
            self.model -= self.learning_rate * self.local_gradients
            self.rdf_kg.save_to_knowledge_graph(self.model)
            self.mastodon_api.post_to_mastodon(f"Model updated: {self.model.tolist()}")
            time.sleep(60)
