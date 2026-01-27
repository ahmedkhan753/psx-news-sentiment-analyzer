
import os
import json
from .constants import *
from .countries import CountriesListType, Countries
from .types import CountryType

def getPort() -> str:
    return os.getenv('PORT') or '4200'

def getCurrentEnvironment():
    return os.getenv('APP_ENV')

def isProduction(env_name) -> bool:
    if env_name == ENV_PPRODUCTION:
        return True
    return False

def get_env_value(env_name: str) -> str:
    return os.getenv(env_name)

def check_required_values() -> tuple[bool, str]:
    all_satisfied = True
    env_message = ''
    for env in REQUIRED_ENVS:
        env_value = get_env_value(env)
        if not env_value or not len(str(env_value)):
            env_message = "no value for %s detected" % env
            all_satisfied = False
            break
    return all_satisfied, env_message

def loadCountries() -> CountriesListType:
    path = "%s/utils/json_files/countries.json" %os.getcwd()
    print(path)
    f = open(path, 'r')
    data = json.load(f)
    countries = []
    for i in data:
        code = i['code']
        name = i['name']
        lower = str(i['name']).lower()
        country = CountryType(code=code, lower_case=lower, name=name)
        should_filter = [x for x in COUNTRIES_TO_OMIT if(x in country.get('lower_case'))]    
        if not bool(should_filter):
            countries.append(country)
    # call singleton class and load values there
    country_singleton = Countries()
    country_singleton.load_countries_list(countries)
    return country_singleton.get_countires_list()

def getCountries() -> CountriesListType:
    country_singleton = Countries()
    return country_singleton.get_countires_list()
