import twitter_collect.twitter_connection_setup as tcs

def get_tweets_from_candidates_search_queries(queries, twitter_api):
    '''
    This function returns the tweets searched with the queries
    specified and a twitter api connexion.
    :param queries:
    :param twitter_api:
    :return:
    '''
    for query in queries:
        tweets = twitter_api.search(query,language="french",rpp=10)
        for tweet in tweets:
            print(tweet.text)
