import logging
from datetime import datetime
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import MONGODB_URI, MONGODB_DB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBStorage:
    def __init__(self):
        try:
            self.client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client[MONGODB_DB]
            logger.info("Connected to MongoDB successfully")
            self._create_indexes()
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def _create_indexes(self):
        """Create indexes for better query performance"""
        # Reddit posts collection
        self.db.reddit_posts.create_index([("post_id", ASCENDING)], unique=True)
        self.db.reddit_posts.create_index([("created_at", ASCENDING)])
        self.db.reddit_posts.create_index([("subreddit", ASCENDING)])
        
        # Twitter posts collection
        self.db.twitter_posts.create_index([("tweet_id", ASCENDING)], unique=True)
        self.db.twitter_posts.create_index([("created_at", ASCENDING)])
        
        logger.info("Indexes created successfully")

    def save_reddit_post(self, post_data):
        """Save Reddit post to MongoDB"""
        try:
            post = {
                "post_id": post_data.get("id"),
                "title": post_data.get("title"),
                "content": post_data.get("content"),
                "author": post_data.get("author"),
                "subreddit": post_data.get("subreddit"),
                "url": post_data.get("url"),
                "score": post_data.get("score"),
                "comments": post_data.get("comments"),
                "created_at": datetime.fromtimestamp(post_data.get("created_utc")),
                "scraped_at": datetime.utcnow(),
                "source": "reddit"
            }
            
            self.db.reddit_posts.insert_one(post)
            logger.info(f"Saved Reddit post: {post_data.get('id')}")
            return True
        except Exception as e:
            logger.error(f"Error saving Reddit post: {e}")
            return False

    def save_twitter_post(self, tweet_data):
        """Save Twitter post to MongoDB"""
        try:
            tweet = {
                "tweet_id": tweet_data.get("id"),
                "author": tweet_data.get("author_id"),
                "text": tweet_data.get("text"),
                "likes": tweet_data.get("public_metrics", {}).get("like_count", 0),
                "retweets": tweet_data.get("public_metrics", {}).get("retweet_count", 0),
                "replies": tweet_data.get("public_metrics", {}).get("reply_count", 0),
                "created_at": tweet_data.get("created_at"),
                "scraped_at": datetime.utcnow(),
                "source": "twitter"
            }
            
            self.db.twitter_posts.insert_one(tweet)
            logger.info(f"Saved Twitter post: {tweet_data.get('id')}")
            return True
        except Exception as e:
            logger.error(f"Error saving Twitter post: {e}")
            return False

    def get_reddit_posts(self, limit=100):
        """Get recent Reddit posts"""
        return list(self.db.reddit_posts.find().sort("created_at", -1).limit(limit))

    def get_reddit_post_by_index(self, index):
        """Get a single Reddit post by its zero-based index in reverse chronological order"""
        if index < 0:
            return None

        cursor = self.db.reddit_posts.find().sort("created_at", -1).skip(index).limit(1)
        return next(cursor, None)
    def get_reddit_post_by_id(self, post_id):
        """Get a single Reddit post by its post_id"""
        return self.db.reddit_posts.find_one({"post_id": post_id})
    def update_reddit_post_rewrite(self, post_id, rewrite):
        """Update a Reddit post with an AI rewrite"""
        try:
            result = self.db.reddit_posts.update_one(
                {"post_id": post_id},
                {"$set": {"rewrite": rewrite}}
            )
            return result.modified_count == 1
        except Exception as e:
            logger.error(f"Error updating rewrite for {post_id}: {e}")
            return False

    def get_twitter_posts(self, limit=100):
        """Get recent Twitter posts"""
        return list(self.db.twitter_posts.find().sort("created_at", -1).limit(limit))

    def get_posts_by_date_range(self, start_date, end_date):
        """Get posts within a date range"""
        query = {"created_at": {"$gte": start_date, "$lte": end_date}}
        reddit = list(self.db.reddit_posts.find(query))
        twitter = list(self.db.twitter_posts.find(query))
        return {"reddit": reddit, "twitter": twitter}

    def close(self):
        """Close MongoDB connection"""
        self.client.close()
        logger.info("MongoDB connection closed")
