from .types import CountriesListType

class Countries(object):
    __list = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Countries, cls).__new__(cls)
        return cls.instance
    
    def load_countries_list(self, CountriesListType):
        self.__list = CountriesListType
    
    def get_countires_list(self) -> CountriesListType:
        return self.__list
