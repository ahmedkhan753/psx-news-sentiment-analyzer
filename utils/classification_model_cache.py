from ml_models.national_news_sentiment_analysis.national_news_sentiment_classification import MultinomialNB,CountVectorizer

class ClassificationModelCache(object):
    __vector_shape = []
    __model: MultinomialNB
    __vector: CountVectorizer

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ClassificationModelCache, cls).__new__(cls)
        return cls.instance
    
    def load_model(self, model:MultinomialNB) -> None:
        self.__model = model

    def load_vector(self, vector:CountVectorizer) -> None:
        self.__vector = vector
    
    def load_vector_shape(self, vector_shape:list) -> None:
        self.__vector_shape = vector_shape
    
    def get_model(self) -> MultinomialNB:
        return self.__model
    
    def get_vector(self) -> CountVectorizer:
        return self.__vector
    
    def get_vector_shape(self) -> list:
        return self.__vector_shape
