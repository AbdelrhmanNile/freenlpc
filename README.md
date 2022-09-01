# freenlpc
a wrapper for nlpcloud free-tier.

# FEATURES
- wrappes all the important nlpcloud free-tier models in one object.
- no rate limit per minute error, it will just keep on trying until it gets the response.
- you can initialize it with more than one API token, if one reached the rate limit it will automatically switch to the other API token.

# AVAILABLE TASKS
- classification
- dialog summary
- headline generation
- entities extraction
- question answering
- semantic similarity
- sentiment/emotions analysis
- summarization
- embeddings
- translation
- language detection
- tokenization and lemmatization
- sentence dependencies

# INSTALLATION
```
pip install freenlpc
```
# USAGE
```
from freenlpc import FreeNlpc

tokens = ["token1", "token2"] # your nlpcloud api token/s
nlpc = FreeNlpc(tokens)

# then use whatever task you want
result = nlpc.sentiment_emotions("i am feelin happy")
```
