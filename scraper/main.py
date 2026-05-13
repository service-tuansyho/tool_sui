import logging
import schedule
import time
from datetime import datetime
from config import SCRAPE_INTERVAL_HOURS
from reddit_scraper import RedditScraper
from twitter_scraper import TwitterScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_scrapers(run_reddit=True, run_twitter=True):
    """Run selected scrapers."""
    logger.info("=" * 50)
    logger.info(f"Starting scraping job at {datetime.now()}")
    logger.info("=" * 50)
    
    try:
        reddit_posts = 0
        twitter_tweets = 0

        if run_reddit:
            logger.info("Running Reddit scraper...")
            reddit_scraper = RedditScraper()
            reddit_posts = reddit_scraper.run()

        if run_twitter:
            logger.info("Running Twitter scraper...")
            twitter_scraper = TwitterScraper()
            twitter_tweets = twitter_scraper.run()

        logger.info("=" * 50)
        logger.info("Scraping job completed!")
        logger.info(f"Reddit posts saved: {reddit_posts}")
        logger.info(f"Twitter tweets saved: {twitter_tweets}")
        logger.info(f"Total data points: {reddit_posts + twitter_tweets}")
        logger.info("=" * 50)
    except Exception as e:
        logger.error(f"Error in scraping job: {e}")


def start_scheduler(run_reddit=True, run_twitter=True):
    """Start the scheduler for periodic scraping"""
    schedule.every(SCRAPE_INTERVAL_HOURS).hours.do(lambda: run_scrapers(run_reddit, run_twitter))
    
    logger.info(f"Scheduler started. Running scrapers every {SCRAPE_INTERVAL_HOURS} hours")
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)

def run_once(run_reddit=True, run_twitter=True):
    """Run scrapers once"""
    run_scrapers(run_reddit, run_twitter)

if __name__ == "__main__":
    import sys

    once = "--once" in sys.argv
    only_twitter = "--twitter-only" in sys.argv
    only_reddit = "--reddit-only" in sys.argv

    if only_twitter and only_reddit:
        logger.error("Cannot use both --twitter-only and --reddit-only")
        sys.exit(1)

    run_reddit = not only_twitter
    run_twitter = not only_reddit

    if once:
        logger.info("Running scraper once...")
        run_once(run_reddit, run_twitter)
    else:
        logger.info("Starting scraper in scheduled mode...")
        start_scheduler(run_reddit, run_twitter)
