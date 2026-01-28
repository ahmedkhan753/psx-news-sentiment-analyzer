from utils import constants, functions

class NewsFilter:
    def __init__(self) -> None:
        self.__countries = self.__get_country_names()
    
    def should_filter(self, headline:str, source:str, filter_on_ommited_words=True) -> bool:
        filtered_words = constants.FILTERED_WORDS
        omitted_source = constants.SOURCES_TO_OMIT
        
        filtered_source = self.__in_array(omitted_source, source)
        filtered_country_exist = self.__in_array(self.__countries, headline)
        filtered_word_exists = self.__in_array(filtered_words, headline)

        # if news iteself from ommited source return early
        if filtered_source:
            return True
        
        # special condition if to apply filtering on ommited words or not
        if not filter_on_ommited_words:
            filtered_word_exists = False

        if filtered_country_exist or filtered_word_exists:
            return True
        
        return False

    def __get_country_names(self) -> list:
        names = []
        functions.loadCountries()
        countries = functions.getCountries()
        for data in countries:
            name = data.get('name')
            name = str(name).strip()
            names.append(name)
        return names
    
    def __in_array(self, array:list, sub_string:str) -> bool:
        import re
        sub_string_lower = sub_string.lower()
        for x in array:
            # Match whole word only to avoid generic filtering
            # escaped to handle any special chars in the array items
            pattern = r'\b' + re.escape(str(x).lower()) + r'\b'
            if re.search(pattern, sub_string_lower):
                return True
        return False