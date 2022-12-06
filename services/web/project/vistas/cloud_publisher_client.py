from google.cloud import pubsub_v1
import os

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./path_to_your_.json_credential_file"

GCP_PROJECT_NAME = os.environ.get("GCP_PROJECT_NAME", "music-converter-prueba-1")
TARGET_TOPIC = os.environ.get("TARGET_TOPIC", "converter-topic")

class CloudPublisherClient:

    # Cliente publicador
    publisher_client = pubsub_v1.PublisherClient()

    def publish_message(self, message):
        topic_path = self.publisher_client.topic_path(GCP_PROJECT_NAME, TARGET_TOPIC)
        data_str = message #ver formato json en vistas, linea 103
        # Codificacion a bytestring
        data = data_str.encode("utf-8")
        # Capturar futuro retornado por cliente API
        future = self.publisher_client.publish(topic_path, data)
        print(future.result())