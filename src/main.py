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

class BabyFungus:
    def __init__(self):
        logging.info("[START] Baby Fungus instance starting up")
        self.mastodon = MastodonClient()
        self.rdf_kg = RDFKnowledgeGraph(fuseki_server=os.getenv("FUSEKI_SERVER_UPDATE_URL"), fuseki_query=os.getenv("FUSEKI_SERVER_QUERY_URL"))
        self.fl = FederatedLearning()
        self.feedback_threshold = 0.5

    def start(self):
        switch_team = True
        while True:
            logging.info("[CHECK] Looking for new fungus group")
            if switch_team:
                if self.rdf_kg.look_for_new_fungus_group():
                    logging.info("[TRAINING] New fungus group found, starting training")
                    self.train_and_deploy_model()
                else:
                    logging.info("[WAIT] No new fungus group found, answer user feedback")
            else:
                # participate in next epoche
                self.train_and_deploy_model()
            feedback = self.mastodon.answerUserFeedback()
            switch_team = self.decide_whether_to_switch_team(feedback)
            time.sleep(60)

    def train_and_deploy_model(self):
        model, gradients = self.fl.train()
        logging.info(f"[RESULT] Training complete. Model: {model.tolist()} | Gradients: {gradients.tolist()}")
        self.rdf_kg.save_model(model)
        self.mastodon.post_status(f"Training complete. Updated model: {model.tolist()}")
        logging.info("[FINISH] Training complete - start answering user feedback with new model")

    def decide_whether_to_switch_team(self, feedback):
        return feedback < self.feedback_threshold

if __name__ == "__main__":
    logging.info("[INIT] Baby Fungus instance initializing")
    babyFungus = BabyFungus()
    babyFungus.start()
