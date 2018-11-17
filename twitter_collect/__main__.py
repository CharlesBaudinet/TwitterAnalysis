import twitter_collect.collect_candidate_tweet_activity as ccta
import json

def main():
    candidates_name = []
    with open('CandidateData/noms_candidates.txt','r') as file:
        for line in file:
            candidates_name.append(line)

    tweets = {}

    for i in range(len(candidates_name)):
        candidate_info = []
        candidate_info.append(ccta.get_replies_to_candidate(i+1))
        candidate_info.append(ccta.get_retweets_of_candidate(i+1))
        #candidate_info.append(ccta.get_streaming_of_candidate(i+1))
        tweets[candidates_name[i]] = candidate_info
    return tweets

tweets = main()

def store_tweets(tweets,filename):
    '''

    This function simply stores all tweets given as json file,
    in hard drive

    :param tweets:
    :param filename:
    :return: saves in disk a json file (with filename)
    '''

    with open("output/" + filename + '.txt', 'w') as outfile:
        json.dump(tweets, outfile)


def status_to_dataframe(status):
    '''

    This function takes as an argument a list of statuses(tweets), chooses
    the most important features (defined by we).

    :param status:
    :return: returns a panda dataframe, with the chosen features.
    '''

    dataframe = {'text': [status.text] ,'date': [status.created_at],'hashtag': [status.entities['hashtags']],'id': [status.id],'location':[status.user['location']]}
    return dataframe


