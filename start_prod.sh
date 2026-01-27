#!/bin/bash
export PORT=4200
export APP_ENV=production
export NEWS_FETCHER_SUB=news-sentiment-news-fetcher-topic-sub
export GOOGLE_CLOUD_PROJECT=psx-bot
export NEWS_SENTIMENT_PROCESSED_TOPIC=news-sentiment-processor-topic
export PUB_SUB_TIMEOUT=604800
uvicorn main:app --reload --host 0.0.0.0 --port $PORT 