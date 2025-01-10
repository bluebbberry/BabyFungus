import time
import logging
import os
from dotenv import load_dotenv
from federated_learning import FederatedLearning
from rdf_knowledge_graph import RDFKnowledgeGraph
from mastodon_client import MastodonClient

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class BabyFungus:
    def __init__(self):
        logging.info("[INIT] Initializing Baby Fungus instance")
        self.mastodon = MastodonClient()
        self.rdf_kg = RDFKnowledgeGraph(
            fuseki_server=os.getenv("FUSEKI_SERVER_UPDATE_URL"),
            fuseki_query=os.getenv("FUSEKI_SERVER_QUERY_URL")
        )
        self.fl = FederatedLearning()
        self.feedback_threshold = float(os.getenv("FEEDBACK_THRESHOLD", 0.5))
        logging.info(f"[CONFIG] Feedback threshold set to {self.feedback_threshold}")

    def start(self):
        switch_team = True
        while True:
            try:
                logging.info("[CHECK] Searching for a new fungus group")
                if switch_team and self.rdf_kg.look_for_new_fungus_group():
                    logging.info("[TRAINING] New fungus group detected, initiating training")
                    self.train_and_deploy_model()
                else:
                    logging.info("[WAIT] No new groups found. Responding to user feedback.")

                feedback = self.mastodon.answerUserFeedback()
                logging.info(f"[FEEDBACK] Received feedback: {feedback}")

                switch_team = self.decide_whether_to_switch_team(feedback)

                time.sleep(60)
            except Exception as e:
                logging.error(f"[ERROR] An error occurred: {e}", exc_info=True)

    def train_and_deploy_model(self):
        try:
            logging.info("[TRAINING] Starting model training")
            model, gradients = self.fl.train()
            logging.info(f"[RESULT] Model trained successfully. Model: {model.tolist()}")

            self.rdf_kg.save_model(model)
            logging.info("[STORE] Model saved to RDF Knowledge Graph")

            self.mastodon.post_status(f"Training complete. Updated model: {model.tolist()}")
            logging.info("[NOTIFY] Status posted to Mastodon")
        except Exception as e:
            logging.error(f"[ERROR] Failed during training and deployment: {e}", exc_info=True)

    def decide_whether_to_switch_team(self, feedback):
        switch_decision = feedback < self.feedback_threshold
        logging.info(f"[DECISION] Switch team: {switch_decision}")
        return switch_decision

if __name__ == "__main__":
    logging.info("[STARTUP] Launching Baby Fungus instance")
    baby_fungus = BabyFungus()
    baby_fungus.start()
