import argparse
import logging
from storage import MongoDBStorage
from ai_summarizer import AISummarizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def summarize_posts(limit=100, index=None, post_id=None):
    storage = MongoDBStorage()
    summarizer = AISummarizer()

    if post_id is not None:
        post = storage.get_reddit_post_by_id(post_id)
        posts = [post] if post else []
    elif index is not None:
        post = storage.get_reddit_post_by_index(index)
        posts = [post] if post else []
    else:
        posts = storage.get_reddit_posts(limit=limit)

    logger.info(f'Loaded {len(posts)} posts from MongoDB')

    updated = 0
    for post in posts:
        if not post:
            continue
        if post.get('rewrite'):
            continue

        content = post.get('content') or post.get('title')
        if not content:
            continue

        try:
            rewrite = summarizer.rewrite_text(content)
            if rewrite:
                storage.update_reddit_post_rewrite(post['post_id'], rewrite)
                updated += 1
                logger.info(f"Rewrote post {post['post_id']}")
            else:
                logger.warning(f"Empty rewrite for post {post['post_id']}")
        except Exception as e:
            logger.error(f"Failed to rewrite post {post['post_id']}: {e}")

    storage.close()
    logger.info(f'Finished rewriting {updated} posts')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rewrite Reddit posts from MongoDB using AI')
    parser.add_argument('limit', nargs='?', type=int, default=100,
                        help='Number of most recent posts to rewrite (default: 100)')
    parser.add_argument('--index', type=int,
                        help='One-based index of the post to rewrite by reverse chronological order')
    parser.add_argument('--post_id', type=str,
                        help='Post ID of the Reddit post to rewrite directly')
    args = parser.parse_args()

    if args.post_id:
        summarize_posts(post_id=args.post_id)
    elif args.index is not None:
        if args.index < 1:
            logger.error('Index must be 1 or greater')
        else:
            summarize_posts(index=args.index - 1)
    else:
        summarize_posts(limit=args.limit)
