import logging
import requests
from datetime import datetime
from config import (
    KEYWORDS,
    SUBREDDITS,
    MAX_RESULTS_PER_RUN
)
from storage import MongoDBStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedditScraper:
    def __init__(self):
        try:
            self.storage = MongoDBStorage()
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
            }
            logger.info("Reddit scraper initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Reddit scraper: {e}")
            raise

    def scrape_subreddit(self, subreddit_name):
        """Scrape posts from a specific subreddit"""
        try:
            posts_saved = 0
            url = f'https://www.reddit.com/r/{subreddit_name}/new.json'
            
            params = {'limit': 100}
            after = None
            
            while posts_saved < MAX_RESULTS_PER_RUN:
                if after:
                    params['after'] = after
                
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                if response.status_code != 200:
                    logger.error(f"Failed to fetch r/{subreddit_name}: {response.status_code}")
                    break
                
                data = response.json()
                posts = data.get('data', {}).get('children', [])
                
                if not posts:
                    break
                
                for post in posts:
                    if posts_saved >= MAX_RESULTS_PER_RUN:
                        break
                    
                    post_data = post.get('data', {})
                    save_data = {
                        "id": post_data.get('id'),
                        "title": post_data.get('title'),
                        "content": post_data.get('selftext'),
                        "author": post_data.get('author'),
                        "subreddit": post_data.get('subreddit'),
                        "url": post_data.get('url'),
                        "score": post_data.get('score', 0),
                        "comments": post_data.get('num_comments', 0),
                        "created_utc": post_data.get('created_utc'),
                    }
                    
                    if self.storage.save_reddit_post(save_data):
                        posts_saved += 1
                
                after = data.get('data', {}).get('after')
                if not after:
                    break
            
            logger.info(f"Saved {posts_saved} posts from r/{subreddit_name}")
            return posts_saved
        except Exception as e:
            logger.error(f"Error scraping subreddit {subreddit_name}: {e}")
            return 0

    def scrape_by_keywords(self):
        """Search and scrape posts by keywords"""
        total_saved = 0
        
        for keyword in KEYWORDS:
            try:
                posts_saved = 0
                url = f'https://www.reddit.com/search.json'
                
                # Build search query with subreddit filter
                search_query = keyword
                if SUBREDDITS:
                    subreddit_filter = '+'.join(SUBREDDITS)
                    search_query = f'{keyword} subreddit:{subreddit_filter}'
                
                params = {
                    'q': search_query,
                    'type': 'link',
                    'sort': 'new',
                    'limit': 100
                }
                
                after = None
                
                while posts_saved < MAX_RESULTS_PER_RUN:
                    if after:
                        params['after'] = after
                    
                    response = requests.get(url, headers=self.headers, params=params, timeout=10)
                    if response.status_code != 200:
                        logger.error(f"Failed to search for '{keyword}': {response.status_code}")
                        break
                    
                    data = response.json()
                    posts = data.get('data', {}).get('children', [])
                    
                    if not posts:
                        break
                    
                    for post in posts:
                        if posts_saved >= MAX_RESULTS_PER_RUN:
                            break
                        
                        post_data = post.get('data', {})
                        save_data = {
                            "id": post_data.get('id'),
                            "title": post_data.get('title'),
                            "content": post_data.get('selftext'),
                            "author": post_data.get('author'),
                            "subreddit": post_data.get('subreddit'),
                            "url": post_data.get('url'),
                            "score": post_data.get('score', 0),
                            "comments": post_data.get('num_comments', 0),
                            "created_utc": post_data.get('created_utc'),
                        }
                        
                        if self.storage.save_reddit_post(save_data):
                            posts_saved += 1
                    
                    after = data.get('data', {}).get('after')
                    if not after:
                        break
                
                logger.info(f"Found {posts_saved} posts for keyword: {keyword}")
                total_saved += posts_saved
            except Exception as e:
                logger.error(f"Error searching for keyword '{keyword}': {e}")
        
        return total_saved

    def run(self):
        """Run the scraper"""
        logger.info("Starting Reddit scraper...")
        
        total_posts = 0
        
        # Scrape popular subreddits
        for subreddit in SUBREDDITS:
            total_posts += self.scrape_subreddit(subreddit)
        
        # Search by keywords
        total_posts += self.scrape_by_keywords()
        
        logger.info(f"Reddit scraping completed. Total posts saved: {total_posts}")
        self.storage.close()
        return total_posts


if __name__ == "__main__":
    scraper = RedditScraper()
    scraper.run()
