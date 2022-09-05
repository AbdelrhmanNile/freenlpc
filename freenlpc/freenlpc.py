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
            "classification2": "xlm-roberta-large-xnli",
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
            "lang_detection": "python-langdetect",
            "tokenize": "en_core_web_lg",
            "sentence_dependencies": "en_core_web_lg"
        }
        self.activated_apikey = None
        self.__check_keys()
        self.__init_api()
        
    
    def __check_keys(self):
        """check if API tokens passed to the constructor are valid.

        Raises:
            Exception: API Token at index {i} is not valid.
        """
        for i in range(len(self.__api_keys)):
            try:
                nlpcloud.Client(self.which_model("sentiment_pos_neg"),
                            self.__api_keys[i], lang="en").sentiment("i hate physics")
            except requests.exceptions.HTTPError:
                raise Exception(f"API Token at index {i} is not valid.")
            
    def which_model(self, task_name):
        """which model is being used for a specific task.

        Args:
            task_name (str): function's name.

        Returns:
            str: model's name.
        """
        return self.__task_model[task_name]
    
    def __init_api(self):
        """initialize the apis and switch between api keys
        """
        if self.activated_apikey == None:
            self.activated_apikey = 0
        elif self.activated_apikey == len(self.__api_keys) - 1:
            self.activated_apikey = 0
        elif self.activated_apikey < len(self.__api_keys):
            self.activated_apikey += 1
            
        api_key = self.__api_keys[self.activated_apikey]
        
        self.__models = {"classification": nlpcloud.Client(self.which_model("classification"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "classification2": nlpcloud.Client(self.which_model("classification2"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "dialog_sum": nlpcloud.Client(self.which_model("dialog_sum"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "headline_gen":nlpcloud.Client(self.which_model("headline_gen"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "entities_extraction": nlpcloud.Client(self.which_model("entities_extraction"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "qa": nlpcloud.Client(self.which_model("qa"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "semantic_similarity": nlpcloud.Client(self.which_model("semantic_similarity"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "sentiment_pos_neg": nlpcloud.Client(self.which_model("sentiment_pos_neg"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "sentiment_emotions": nlpcloud.Client(self.which_model("sentiment_emotions"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "summarization": nlpcloud.Client(self.which_model("summarization"), api_key, gpu=self.__gpu, lang=self.__lang),
                         "translation": nlpcloud.Client(self.which_model("translation"), api_key, gpu=self.__gpu),
                         "lang_detection": nlpcloud.Client(self.which_model("lang_detection"), api_key),
                         "tokenize": nlpcloud.Client(self.which_model("tokenize"), api_key),
                         "sentence_dependencies": nlpcloud.Client(self.which_model("sentence_dependencies"), api_key)
                        }
        
    
    def classification(self, text: str, lables: list, multiclass: bool =True):
        """perform classification on a piece of text.

        Args:
            text (str): The block of text you want to analyze. 2,500 tokens maximum.
            lables (list): A list of labels you want to use to classify your text. 25 labels maximum.
            multiclass (bool, optional): Whether multiple labels should be applied to your text,
                meaning that the model will calculate an independent score for each label. Defaults to True.

        Returns:
            dict: scored labels.
        """
        while True:
            try:
                sleep(1)
                response = self.__models[self.classification.__name__].classification(text, lables, multiclass)
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
    
    def classification2(self, text: str):
        """perform classification on a piece of text.

        Args:
            text (str): The block of text you want to analyze. 2,500 tokens maximum.
            lables (list): A list of labels you want to use to classify your text. 25 labels maximum.
            multiclass (bool, optional): Whether multiple labels should be applied to your text,
                meaning that the model will calculate an independent score for each label. Defaults to True.


        Returns:
            dict: scored labels.
        """
        while True:
            try:
                sleep(1)
                response = self.__models[self.classification2.__name__].classification(text)
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
        """summarize a dialog.

        Args:
            dialog (str): the dialog you want to summarize. 1024 tokens maximum.

        Returns:
            dict: summary text.
        """
        while True:
            try:
                sleep(1)
                return self.__models[self.dialog_sum.__name__].summarization(dialog)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def headline_gen(self, text: str):
        """Headline generation is a summarization task that creates a very short summary, suited for news headlines.

        Args:
            text (str): The block of text that you want to summarize. 8192 tokens maximum.

        Returns:
            dict: headline.
        """
        while True:
            try:
                sleep(1)
                return self.__models[self.headline_gen.__name__].summarization(text)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def entities_extraction(self, text: str):
        """extract entities from a block of text.
        
        Args:
            text (str): The sentence you want to analyze. 350 tokens maximum.
            
        Returns:
            dict: entities.
        """ 
        while True:
            try:
                sleep(1)
                return self.__models[self.entities_extraction.__name__].entities(text)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def qa(self, question: str, context: str):
        """Answer a question using a context.

        Args:
            question (str): The question you want to ask.
            context (str): The block of text that the model will use in order to find an answer to your question.
                25,000 tokens maximum.

        Returns:
            dict: answer.
        """
        while True:
            try:
                sleep(1)
                return self.__models[self.qa.__name__].question(question=question, context=context)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def semantic_similarity(self, texts: list):
        """detect whether 2 pieces of text have the same meaning or not.

        Args:
            texts (list): The pieces of text you want to analyze.
                The list should contain exactly 2 elements.
                Each element should contain 128 tokens maximum.

        Returns:
            dict: score.
        """
        while True:
            try:
                sleep(1)
                return self.__models[self.semantic_similarity.__name__].semantic_similarity(texts)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def sentiment_pos_neg(self, text: str):
        """determine whether a text is positive or negative.

        Args:
            text (str): The block of text you want to analyze. 512 tokens maximum.

        Returns:
            dict: scored labels.
        """
        while True:
            try:
                sleep(1)
                return self.__models[self.sentiment_pos_neg.__name__].sentiment(text)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def sentiment_emotions(self, text: str):
        """detect sadness, joy, love, anger, fear, and surprise.

        Args:
            text (str): The block of text you want to analyze. 512 tokens maximum.

        Returns:
            dict: scored emotions.
        """
        while True:
            try:
                sleep(1)
                response = self.__models[self.sentiment_emotions.__name__].sentiment(text)["scored_labels"]
                ordered = sorted(response, key=itemgetter('score'), reverse=True)
                return {'scored_labels': ordered}
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def summarization(self, text: str):
        """summarize a text.

        Args:
            text (str): The block of text that you want to summarize. 1024 tokens maximum.

        Returns:
            dict: summary text.
        """
        while True:
            try:
                sleep(1)
                return self.__models[self.summarization.__name__].summarization(text)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def embeddings(self, texts: list):
        """calculate word embeddings. 

        Args:
            texts (list): The pieces of text you want to analyze.
                The list can contain 50 elements maximum. Each element should contain 128 tokens maximum.

        Returns:
            dict: embeddings
        """
        while True:
            try:
                sleep(1)
                return self.__models["semantic_similarity"].embeddings(texts)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def translation(self, text: str, source_lang: str, target_lang: str):
        """translate text.

        Args:
            text (str): The sentence that you want to translate. 250 tokens maximum.
            source_lang (str): The language code of the input text. If is an empty string,
                the model will try to automatically detect the input language,
                but if you know the language it is recommended to explicitly mention it.
            target_lang (str): The language of the translated text.
        
        for language codes:
            https://docs.nlpcloud.com/#translation

        Returns:
            dict: translation text.
        """
        while True:
            try:
                sleep(1)
                return self.__models[self.translation.__name__].translation(text, source_lang, target_lang)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def lang_detection(self, text: str):
        """detect which language a text is in.

        Args:
            text (str): The block of text containing one or more languages your want to detect. 25,000 tokens maximum.

        Returns:
            dict: scored languages.
        """
        while True:
            try:
                sleep(1)
                response = self.__models[self.lang_detection.__name__].langdetection(text)["languages"]
                result = []
                for i in response:
                    lang = list(i.keys())[0]
                    score = i[lang]
                    result.append({'language': lang, 'score': score})
                return {'scored_languages': result}
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def tokenize(self, text: str):
        """tokenize and lemmatize a text

        Args:
            text (str): The sentence containing the tokens to extract. 350 tokens maximum.

        Returns:
            dict: tokens
        """
        while True:
            try:
                sleep(1)
                return self.__models[self.tokenize.__name__].tokens(text)
            except requests.exceptions.HTTPError:
                self.__init_api()
    
    def sentence_dependencies(self, text: str):
        """perform Part-of-Speech (POS) tagging.
        
        Args:
            text (str): The sentences containing parts of speech to extract. 350 tokens maximum.

        Returns:
            dict: sentence dependencies.
        """
        while True:
            try:
                sleep(1)
                return self.__models[self.sentence_dependencies.__name__].sentence_dependencies(text)
            except requests.exceptions.HTTPError:
                self.__init_api()
                       
    
    def __repr__(self) -> str:
        tasks = list(self.__task_model.keys())
        models = list(self.__task_model.values())
        result = "\n"
        for i in range(len(tasks)):
            result = result + f"{tasks[i]}: {models[i]}\n"
        return "{" + result + "}"
