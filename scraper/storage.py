import logging
import re
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
        # Posts collection
        self.db.posts.create_index([("post_id", ASCENDING)], unique=True)
        self.db.posts.create_index([("slug", ASCENDING)], unique=True)
        self.db.posts.create_index([("created_at", ASCENDING)])
        self.db.posts.create_index([("source", ASCENDING)])
        self.db.posts.create_index([("source", ASCENDING), ("created_at", ASCENDING)])
        
        logger.info("Indexes created successfully")

    def _slugify(self, text: str) -> str:
        """Convert a title or text into a URL-friendly slug."""
        if not text:
            return ""

        slug = text.strip().lower()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[\s_-]+", "-", slug)
        slug = re.sub(r"^-+|-+$", "", slug)
        return slug

    def _generate_unique_slug(self, text: str, fallback: str) -> str:
        """Generate a unique slug within the posts collection."""
        base_slug = self._slugify(text) or self._slugify(fallback) or "post"
        slug = base_slug
        counter = 1

        while self.db.posts.find_one({"slug": slug}):
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def save_post(self, post_data):
        """Save post (Reddit or Twitter) to MongoDB with source field"""
        try:
            source = post_data.get("source", "unknown")
            
            # Get content based on source
            if source == "reddit":
                content = post_data.get("content", "").strip()
                if not content:
                    logger.info(f"Skipping Reddit post {post_data.get('id')} - no content")
                    return False
                
                slug = self._generate_unique_slug(post_data.get("title"), post_data.get("id"))
                post = {
                    "post_id": post_data.get("id"),
                    "source": "reddit",
                    "title": post_data.get("title"),
                    "slug": slug,
                    "content": content,
                    "author": post_data.get("author"),
                    "subreddit": post_data.get("subreddit"),
                    "url": post_data.get("url"),
                    "score": post_data.get("score"),
                    "comments": post_data.get("comments"),
                    "created_at": datetime.fromtimestamp(post_data.get("created_utc")),
                    "scraped_at": datetime.utcnow(),
                    "publish": "not publish",
                }
                logger.info(f"Saved Reddit post: {post_data.get('id')}")
                
            elif source == "twitter":
                text = post_data.get("text", "").strip()
                if not text:
                    logger.info(f"Skipping Twitter post {post_data.get('id')} - no content")
                    return False
                
                slug = self._generate_unique_slug(post_data.get("title") or text, post_data.get("id"))
                post = {
                    "post_id": post_data.get("id"),
                    "source": "twitter",
                    "slug": slug,
                    "author": post_data.get("author_id"),
                    "content": text,
                    "likes": post_data.get("public_metrics", {}).get("like_count", 0),
                    "retweets": post_data.get("public_metrics", {}).get("retweet_count", 0),
                    "replies": post_data.get("public_metrics", {}).get("reply_count", 0),
                    "created_at": post_data.get("created_at"),
                    "scraped_at": datetime.utcnow(),
                    "publish": "not publish",
                }
                logger.info(f"Saved Twitter post: {post_data.get('id')}")
            else:
                logger.error(f"Unknown source: {source}")
                return False
            
            self.db.posts.insert_one(post)
            return True
        except Exception as e:
            logger.error(f"Error saving post: {e}")
            return False

    def save_reddit_post(self, post_data):
        """Save Reddit post to MongoDB (deprecated - use save_post instead)"""
        post_data["source"] = "reddit"
        return self.save_post(post_data)

    def save_twitter_post(self, tweet_data):
        """Save Twitter post to MongoDB (deprecated - use save_post instead)"""
        tweet_data["source"] = "twitter"
        return self.save_post(tweet_data)

    def get_posts(self, source=None, limit=100):
        """Get recent posts, optionally filtered by source"""
        if source:
            return list(self.db.posts.find({"source": source}).sort("created_at", -1).limit(limit))
        return list(self.db.posts.find().sort("created_at", -1).limit(limit))

    def get_reddit_posts(self, limit=100):
        """Get recent Reddit posts (deprecated - use get_posts instead)"""
        return self.get_posts(source="reddit", limit=limit)

    def get_twitter_posts(self, limit=100):
        """Get recent Twitter posts (deprecated - use get_posts instead)"""
        return self.get_posts(source="twitter", limit=limit)

    def get_post_by_index(self, index, source=None):
        """Get a single post by its zero-based index in reverse chronological order"""
        if index < 0:
            return None

        query = {"source": source} if source else {}
        cursor = self.db.posts.find(query).sort("created_at", -1).skip(index).limit(1)
        return next(cursor, None)

    def get_reddit_post_by_index(self, index):
        """Get a single Reddit post by its zero-based index (deprecated - use get_post_by_index instead)"""
        return self.get_post_by_index(index, source="reddit")
    def get_post_by_id(self, post_id):
        """Get a single post by its post_id"""
        return self.db.posts.find_one({"post_id": post_id})

    def get_reddit_post_by_id(self, post_id):
        """Get a single Reddit post by its post_id (deprecated - use get_post_by_id instead)"""
        return self.get_post_by_id(post_id)

    def update_post_rewrite(self, post_id, rewrite):
        """Update a post with an AI rewrite"""
        try:
            result = self.db.posts.update_one(
                {"post_id": post_id},
                {"$set": {"rewrite": rewrite}}
            )
            return result.modified_count == 1
        except Exception as e:
            logger.error(f"Error updating rewrite for {post_id}: {e}")
            return False

    def update_reddit_post_rewrite(self, post_id, rewrite):
        """Update a Reddit post with an AI rewrite (deprecated - use update_post_rewrite instead)"""
        return self.update_post_rewrite(post_id, rewrite)

    def close(self):
        """Close MongoDB connection"""
        self.client.close()
        logger.info("MongoDB connection closed")
