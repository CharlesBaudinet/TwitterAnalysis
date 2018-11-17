import pandas as pd
import matplotlib.pyplot as plt
import linecache
import twitter_collect.twitter_connection_setup as tcs
from textblob import *


def retweet_analysis(tweets):
    '''
    This function returns how many times a given tweet has been
    retweeted.


    :param tweets:
    :return: a dictionary
    '''

    #Here we use status attribute "retweet_count"

    retweet_count = {}
    for status in tweets:
        if status.id in retweet_count:
            retweet_count[status.id] += status.retweet_count
        else:
            retweet_count[status.id] = status.retweet_count
    return retweet_count

def favorite_analysis(tweets):
    '''
    This function returns how many times a given tweet has been
    favorited.


    :param tweets:
    :return: a dictionary
    '''

    #Here we use status attribute "favorite_count"
    favorite_count = {}
    for status in tweets:
        if status.id in favorite_count:
            favorite_count[status.id] += status.favorite_count
        else:
            favorite_count[status.id] = status.favorite_count
    return favorite_count

def likes_retweets_correlation(num_candidate):
    '''
    Establish the relation between retweets and likes.

    :param num_candidate, which is simply the line number in our noms_candidates.txt file.
    :return: a two dimensional plot, containing two curves, each one of them refering to the favorite
    and retweet count.
    '''

    nom_candidate = linecache.getline("CandidateData/noms_candidates.txt", num_candidate)

    connexion = tcs.twitter_setup()
    statuses = connexion.user_timeline(id = nom_candidate, count = 10)
    dict_retweet = retweet_analysis(statuses)
    dict_favorites = favorite_analysis(statuses)

    plt.plot([i for i in range(len(dict_favorites))],dict_favorites.values())
    plt.plot([i for i in range(len(dict_favorites))],dict_retweet.values())

    plt.xlabel('Tweet count')
    plt.ylabel('Statistics')
    plt.title('Relation between favorite/retweet')
    plt.legend(["favorites","retweets"])
    plt.show()



def collect_important_words(tweet):
    '''

    This function takes a single tweet and outputs a set containing it's "lemmatized" words

    :param tweet:
    :return: a set with the lemmatized words
    '''

    sentence = TextBlob(tweet)
    words = sentence.words
    words_blobbed = []

    # this loop takes in consideration when a word is a verb or not
    # (which is required by textblob when using the lemmatize function

    for word in words:
        if word.lemmatize() == word and word.lemmatize('v') == word:
            words_blobbed.append(word)
        elif word.lemmatize('v') == word:
            words_blobbed.append(word.lemmatize())
        else:
            words_blobbed.append(word.lemmatize('v'))
    return set(words_blobbed)


def candidate_sentiment_analysis(num_candidate):
    '''

    This function reads the last 100 tweets from a candidate (among the ones defined in "noms_candidates.txt" file)
    and utilizing textblob, performs sentiment analysis and prints the percentage for each sentiment defined
    (positive,neutral or negative).

    :param num_candidate:
    :return: prints the result
    '''

    nom_candidate = linecache.getline("CandidateData/noms_candidates.txt", num_candidate)

    connexion = tcs.twitter_setup()
    statuses = connexion.user_timeline(id = nom_candidate, count = 100)
    count_tweets = [0,0,0] # in order: positive, neutral and negative
    tweets = []
    for status in statuses:
        tweets.append(status.text)
    for tweet in tweets:
        polarity = TextBlob(tweet).sentiment.polarity
        if polarity > 0 :
            count_tweets[0] += 1
        elif polarity == 0 :
            count_tweets[1] += 1
        else:
            count_tweets[2] += 1


    print("Percentage of positive tweets: {}%".format(count_tweets[0]*100/len(tweets)))
    print("Percentage of neutral tweets: {}%".format(count_tweets[1]*100/len(tweets)))
    print("Percentage de negative tweets: {}%".format(count_tweets[2]*100/len(tweets)))

