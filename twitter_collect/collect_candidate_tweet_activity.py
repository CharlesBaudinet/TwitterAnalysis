import twitter_collect.twitter_connection_setup as tcs
import linecache
from tweepy.streaming import StreamListener
import tweepy

def get_replies_to_candidate(num_candidate):

    #lire dans le fichier le nom du candidate associé à son numero
    nom_candidate = linecache.getline("CandidateData/noms_candidates.txt", num_candidate)

    tweets_candidates_id = []
    connexion = tcs.twitter_setup()
    statuses = connexion.user_timeline(id = nom_candidate, count = 10)
    for status in statuses:
        tweets_candidates_id.append(status.id)

    replies_tweets_candidate = {}
    replies = connexion.search('@' + nom_candidate,language="french",rpp=4)
    for reply in replies:
        if reply.in_reply_to_status_id in tweets_candidates_id:
            replies_tweets_candidate[reply.in_reply_to_status_id] = reply.text

    return replies_tweets_candidate


def get_retweets_of_candidate(num_candidate):
    '''

    This function reads a candidate's last tweets and for each tweet,
    counts the number of retweets

    :param num_candidate:
    :return: a dictionary mapping a twitter id to it's retweet count
    '''
    # reads from a text file that maps the candidate's number to it's tweeter account name
    nom_candidate = linecache.getline("CandidateData/noms_candidates.txt", num_candidate)

    counter_retweets_candidate = {}
    connexion = tcs.twitter_setup()
    statuses = connexion.user_timeline(id = nom_candidate, count = 10)
    # for each tweet(status) we stash it's retweet count.
    for status in statuses:
        counter_retweets_candidate[status.id] = status.retweet_count

    return counter_retweets_candidate


def get_streaming_of_candidate(num_candidate):

    '''

    This function returns every tweet about a candidate with API Streaming and Filter

    :param num_candidate:
    :return: tweet about a condidate
    '''
    # reads from a text file that maps the candidate's number to it's tweeter account name
    nom_candidate = linecache.getline("CandidateData/noms_candidates.txt", num_candidate)


    class StdOutListener(StreamListener):

        def on_data(self, data):
            print(data)
            return True

        def on_error(self, status):
            if  str(status) == "420":
                print(status)
                print("You exceed a limited number of attempts to connect to the streaming API")
                return False
            else:
                return True

    def collect_by_streaming():

        connexion = tcs.twitter_setup()
        listener = StdOutListener()
        stream=tweepy.Stream(auth = connexion.auth, listener=listener)
        stream.filter(track=[nom_candidate])
        
    collect_by_streaming()
