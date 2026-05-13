# Quick Start Guide

## 1. Initial Setup

```bash
cd tool/scraper
chmod +x setup.sh
./setup.sh
```

## 2. Get API Credentials

### Reddit API
1. Go to https://www.reddit.com/prefs/apps
2. Scroll to "Developed applications" 
3. Click "Create App" or "Create another app..."
4. Name: "SUI NFT Scraper"
5. Select: "Script"
6. Redirect URI: http://localhost:8000
7. Copy the credentials under your app name

### Twitter/X API (V2)
1. Go to https://developer.twitter.com/
2. Create a new app in your project
3. Go to "Keys and tokens"
4. Generate/copy:
   - API Key (API_KEY)
   - API Secret Key (API_SECRET)
   - Access Token
   - Access Token Secret  
   - Bearer Token (for search)

### MongoDB
- Local: `mongodb://localhost:27017`
- Or create MongoDB Atlas account: https://www.mongodb.com/cloud/atlas

## 3. Configure .env

```bash
nano .env
```

Fill in your credentials:
```
REDDIT_CLIENT_ID=your_id_here
REDDIT_CLIENT_SECRET=your_secret_here
TWITTER_BEARER_TOKEN=your_token_here
MONGODB_URI=mongodb://localhost:27017
```

## 4. Run Scraper

### Test run (one time)
```bash
python main.py --once
```

### Scheduled mode (runs every 6 hours)
```bash
python main.py
```

### Export data
```bash
# Export all to JSON and CSV
python exporter.py --all

# Get statistics
python exporter.py --stats

# Export only Reddit posts to CSV
python exporter.py --csv reddit_posts

# Export only Twitter posts to JSON
python exporter.py --json twitter_posts
```

## 5. Modify Search Terms

Edit `config.py`:

```python
KEYWORDS = [
    'sui blockchain',
    'sui nft',
    'my custom keyword',
]

SUBREDDITS = [
    'suinetwork',
    'nft',
    'mycommunity',
]

TWITTER_HASHTAGS = [
    '#Sui',
    '#MyHashtag',
]
```

## 6. Check Logs

```bash
tail -f logs/scraper.log
```

## 7. Monitor Data

Access MongoDB:
```bash
mongosh

use sui_nft_scraper
db.reddit_posts.countDocuments()
db.twitter_posts.countDocuments()
db.reddit_posts.find().limit(5)
```

## Common Commands

```bash
# Check if MongoDB is running
systemctl status mongod

# Start MongoDB
sudo systemctl start mongod

# Activate venv
source venv/bin/activate

# Check logs
tail -20 logs/scraper.log

# Clear old data (last 30 days only)
# Edit storage.py and add cleanup function
```

## Next Steps

- Integrate with Next.js dashboard
- Add sentiment analysis
- Create analytics charts
- Set up alerts for trending topics
- Export to CSV/Excel for analysis
