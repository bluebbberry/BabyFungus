# federated_learning.py
import numpy as np
import logging
import time
from rdf_knowledge_graph import RDFKnowledgeGraph
from mastodon_client import MastodonClient
import os

logging.basicConfig(level=logging.INFO)

class FederatedLearning:
    def __init__(self, model_size=3, learning_rate=0.01):
        self.model = np.random.rand(model_size)
        self.local_gradients = np.zeros_like(self.model)
        self.learning_rate = learning_rate
        self.rdf_kg = RDFKnowledgeGraph(fuseki_server=os.getenv("FUSEKI_SERVER_UPDATE_URL"), fuseki_query=os.getenv("FUSEKI_SERVER_QUERY_URL"))
        self.mastodon_api = MastodonClient()

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
            self.mastodon_api.post_status(f"Model updated: {self.model.tolist()}")
            logging.info(f"Model updated: {self.model}")
            logging.info(f"Gradients calculated: {gradients}")
            time.sleep(60)
