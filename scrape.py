import twint
from datetime import date

class TwitterScraper(object):
    """
    This class is a twitter TwitterScraper called TwitterScraper. It takes the user as input and collects the user's tweets
    from 'from_date' to 'to_date'. If 'from_date' and 'to_date' are not specified, it collects the number of tweets 'num_tweets' from today.
    It outputs a dictionary with the tweet unique id and some other information.
    input: user, from_date, to_date, num_tweets
    output: dict
    """
    def __init__(self, from_date="2006-07-01", to_date=str(date.today()), num_tweets=20):
        self.from_date = from_date
        self.to_date = to_date
        self.num_tweets = num_tweets
        self.conf = twint.Config()

    def scrape_by_user(self, _user):
        """This method uses twint to extract tweets  based on username"""
        self.conf.Search = "from:@" + _user  # is the search configuration is given in this format it searches after
        # user_names.
        return self.__get_tweets__from_twint__()

    def scrape_by_string(self, _string: str):
        """This method uses twint to extract tweets based on string.
        all extracted tweets have the specified word in _string parameter in it.
        """
        self.conf.Search = _string  # this tells twint configuration to search for string 
        return self.__get_tweets__from_twint__()

    def scrape_by_user_and_string(self, _user: str, _string: str):
        """This method uses twint to extract tweets brased on string and username"""
        self.conf.Username = _user
        self.conf.Search = _string
        return self.__get_tweets__from_twint__()

    def get_only_tweets(self, tweet_and_replies_info):
        tweet_and_replies = tweet_and_replies_info["tweet"]
        """
        This functions input arg is a data frame (the output from scrape methords ) and removes...
         all tweets starting with \"@\" which is indicator of a reply or retweet.
        """
        indx_replies = []
        for i in range(len(tweet_and_replies)):
            if tweet_and_replies[i].startswith("@"):
                indx_replies.append(i)

        tweets_info = tweet_and_replies_info.drop(labels=indx_replies, axis=0)
        # drop removes the columns which its index specified by
        # indx_replies. axis=0  if we want to delete rows.
        #print(len(tweets['tweet']), " of them are Tweets")
        return tweets_info

    def __get_tweets__from_twint__(self):
        """ __get_tweets_from_twint__
        tweet info is a dataframe with fallowing columns
            Index(['id', 'conversation_id', 'created_at', 'date', 'timezone', 'place',
            'tweet', 'language', 'hashtags', 'cashtags', 'user_id', 'user_id_str',
            'username', 'name', 'day', 'hour', 'link', 'urls', 'photos', 'video',
            'thumbnail', 'retweet', 'nlikes', 'nreplies', 'nretweets', 'quote_url',
            'search', 'near', 'geo', 'source', 'user_rt_id', 'user_rt',
            'retweet_id', 'reply_to', 'retweet_date', 'translate', 'trans_src',
            'trans_dest']
        we just pick the relevant ones.
        c is a twint.Config() object
        we also configure twint output.
        """
        self.conf.Pandas = True  #
        self.conf.Count = True  #
        self.conf.Limit = self.num_tweets  # specifies how many tweet should be scraped
        self.conf.Since = self.from_date
        self.conf.Until = self.to_date
        self.conf.Hide_output = True  # Hides the output. If set to False it will prints tweets in the terminal window.
        twint.run.Search(self.conf)
        tweet_and_replies_inf = twint.output.panda.Tweets_df  # here we say that output souldwe dataframe.
        tweet_and_replies_inf = tweet_and_replies_inf[
            ["id", "tweet", "date", "user_id", "username", "urls", 'nlikes', 'nreplies', 'nretweets']]
        return tweet_and_replies_inf
    # def __check_date_type(d1,d2): if (type(d1) or type(d2)) is not type("str"):  # If the type of ite date input
    # is not string it generates exception print("[!] Please make sure the date is a string in this format
    # \"yyyy-mm-dd\" ") raise EXCEPTION("Incorrect date type Exception!") elif (len(d1.split("-")) or len(d2.split(
    # "-")))<2: print("[!] Please make sure the date is a string in this format \"yyyy-mm-dd\" ") raise EXCEPTION(
    # "Incorrect date type Exception!")


if __name__ == "__main__":
     sc = TwitterScraper(from_date="2021-01-01", to_date=str(date.today()),num_tweets=100000)
     dc = sc.scrape_by_user("annieloof")
     print(dc.head())
     print(dc.shape)
