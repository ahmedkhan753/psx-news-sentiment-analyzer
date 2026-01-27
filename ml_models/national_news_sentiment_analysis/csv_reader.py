import csv
import json
from utils.types import NationalNewsPayloadListType, NationalNewsPayloadType
from ..helpers.news_filter import NewsFilter

class CsvReader:
    def __init__(self, file_path:str, verbose=False) -> None:
        self.__file_path = file_path
        self.__news_list = []
        self.__news_filter = NewsFilter()
        self.__verbose = verbose
    
    def read(self):
        line_count = 0
        filter_count = 0
        with open(self.__file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                    continue

                # _id,createdAt,headlines,id,source
                primary_id = row[3]
                headlines_json_string = row[2]
                source = row[4]
                headlines_parsed = json.loads(headlines_json_string)
                news_type_parsed = self.__parse_headline_json(primary_id, headlines_parsed, source)
                for item in news_type_parsed:
                    line =  item.get('headline')
                    line = str(line).strip()
                    line = line.replace("'s", '')
                    should_filter = self.__news_filter.should_filter(headline=line, source=source, filter_on_ommited_words=False)
                        
                    if should_filter:
                        if self.__verbose:
                            print("[filtered]: %s" % line)
                        filter_count += 1
                    else:
                        self.__news_list.append(item)    
                    line_count += 1
        print("Total HeadlinesCount=%s" % line_count)
        print("Total Filtered HeadlinesCount=%s" % filter_count)
        print("FilteredTotal=%s" % (line_count - filter_count))

    def __parse_headline_json(self, primary_id:str, parsed:any, source:str) -> NationalNewsPayloadListType:
        news_list = []
        # id,headline,sentiment
        for item in parsed:
            id = item['id']
            headline = item['headline']
            data = NationalNewsPayloadType(primaryId=primary_id, id=id, source=source, headline=headline, description='')
            news_list.append(data)
        return news_list
    
    def get_parsed_news_list(self) -> NationalNewsPayloadListType:
        return self.__news_list
