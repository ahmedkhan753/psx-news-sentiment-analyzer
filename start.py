from ml_models.national_news_sentiment_analysis.national_news_sentiment_classification import NationalNewsSentimentClassification
from utils.classification_model_cache import ClassificationModelCache
from utils.functions import getCurrentEnvironment, isProduction
from pubsub_listeners_publishers.subscriber import news_fetcher_subscription

# train classifier model from test data
def train_model():
    show_chart = True
    if isProduction(getCurrentEnvironment()):
        show_chart = False
    classifier_model = NationalNewsSentimentClassification(verbose=True, train_model_data=True, show_chart=show_chart, omit_neutral_news=False)
    cache = ClassificationModelCache()
    model, vector, vector_shape = classifier_model.train_model()
    cache.load_model(model=model)
    cache.load_vector(vector=vector)
    cache.load_vector_shape(vector_shape=vector_shape)

# listen to events from news-process and perform sentiment analysis on them
def listen_events_from_news_fetcher(timeout:float):
    """
    Example payload
    {"id":"bc357db1-9f37-491b-8a8e-0adfeca8205d","primary":"367e61ca-d46f-4220-a46a-7b671903066d","source":"authentic","headline":"6 dead, 10 injured as gas cylinder explosion causes building to collapse in Jhelum"}
    """
    listener = news_fetcher_subscription.ListenToNewsFetcher()
    listener.listen(timeout)