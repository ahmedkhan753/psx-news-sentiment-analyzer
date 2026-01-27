from enum import Enum

ENV_STAGING = 'staging'
ENV_PPRODUCTION = 'production'
NEWS_FETCHER_SUBCRIPTION = 'NEWS_FETCHER_SUB'
NEWS_SENTIMENT_PROCESSED_TOPIC = 'NEWS_SENTIMENT_PROCESSED_TOPIC'
GOOGLE_CLOUD_PROJECT_ID= 'GOOGLE_CLOUD_PROJECT'

COUNTRIES_TO_OMIT = [
    'pakistan', 'america',
    'china', 'saudi arabia'
    #,'india'
]

FILTERED_WORDS = [
 'Olympic', 'Europe', 'ChatGPT', 'Meta', 'Covid',
 'Wimbledon', 'Eidul Azha', 'Beijing', 'Haj', 'EU',
 'maritime', 'dies', 'cyclone', 'accident', 'BLF', 'Greek',
 'Titanic', 'UN', 'Wagner', 'monsoon', 'harrasment', 'civilians',
 'Polo', 'Sterling', 'Musk', 'Elon', 'Zuckerberg', 'Holi', 'Coast',
 'cars', 'Eid', 'Ramadan', 'holiday', 'Cup', 'FIFA', 'Cricket', 'PCB',
 'food', 'KE', 'Askari', 'aviation', 'HEC', 'social', 'boat', 'sea'    
]

SOURCES_TO_OMIT = [
    'arynews'
]

class SentimentClassifierPredictionLabels(Enum):
    POSITIVE = 1
    NEGATIVE = -1

REQUIRED_ENVS = [
    'PORT',
    NEWS_FETCHER_SUBCRIPTION,
    GOOGLE_CLOUD_PROJECT_ID,
    NEWS_SENTIMENT_PROCESSED_TOPIC,
]