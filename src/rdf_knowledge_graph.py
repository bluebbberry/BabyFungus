# rdf_knowledge_graph.py
import requests
from rdflib import Graph, Namespace, Literal

class RDFKnowledgeGraph:
    def __init__(self, fuseki_server, fuseki_query):
        self.FUSEKI_SERVER = fuseki_server
        self.FUSEKI_QUERY = fuseki_query
        self.DATA_NS = Namespace("http://example.org/data/")
        self.graph = Graph()
        self.graph.bind("data", self.DATA_NS)

    def save_to_knowledge_graph(self, model):
        self.graph.set((self.DATA_NS["model"], self.DATA_NS["weights"], Literal(str(model.tolist()))))
        requests.post(self.FUSEKI_SERVER, data=self.graph.serialize(format='nt'))

    def share_gradients(self, gradients):
        self.graph.set((self.DATA_NS["model"], self.DATA_NS["gradients"], Literal(str(gradients.tolist()))))
        requests.post(self.FUSEKI_SERVER, data=self.graph.serialize(format='nt'))

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
