import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pprint import pprint
from .csv_reader import CsvReader
from utils.types import NationalNewsPayloadListType, NationalNewsPayloadType

class SentimentAnalysis:
    def __init__(self, show_chart=False, verbose=True) -> None:
        self.__show_chart = show_chart
        self.__verbose = verbose
        self.__csv_path = "%s/ml_models/nationalnews.csv" %os.getcwd()
        if verbose:
            print("CSV_PATH: %s" %self.__csv_path)
    
    def process_training_data(self) -> pd.DataFrame:
        csv_reader = CsvReader(self.__csv_path)
        csv_reader.read()
        headlines = csv_reader.get_parsed_news_list()
        self.__print_if_verbose("Total headlines=%s" % len(headlines))
        return self.process_sentiment_analysis(headlines)

    def process_sentiment_analysis(self, sentences:NationalNewsPayloadListType) -> pd.DataFrame:
        sia = SIA()
        results = []
        headlines:NationalNewsPayloadListType = sentences
        
        for data in headlines:
            headline = data.get('headline')
            pol_score = sia.polarity_scores(headline)
            pol_score['headline'] = headline
            pol_score['id'] = data.get('id')
            pol_score['primary_id'] = data.get('primaryId')
            pol_score['source'] = data.get('source')
            results.append(pol_score)
        
        # Let's create a positive label of 1 if the compound is greater than 0.2, 
        # and a label of -1 if compound is less than -0.2.
        # Everything else will be 0.
        df = pd.DataFrame.from_records(results)
        df['label'] = 0
        df.loc[df['compound'] > 0.2, 'label'] = 1
        df.loc[df['compound'] < -0.2, 'label'] = -1

        self.__print_if_verbose(df.label.value_counts())
        self.__print_if_verbose(df.label.value_counts(normalize=True) * 100)
            
        # plots
        self.__display_chart(df=df)
        return df
    
    def __display_chart(self, df:pd.DataFrame) -> bool:
        if not self.__show_chart:
            return False
        fig, ax = plt.subplots(figsize=(8, 8))
        counts = df.label.value_counts(normalize=True) * 100
        sns.barplot(x=counts.index, y=counts, ax=ax)
        ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
        ax.set_ylabel("Percentage")
        plt.show()
        return True

    def __print_if_verbose(self, data:any) -> None:
        if self.__verbose:
           print(data) 