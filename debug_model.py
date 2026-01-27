import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import nltk
nltk.download('vader_lexicon')
from ml_models.national_news_sentiment_analysis.sentiment_analysis import SentimentAnalysis
from ml_models.national_news_sentiment_analysis.sentiment_classifier import SentimentClassifier

def debug_model():
    print("--- Debugging Model Training ---")
    sa = SentimentAnalysis(verbose=True)
    df = sa.process_training_data()
    
    # Filter out neutral
    df_train = df[df.label != 0].copy()
    print(f"Total training samples (non-zero): {len(df_train)}")
    print("Label distribution:")
    print(df_train.label.value_counts())
    
    sc = SentimentClassifier(verbose=True)
    # nb, vect, X_train = sc.train_model(df)
    
    # Manual mock training since SMOTE is missing
    df_train = df[df.label != 0]
    x = df_train.headline
    y = df_train.label
    vect = CountVectorizer(stop_words='english', binary=True)
    X_vect = vect.fit_transform(x)
    nb = MultinomialNB()
    nb.fit(X_vect, y)
    X_train = x # for consistency with sc.predict
    
    test_sentence = "ATC issues non-bailable arrest warrant for PTI chairman "
    print(f"\n--- Predicting for: '{test_sentence}' ---")
    
    # Check if words are in vocabulary
    words = test_sentence.lower().split()
    vocab = vect.get_feature_names_out()
    print("Words in vocabulary found in sentence:")
    for word in words:
        if word in vocab:
            print(f"  - {word}")
        else:
            print(f"  - {word} (NOT IN VOCAB)")
            
    # Predict
    pred = sc.predict(test_sentence, df, nb, vect, X_train)
    print(f"Final Prediction: {pred}")

    # Inspect weights (log probabilities)
    neg_ind = 0 if nb.classes_[0] == -1 else 1
    pos_ind = 1 - neg_ind
    
    # Get top 20 words contributing to positive class
    feature_names = vect.get_feature_names_out()
    pos_probs = nb.feature_log_prob_[pos_ind]
    neg_probs = nb.feature_log_prob_[neg_ind]
    
    word_probs = pd.DataFrame({
        'word': feature_names,
        'pos_log_prob': pos_probs,
        'neg_log_prob': neg_probs,
        'diff': pos_probs - neg_probs
    })
    
    print("\nTop words leaning towards POSITIVE (diff > 0):")
    print(word_probs.sort_values(by='diff', ascending=False).head(10))
    
    print("\nTop words leaning towards NEGATIVE (diff < 0):")
    print(word_probs.sort_values(by='diff', ascending=True).head(10))

if __name__ == "__main__":
    debug_model()
