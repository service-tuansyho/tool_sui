import logging
from datetime import datetime, timedelta
import snscrape.modules.twitter as sntwitter
from config import (
    KEYWORDS,
    TWITTER_HASHTAGS,
    MAX_RESULTS_PER_RUN
)
from storage import MongoDBStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwitterScraper:
    def __init__(self):
        try:
            self.storage = MongoDBStorage()
            logger.info("Twitter scraper initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter scraper: {e}")
            raise

    def search_tweets(self, query):
        """Search tweets by query"""
        try:
            tweets_saved = 0
            cutoff = datetime.utcnow() - timedelta(days=7)

            for tweet in sntwitter.TwitterSearchScraper(query).get_items():
                if tweets_saved >= MAX_RESULTS_PER_RUN:
                    break

                if tweet.date and tweet.date < cutoff:
                    continue

                tweet_data = {
                    "id": tweet.id,
                    "text": tweet.content,
                    "created_at": tweet.date,
                    "author_id": tweet.user.username if tweet.user else None,
                    "public_metrics": {
                        "like_count": getattr(tweet, "likeCount", 0),
                        "retweet_count": getattr(tweet, "retweetCount", 0),
                        "reply_count": getattr(tweet, "replyCount", 0),
                    }
                }

                if self.storage.save_twitter_post(tweet_data):
                    tweets_saved += 1

            logger.info(f"Saved {tweets_saved} tweets for query: {query}")
            return tweets_saved
        except Exception as e:
            logger.error(f"Error searching tweets for query '{query}': {e}")
            return 0

    def search_by_keywords(self):
        """Search tweets by keywords and hashtags"""
        total_saved = 0

        for keyword in KEYWORDS:
            query = f'"{keyword}" -is:retweet lang:en'
            total_saved += self.search_tweets(query)

        for hashtag in TWITTER_HASHTAGS:
            query = f'{hashtag} -is:retweet lang:en'
            total_saved += self.search_tweets(query)

        return total_saved

    def search_nft_discussions(self):
        """Search for NFT-related discussions"""
        try:
            tweets_saved = 0
            query = '(NFT OR "non-fungible token") (Sui OR SUI OR "Sui Network") -is:retweet lang:en'
            cutoff = datetime.utcnow() - timedelta(days=7)

            for tweet in sntwitter.TwitterSearchScraper(query).get_items():
                if tweets_saved >= MAX_RESULTS_PER_RUN:
                    break

                if tweet.date and tweet.date < cutoff:
                    continue

                tweet_data = {
                    "id": tweet.id,
                    "text": tweet.content,
                    "created_at": tweet.date,
                    "author_id": tweet.user.username if tweet.user else None,
                    "public_metrics": {
                        "like_count": getattr(tweet, "likeCount", 0),
                        "retweet_count": getattr(tweet, "retweetCount", 0),
                        "reply_count": getattr(tweet, "replyCount", 0),
                    }
                }

                if self.storage.save_twitter_post(tweet_data):
                    tweets_saved += 1

            logger.info(f"Saved {tweets_saved} NFT-related tweets")
            return tweets_saved
        except Exception as e:
            logger.error(f"Error searching NFT tweets: {e}")
            return 0

    def run(self):
        """Run the scraper"""
        logger.info("Starting Twitter scraper...")

        total_tweets = 0
        total_tweets += self.search_by_keywords()
        total_tweets += self.search_nft_discussions()

        logger.info(f"Twitter scraping completed. Total tweets saved: {total_tweets}")
        self.storage.close()
        return total_tweets


if __name__ == "__main__":
    scraper = TwitterScraper()
    scraper.run()
