from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import numpy as np
import pandas as pd
from utils.constants import SentimentClassifierPredictionLabels


class SentimentClassifier:
    def __init__(self, verbose=True, omit_neutral_news=True) -> None:
        self.__verbose = verbose
        self.__omit_neutral = omit_neutral_news
    
    def train_model(self, df:pd.DataFrame) -> tuple[MultinomialNB, CountVectorizer, list]:
        df = df[df.label != 0]
        df.label.value_counts()

        x = df.headline
        y = df.label
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
        vect = CountVectorizer(max_features=1000, binary=True, stop_words='english')
        X_train_vect = vect.fit_transform(X_train)
        counts = df.label.value_counts()
        self.__print_if_verbose(counts)
        self.__print_if_verbose("\nPredicting only -1 = {:.2f}% accuracy".format(counts[-1] / sum(counts) * 100))

         # using Smoote for imba;ance data
        try:
            from imblearn.over_sampling import SMOTE
            sm = SMOTE()
            X_train_res, y_train_res = sm.fit_resample(X_train_vect, y_train)
        except ImportError:
            print("SMOTE not found, skipping oversampling...")
            X_train_res, y_train_res = X_train_vect, y_train
        unique, counts = np.unique(y_train_res, return_counts=True)
        self.__print_if_verbose(list(zip(unique, counts)))

        # using Naive Bayes Classifier
        nb = MultinomialNB()
        nb.fit(X_train_res, y_train_res)
        naive_score = nb.score(X_train_res, y_train_res)
        print("NaiveBayes Score: %s" % naive_score)

        X_test_vect = vect.transform(X_test)
        self.__print_if_verbose("Shape needed for prediction \n")
        self.__print_if_verbose(X_test_vect.shape)
        y_pred = nb.predict(X_test_vect)
        print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
        #print("\nF1 Score: {:.2f}".format(f1_score(y_test, y_pred) * 100))
        print("\nCOnfusion Matrix:\n", confusion_matrix(y_test, y_pred))
        return nb, vect, X_train
    
    def predict(self, sentence:str, df: pd.DataFrame, nb:MultinomialNB, vect:CountVectorizer, vector_training:any) -> list:
        document_transformed = vect.transform([sentence]).reshape(1, -1)
        data_to_predict = document_transformed
        self.__print_if_verbose("Shape suppplied for prediction \n")
        self.__print_if_verbose(data_to_predict.shape)
        predictions = nb.predict(data_to_predict)

        prediction_label = SentimentClassifierPredictionLabels.NEGATIVE.name

        if predictions[0] == SentimentClassifierPredictionLabels.POSITIVE.value:
            prediction_label = SentimentClassifierPredictionLabels.POSITIVE.name
        
        predictions = predictions.tolist()
        predictions.append(prediction_label)

        print("[Sentence]:%s" % sentence)
        print(predictions)
        return predictions
    
    def __print_if_verbose(self, data:any) -> None:
        if self.__verbose:
           print(data) 
