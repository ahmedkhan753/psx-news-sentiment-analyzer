
import json
from google.auth import jwt
from google.cloud import pubsub_v1
from utils.types import NationalNewsSentimentProcessedType
from utils.constants import NEWS_SENTIMENT_PROCESSED_TOPIC, GOOGLE_CLOUD_PROJECT_ID
from utils.functions import get_env_value

GOOGLE_PROJECCT = get_env_value(GOOGLE_CLOUD_PROJECT_ID)
TOPIC_NAME = get_env_value(NEWS_SENTIMENT_PROCESSED_TOPIC)

class PublishProcessedNews:
    def __init__(self) -> None:
        pass

    def publish(self, payload:NationalNewsSentimentProcessedType) -> bool:
        try:
            service_account_info = json.load(open("key.json"))
            audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
            credentials = jwt.Credentials.from_service_account_info(service_account_info, audience=audience)
            publisher = pubsub_v1.PublisherClient(credentials=credentials)
            topic_path = publisher.topic_path(GOOGLE_PROJECCT, TOPIC_NAME)
            json_dumps = json.dumps(payload)
            publisher.publish(topic_path, json_dumps.encode('utf-8'))
            return True
        except Exception as e:
            print("Error occurred while publishing data")
            print(e)
            return False 


