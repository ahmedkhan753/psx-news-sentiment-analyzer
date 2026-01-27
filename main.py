from fastapi import FastAPI, Form
from contextlib import asynccontextmanager
from typing import Annotated
import uvicorn
from utils import functions, types, classification_model_cache
from start import train_model, NationalNewsSentimentClassification, listen_events_from_news_fetcher
from ml_models.helpers import news_filter

# before all check for required envs
env_result, env_message = functions.check_required_values()
if not env_result:
    raise Exception(env_message)

# life span event callbacks
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("loading countries list")
    functions.loadCountries()
    print("training news classifier")
    train_model()
    print("Starting listening to events from news-fetcher")
    listen_events_from_news_fetcher(float(functions.get_env_value("PUB_SUB_TIMEOUT")) or 100)
    yield
    print("after app close event")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict/")
def predict(headline: Annotated[str, Form()], id: Annotated[str, Form()], source: Annotated[str, Form()], primary: Annotated[str, Form()]):
    # sanity check
    if not headline or not id or not source or not primary:
        return {"status": "false", "error": "bad payload"}
    
    cache = classification_model_cache.ClassificationModelCache()
    model = cache.get_model()
    vector = cache.get_vector()
    vector_shape_data = cache.get_vector_shape()

    if not model:
        return {"status": "false", "error": "bad model"}
    if not vector:
        return {"status": "false", "error": "bad vector"}
    if not len(vector_shape_data):
        return {"status": "false", "error": "bad vector shape"}
    
    # check if headline needs to be filtered
    should_filter = news_filter.NewsFilter().should_filter(headline=headline, source=source)
    if should_filter:
        return {"status": "false", "error": "headline is filtered out"}

    classification = NationalNewsSentimentClassification(show_chart=False, verbose=True, train_model_data=False)
    sentence = headline
    payload:types.NationalNewsPayloadType = types.NationalNewsPayloadType(primaryId=primary, id=id, source=source, headline=sentence, description='')
    payloadListType:types.NationalNewsPayloadListType = []
    payloadListType.append(payload)
    result, df = classification.perform_prediction(sentence=sentence, headline=payloadListType, nb=model, vect=vector, vector_training=vector_shape_data)
    return {"status": "ok", "prediction": result, "sentiment": df.to_dict()}

if __name__ == "__main__":
    currentEnvironment = functions.getCurrentEnvironment()
    env_port = functions.getPort()
    isProduction = functions.isProduction(currentEnvironment)
    uvicorn.run(app, host="0.0.0.0", port=env_port)
    print("Server running on %s on %s mode" %(env_port, currentEnvironment))
