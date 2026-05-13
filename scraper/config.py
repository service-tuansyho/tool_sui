import os
from dotenv import load_dotenv

load_dotenv()

# Reddit
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'SUI-NFT-Scraper/1.0')

# Twitter/X
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

# MongoDB
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'sui_nft_scraper')

# Google AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_AI_MODEL = os.getenv('GOOGLE_AI_MODEL', 'gemini-2.5-flash')

# Ollama local AI
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://127.0.0.1:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL')

# Scraper Settings
SCRAPE_INTERVAL_HOURS = int(os.getenv('SCRAPE_INTERVAL_HOURS', '6'))
MAX_RESULTS_PER_RUN = int(os.getenv('MAX_RESULTS_PER_RUN', '100'))

# Keywords to search
KEYWORDS = [
    'sui blockchain',
    'sui nft',
    'sui ecosystem',
    'move language',
    'mysten labs',
]

SUBREDDITS = [
    'suinetwork',
    'nft',
    'cryptocurrency',
    'defi',
]

TWITTER_HASHTAGS = [
    '#Sui',
    '#SuiNetwork',
    '#NFT',
    '#Web3',
]
