from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from .sentiment_analysis import SentimentAnalysis
from .sentiment_classifier import SentimentClassifier
from utils.types import NationalNewsPayloadListType, NationalNewsPayloadType

class NationalNewsSentimentClassification:
    def __init__(self, show_chart=False, verbose=True, train_model_data=False, omit_neutral_news=True) -> None:
        self.__show_chart = show_chart
        self.__verbose = verbose
        self.__train_model_data = train_model_data
        self.__omit_neutral = omit_neutral_news
    
    def train_model(self)-> tuple[MultinomialNB, CountVectorizer, list]:
        sentiment_analysis = SentimentAnalysis(show_chart=self.__show_chart, verbose=self.__verbose)
        classifier_model = SentimentClassifier(verbose=self.__verbose, omit_neutral_news=self.__omit_neutral)
        df: pd.DataFrame = sentiment_analysis.process_training_data()
        nb, vector, vector_shape = classifier_model.train_model(df)
        return nb, vector, vector_shape

    def perform_prediction(self, sentence:str, headline:NationalNewsPayloadListType, nb:MultinomialNB, vect:CountVectorizer, vector_training:any) -> tuple[list, pd.DataFrame]:
        sentiment_analysis = SentimentAnalysis(show_chart=self.__show_chart, verbose=self.__verbose)
        classifier_model = SentimentClassifier(verbose=self.__verbose)
        df: pd.DataFrame = sentiment_analysis.process_sentiment_analysis(sentences=headline)
        predictions = classifier_model.predict(sentence=sentence, df=df, nb=nb, vect=vect, vector_training=vector_training)
        return predictions, df