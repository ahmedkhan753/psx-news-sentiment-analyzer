from ml_models.helpers.news_filter import NewsFilter
from utils import constants, functions
import re

def debug():
    nf = NewsFilter()
    headline = "Nearly 100 dead as Indian states swelter in heat"
    source = "manual"
    
    print(f"Testing headline: '{headline}'")
    should_filter = nf.should_filter(headline, source)
    print(f"Should filter: {should_filter}")
    
    # manual debug to find the culprit
    countries = nf._NewsFilter__countries # access private member
    filtered_words = constants.FILTERED_WORDS
    
    print("\n--- Checking Countries ---")
    for x in countries:
        pattern = r'\b' + re.escape(str(x).lower()) + r'\b'
        if re.search(pattern, headline.lower()):
            print(f"MATCHED COUNTRY: '{x}' with pattern '{pattern}'")

    print("\n--- Checking Filtered Words ---")
    for x in filtered_words:
        pattern = r'\b' + re.escape(str(x).lower()) + r'\b'
        if re.search(pattern, headline.lower()):
            print(f"MATCHED WORD: '{x}' with pattern '{pattern}'")

if __name__ == "__main__":
    debug()
