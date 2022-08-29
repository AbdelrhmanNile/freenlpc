# freenlpc
a wrapper for nlpcloud free-tier.

# FEATURES
- wrappes all the important nlpcloud free-tier models in one object.
- no rate limit per minute error, it will just keep on trying until it gets the response.
- you can initialize it with more than one API token, if one reached the rate limit it will automatically switch to the other API token.
