from operator import itemgetter
import nlpcloud
import requests
from time import sleep

class FreeNlpc:
    def __init__(self, api_keys: list, gpu: bool=False, lang: str="en") -> None:
        self.__api_keys = api_keys
        self.__gpu = gpu
        self.__lang = lang
        self.activated_apikey = None
        self.__init_api()
        
        
    def __init_api(self):
        
        if self.activated_apikey == None:
            self.activated_apikey = 0
        elif self.activated_apikey == len(self.__api_keys) - 1:
            self.activated_apikey = 0
        elif self.activated_apikey < len(self.__api_keys):
            self.activated_apikey += 1
            
        api_key = self.__api_keys[self.activated_apikey]
        
        print(self.activated_apikey)
        self.__models = {"classification": nlpcloud.Client("bart-large-mnli-yahoo-answers", api_key, gpu=self.__gpu, lang=self.__lang),
                         "dialog_sum": nlpcloud.Client("bart-large-samsum", api_key, gpu=self.__gpu, lang=self.__lang),
                         "headline_gen":nlpcloud.Client("t5-base-en-generate-headline", api_key, gpu=self.__gpu, lang=self.__lang),
                         "entity_extraction": nlpcloud.Client("en_core_web_lg", api_key, gpu=self.__gpu, lang=self.__lang),
                         "qa": nlpcloud.Client("roberta-base-squad2", api_key, gpu=self.__gpu, lang=self.__lang),
                         "semantic_similarity": nlpcloud.Client("paraphrase-multilingual-mpnet-base-v2", api_key, gpu=self.__gpu, lang=self.__lang),
                         "sentiment_pos_neg": nlpcloud.Client("distilbert-base-uncased-finetuned-sst-2-english", api_key, gpu=self.__gpu, lang=self.__lang),
                         "sentiment_emotions": nlpcloud.Client("distilbert-base-uncased-emotion", api_key, gpu=self.__gpu, lang=self.__lang),
                         "summarization": nlpcloud.Client("bart-large-cnn", api_key, gpu=self.__gpu, lang=self.__lang),
                        }
        
    
    def classification(self, text: str, lables: list, multiclass: bool =True):
        while True:
            try:
                sleep(2)
                response = self.__models["classification"].classification(text, lables, multiclass)
                result = []
                for i in range(len(response['labels'])):
                    info = {}
                    info['label'] = response['labels'][i]
                    info['score'] = response['scores'][i]
                    result.append(info)
        
                ordered = sorted(result, key=itemgetter('score'), reverse=True)
                return {'scored_labels': ordered}
            except requests.exceptions.HTTPError:
                self.__init_api()

    
    def dialog_sum(self, dialog: str):
        while True:
            try:
                sleep(2)
                return self.__models["dialog_sum"].summarization(dialog)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def headline_gen(self, text: str):
        while True:
            try:
                sleep(2)
                return self.__models["headline_gen"].summarization(text)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def entities_extraction(self, text: str): 
        while True:
            try:
                sleep(2)
                return self.__models["entity_extraction"].entities(text)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def qa(self, question: str, context: str):
        while True:
            try:
                sleep(2)
                return self.__models["qa"].question(question=question, context=context)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def semantic_similarity(self, texts: list):
        while True:
            try:
                sleep(2)
                return self.__models["semantic_similarity"].semantic_similarity(texts)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def sentiment_pos_neg(self, text: str):
        while True:
            try:
                sleep(2)
                response = self.__models["sentiment_pos_neg"].sentiment(text)
                return response
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def sentiment_emotions(self, text: str):
        while True:
            try:
                sleep(2)
                response = self.__models["sentiment_emotions"].sentiment(text)["scored_labels"]
                ordered = sorted(response, key=itemgetter('score'), reverse=True)
                return {'scored_labels': ordered}
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def summarization(self, text: str):
        while True:
            try:
                sleep(2)
                return self.__models["summarization"].summarization(text)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def embeddings(self, texts: list):
        while True:
            try:
                sleep(2)
                return self.__models["semantic_similarity"].embeddings(texts)
            except requests.exceptions.HTTPError:
                self.__init_api()
