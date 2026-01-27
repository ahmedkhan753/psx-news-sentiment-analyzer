from typing import TypedDict, List

class NationalNewsPayloadType(TypedDict):
    id: str
    headline: str
    description: str
    source: str
    primaryId: str

class NationalNewsSentimentProcessedType(TypedDict):
    id: str
    positive: float
    negative: float
    neutral: float
    compound: float
    sentiment_analysis_label: int
    classifier_prediction_result: int
    classifier_prediction_label: str
    primaryId: str

class CountryType(TypedDict):
    name: str
    code: str
    lower_case: str

CountriesListType = List[CountryType]
NationalNewsPayloadListType = List[NationalNewsPayloadType]