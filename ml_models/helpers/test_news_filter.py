import unittest
from utils import constants
from .news_filter import NewsFilter

class TestNewsFilter(unittest.TestCase):
    def setUp(self):
        self.__news_filter = NewsFilter()

    def test_should_filter_if_filtered_country_exist(self):
        headline = "Some very serious news from Malaysia"
        source = "authentic"
        result = self.__news_filter.should_filter(headline=headline, source=source)
        self.assertEqual(result, True, 'Country should be filtered')
    
    def test_should_filter_if_filtered_word_exist(self):
        headline = "A marvellous game was shown during Cricket match"
        source = "authentic"
        result = self.__news_filter.should_filter(headline=headline, source=source)
        self.assertEqual(result, True, 'Word should be filtered')
    
    def test_should_filter_if_filtered_source_exist(self):
        headline = "A marvellous game was shown during Cricket match"
        source = constants.SOURCES_TO_OMIT[0]
        result = self.__news_filter.should_filter(headline=headline, source=source)
        self.assertEqual(result, True, 'Source should be filtered')

    def test_should_return_false_if_no_matching_is_found(self):
        headline = "Country is blooming and every one is happy to live in"
        source = "very authentic"
        result = self.__news_filter.should_filter(headline=headline, source=source)
        self.assertEqual(result, False, 'Should return True instead')

if __name__ == '__main__':
    unittest.main()