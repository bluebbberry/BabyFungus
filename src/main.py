import time
from federated_learning import FederatedLearning
from rdf_knowledge_graph import RDFKnowledgeGraph
from mastodon_client import MastodonClient
import logging
import os
from dotenv import load_dotenv, dotenv_values

# Loading variables from .env file
load_dotenv()

# Configuring logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    logging.info("[START] Baby Fungus instance starting up")
    mastodon = MastodonClient()
    rdf_kg = RDFKnowledgeGraph(fuseki_server=os.getenv("FUSEKI_SERVER_UPDATE_URL"), fuseki_query=os.getenv("FUSEKI_SERVER_QUERY_URL"))
    fl = FederatedLearning()

    while True:
        logging.info("[CHECK] Looking for new fungus group")
        if rdf_kg.look_for_new_fungus_group():
            logging.info("[TRAINING] New fungus group found, starting training")
            model, gradients = fl.train()
            logging.info(f"[RESULT] Training complete. Model: {model.tolist()} | Gradients: {gradients.tolist()}")
            rdf_kg.save_model(model)
            mastodon.post_status(f"Training complete. Updated model: {model.tolist()}")
        else:
            logging.info("[WAIT] No new fungus group found, sleeping")
        time.sleep(60)

if __name__ == "__main__":
    logging.info("[INIT] Baby Fungus instance initializing")
    main()
