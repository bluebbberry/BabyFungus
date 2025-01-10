# rdf_knowledge_graph.py
import requests
from rdflib import Graph, Namespace, Literal
import logging
from mastodon_client import MastodonClient
import time

logging.basicConfig(level=logging.INFO)

class RDFKnowledgeGraph:
    def __init__(self, fuseki_server, fuseki_query):
        self.FUSEKI_SERVER = fuseki_server
        self.FUSEKI_QUERY = fuseki_query
        self.DATA_NS = Namespace("http://example.org/data/")
        self.graph = Graph()
        self.graph.bind("data", self.DATA_NS)
        self.mastodon_client = MastodonClient()

    def save_to_knowledge_graph(self, model):
        self.graph.set((self.DATA_NS["model"], self.DATA_NS["weights"], Literal(str(model.tolist()))))
        response = requests.post(self.FUSEKI_SERVER, data=self.graph.serialize(format='nt'))
        if response.ok:
            logging.info("Model successfully saved to knowledge graph.")
        else:
            logging.error(f"Error saving model: {response.status_code}")

    def share_gradients(self, gradients):
        self.graph.set((self.DATA_NS["model"], self.DATA_NS["gradients"], Literal(str(gradients.tolist()))))
        response = requests.post(self.FUSEKI_SERVER, data=self.graph.serialize(format='nt'))
        if response.ok:
            logging.info("Gradients successfully shared.")
        else:
            logging.error("Failed to share gradients.")

    def aggregate_gradients(self):
        query = """
        PREFIX data: <http://example.org/data/>
        SELECT ?gradients WHERE { ?model data:gradients ?gradients }
        LIMIT 5
        """
        response = requests.post(self.FUSEKI_QUERY, data={'query': query}, headers={'Accept': 'application/sparql-results+json'})
        results = response.json().get("results", {}).get("bindings", [])
        aggregated_gradients = []
        for result in results:
            gradients = eval(result['gradients']['value'])
            aggregated_gradients.append(gradients)
        return aggregated_gradients

    def look_for_new_fungus_group(self):
        logging.info("Stage 1: Looking for a new fungus group to join...")
        messages = self.mastodon_client.fetch_and_respond_to_mastodon_requests(None)
        if not messages:
            logging.warning("No messages found under the nutrial hashtag. Trying again later...")
            return None

        for message in messages:
            if "kb-link" in message:
                logging.info("Received join request. Preparing to join...")
                link_to_knowledge_base = "http://example.org/data/"
                return link_to_knowledge_base
        logging.info("Announcing request to join the next epoch.")
        self.mastodon_client.post_status(f"Request-to-join: Looking for a training group. {self.mastodon_client.hashtag}")
        return None

    def save_model(self, model):
        pass

    def fetch_model_from_knowledge_base(self, link_to_model):
        return []

    def fetch_updates_from_knowledge_base(self, link_to_model):
        return []
