from operator import itemgetter
import nlpcloud
import requests
from time import sleep

class FreeNlpc:
    def __init__(self, api_keys: list, gpu: bool=False, lang: str="en") -> None:
        self.__api_keys = api_keys
        self.__gpu = gpu
        self.__lang = lang
        self.__task_model = {
            "classification": "bart-large-mnli-yahoo-answers",
            "dialog_sum": "bart-large-samsum",
            "headline_gen": "t5-base-en-generate-headline",
            "entities_extraction": "en_core_web_lg",
            "qa": "roberta-base-squad2",
            "semantic_similarity": "paraphrase-multilingual-mpnet-base-v2",
            "sentiment_pos_neg": "distilbert-base-uncased-finetuned-sst-2-english",
            "sentiment_emotions": "distilbert-base-uncased-emotion",
            "summarization": "bart-large-cnn",
            "embeddings": "paraphrase-multilingual-mpnet-base-v2",
            "translation": "nllb-200-3-3b",
            "lang_detection": "python-langdetect"
        }
        self.activated_apikey = None
        self.__init_api()
        
    
    def which_model(self, task_name):
        return self.__task_model[task_name]
    
    def __init_api(self):
        
        if self.activated_apikey == None:
            self.activated_apikey = 0
        elif self.activated_apikey == len(self.__api_keys) - 1:
            self.activated_apikey = 0
        elif self.activated_apikey < len(self.__api_keys):
            self.activated_apikey += 1
            
        api_key = self.__api_keys[self.activated_apikey]
        
        self.__models = {"classification": nlpcloud.Client(self.which_model("classification"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "dialog_sum": nlpcloud.Client(self.which_model("dialog_sum"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "headline_gen":nlpcloud.Client(self.which_model("headline_gen"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "entities_extraction": nlpcloud.Client(self.which_model("entities_extraction"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "qa": nlpcloud.Client(self.which_model("qa"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "semantic_similarity": nlpcloud.Client(self.which_model("semantic_similarity"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "sentiment_pos_neg": nlpcloud.Client(self.which_model("sentiment_pos_neg"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "sentiment_emotions": nlpcloud.Client(self.which_model("sentiment_emotions"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "summarization": nlpcloud.Client(self.which_model("summarization"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "translation": nlpcloud.Client(self.which_model("translation"), api_key, gpu=self.__gpu),
                         "lang_detection": nlpcloud.Client(self.which_model("lang_detection"), api_key)
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
    
    def translation(self, text: str, source_lang: str, target_lang: str):
        while True:
            try:
                sleep(2)
                return self.__models["translation"].translation(text, source_lang, target_lang)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def lang_detection(self, text: str):
        while True:
            try:
                sleep(2)
                response = self.__models["lang_detection"].langdetection(text)["languages"]
                result = []
                for i in response:
                    lang = list(i.keys())[0]
                    score = i[lang]
                    result.append({'language': lang, 'score': score})
                return {'scored_languages': result}
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def __repr__(self) -> str:
        tasks = list(self.__task_model.keys())
        models = list(self.__task_model.values())
        result = "\n"
        for i in range(len(tasks)):
            result = result + f"{tasks[i]}: {models[i]}\n"
        return "{" + result + "}"
