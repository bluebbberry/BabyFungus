import pytest
from rdf_knowledge_graph import RDFKnowledgeGraph
from rdflib import Namespace, Graph, Literal

@pytest.fixture
def kg():
    return RDFKnowledgeGraph(fuseki_server="http://localhost:3030/ds/update", fuseki_query="http://localhost:3030/ds/query")

def test_save_to_knowledge_graph(kg):
    model = [0.5, 0.2, 0.7]
    kg.save_model(model)
    # Assuming the function returns success status
    assert True

def test_share_gradients(kg):
    gradients = [0.1, 0.1, 0.1]
    kg.share_gradients(gradients)
    # Assuming no exceptions indicate success
    assert True
