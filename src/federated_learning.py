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

    def train(self, model, updates):
        logging.info("Initializing training with provided model and updates.")
        self.model = np.array(model)
        self.local_gradients = sum([np.array(update) for update in updates])
        logging.info(f"Model initialized: {self.model}")
        logging.info(f"Initial gradients from updates: {self.local_gradients}")

        while True:
            logging.info("Generating new batch of data for training.")
            data = np.random.rand(10, 3)
            labels = (data.sum(axis=1) > 1.5).astype(int)
            predictions = data @ self.model
            logging.info(f"Predictions: {predictions}")
            gradients = data.T @ (predictions - labels)
            logging.info(f"Calculated gradients: {gradients}")
            self.local_gradients = gradients

            logging.info("Sharing gradients with the knowledge graph.")
            self.rdf_kg.share_gradients(gradients)

            logging.info("Fetching aggregated gradients from the knowledge graph.")
            aggregated_gradients = self.rdf_kg.aggregate_gradients()
            logging.info(f"Aggregated gradients received: {aggregated_gradients}")

            self.local_gradients += sum(aggregated_gradients)
            logging.info(f"Updated local gradients: {self.local_gradients}")

            self.model -= self.learning_rate * self.local_gradients
            logging.info(f"Updated model weights: {self.model}")

            logging.info("Saving the updated model to the knowledge graph.")
            self.rdf_kg.save_to_knowledge_graph(self.model)

            logging.info("Posting model update to Mastodon.")
            self.mastodon_api.post_status(f"Model updated: {self.model.tolist()}")

            time.sleep(60)
