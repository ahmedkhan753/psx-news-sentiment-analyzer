from google.cloud import pubsub_v1
from google.auth import jwt
import json
from concurrent.futures import TimeoutError
from utils.constants import NEWS_FETCHER_SUBCRIPTION, GOOGLE_CLOUD_PROJECT_ID
from utils.functions import get_env_value
from utils.types import NationalNewsPayloadType, NationalNewsSentimentProcessedType
from utils.classification_model_cache import ClassificationModelCache
from ml_models.national_news_sentiment_analysis.national_news_sentiment_classification import NationalNewsSentimentClassification
from ..publisher import processed_news_publisher

SUBCRIPTION_NAME = get_env_value(NEWS_FETCHER_SUBCRIPTION)
GOOGLE_PROJECCT = get_env_value(GOOGLE_CLOUD_PROJECT_ID)

class ListenToNewsFetcher:
    def __init__(self) -> None:
        pass

    def listen(self, timeout:float):
        service_account_info = json.load(open("key.json"))
        audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"
        credentials = jwt.Credentials.from_service_account_info(service_account_info, audience=audience)

        subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

        subcription_path = subscriber.subscription_path(GOOGLE_PROJECCT, SUBCRIPTION_NAME)

        def callback(message: pubsub_v1.subscriber.message.Message) -> None:
            try:
                print(f"Received {message}.")
                parsed_message = json.loads(message.data.decode("utf-8"))
                print(parsed_message)
                self.process(parsed_message)
                message.ack()
            except Exception as e:
                print("error occurred")
                print(e)
                message.ack()
        
        streaming_pull_future = subscriber.subscribe(subcription_path, callback=callback)
        print(f"Listening for messages on {subcription_path}..\n")
        with subscriber:
            try:
                # When `timeout` is not set, result() will block indefinitely,
                # unless an exception is encountered first.
                streaming_pull_future.result(timeout=timeout)
            except TimeoutError:
                print("here at timeout now...")
                streaming_pull_future.cancel()  # Trigger the shutdown.
                streaming_pull_future.result()  # Block until the shutdown is complete.
    
    def process(self, payload:NationalNewsPayloadType) -> tuple[bool, str]:
        result = False
        message = ''
        sentence = payload.get('headline')
        payloads = []
        payloads.append(payload)
        cache = ClassificationModelCache()
        model = cache.get_model()
        vector = cache.get_vector()
        vector_shape_data = cache.get_vector_shape()

        if not model:
            raise Exception('no model detected')
        if not vector:
            raise Exception('no vector detected')
        if not len(vector_shape_data):
            raise Exception('no vector shape detected')

        # perfrom sentiment analysis here
        classifier_model = NationalNewsSentimentClassification(show_chart=False, verbose=True, train_model_data=False, omit_neutral_news=True)
        prediction_result, df = classifier_model.perform_prediction(
            headline=payloads, sentence=sentence, nb=model, vect=vector, vector_training=vector_shape_data
            )
        df_to_dict = df.to_dict()
        print(prediction_result)
        print(df_to_dict)

        # parse predicted result and convert it into type now
        parsed_predicted_result = NationalNewsSentimentProcessedType(
            id=payload.get('id'), primaryId=payload.get('primaryId'), 
            classifier_prediction_result=prediction_result[0],
            classifier_prediction_label=prediction_result[1],
            negative=df_to_dict['neg'][0],
            neutral=df_to_dict['neu'][0],
            positive=df_to_dict['pos'][0],
            compound=df_to_dict['compound'][0],
            sentiment_analysis_label=df_to_dict['label'][0],
        )
        # publish these processed sentiment to topic now
        print(parsed_predicted_result)
        publisher = processed_news_publisher.PublishProcessedNews()
        publisher.publish(parsed_predicted_result)
        return result, message