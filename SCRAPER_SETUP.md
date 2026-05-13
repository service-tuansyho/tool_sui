# 🚀 SUI NFT Scraper - Complete Setup Guide

## 📋 Project Structure

```
tool/
├── scraper/
│   ├── config.py              # Configuration & keywords
│   ├── storage.py             # MongoDB storage operations
│   ├── reddit_scraper.py      # Reddit scraper logic
│   ├── twitter_scraper.py     # Twitter/X scraper logic
│   ├── main.py                # Main entry point (scheduler)
│   ├── exporter.py            # Data export utilities
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment template
│   ├── .gitignore             # Git ignore file
│   ├── setup.sh               # Automated setup script
│   ├── README.md              # Full documentation
│   ├── QUICKSTART.md          # Quick start guide
│   ├── logs/                  # Log directory
│   └── data/                  # Data exports directory
├── package.json               # Node.js scripts
├── run-scraper.js             # Node.js wrapper
└── ...
```

---

## 🛠️ Step-by-Step Setup

### **Step 1: Navigate to Tool Directory**
```bash
cd /home/tuansyho/Desktop/carnobon_code/tool
```

### **Step 2: Run Setup Script**
```bash
chmod +x scraper/setup.sh
bash scraper/setup.sh
```

The setup script will:
- ✅ Check Python 3 installation
- ✅ Create Python virtual environment
- ✅ Install all dependencies
- ✅ Create `.env` file from template

### **Step 3: Get API Credentials**

#### 📱 Reddit API
1. Go to: https://www.reddit.com/prefs/apps
2. Click "Create another app"
3. Fill in:
   - **App name**: SUI NFT Scraper
   - **App type**: Select "Script"
   - **Redirect URI**: http://localhost:8000
4. Copy your credentials (shown under the app name):
   ```
   REDDIT_CLIENT_ID=<your_id>
   REDDIT_CLIENT_SECRET=<your_secret>
   ```

#### 🐦 Twitter/X API v2
1. Go to: https://developer.twitter.com/
2. Create/select a project and app
3. Go to "Keys and tokens" tab
4. Copy:
   ```
   TWITTER_API_KEY=<your_api_key>
   TWITTER_API_SECRET=<your_api_secret>
   TWITTER_ACCESS_TOKEN=<your_access_token>
   TWITTER_ACCESS_TOKEN_SECRET=<your_token_secret>
   TWITTER_BEARER_TOKEN=<your_bearer_token>
   ```

#### 🗄️ MongoDB
- **Local MongoDB**: `mongodb://localhost:27017`
- **MongoDB Atlas** (cloud):
  1. Create account: https://www.mongodb.com/cloud/atlas
  2. Create free cluster
  3. Copy connection string:
     ```
     mongodb+srv://username:password@cluster.mongodb.net/
     ```

### **Step 4: Configure Environment**
```bash
cd scraper
nano .env
```

Fill in your credentials:
```env
# Reddit API
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=SUI-NFT-Scraper/1.0

# Twitter API
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here

# MongoDB
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=sui_nft_scraper

# Scraper Settings
SCRAPE_INTERVAL_HOURS=6
MAX_RESULTS_PER_RUN=100
```

Save and exit: `Ctrl+X`, then `Y`, then `Enter`

---

## 🚀 Running the Scraper

### **Option 1: Single Run (Test)**
```bash
python main.py --once
```
This will scrape once and exit.

### **Option 2: Scheduled Mode**
```bash
python main.py
```
Runs automatically every 6 hours (configurable in `.env`)

### **Option 3: From Node.js**
```bash
# In the tool/ directory
node run-scraper.js --once
node run-scraper.js  # scheduled mode
```

### **Option 4: Export Data**
```bash
# Export all collections to JSON and CSV
python exporter.py --all

# Get statistics
python exporter.py --stats

# Export specific collection
python exporter.py --json reddit_posts
python exporter.py --csv twitter_posts
```

---

## 📊 What Gets Scraped

### Reddit
- Subreddits: `r/suinetwork`, `r/nft`, `r/cryptocurrency`, `r/defi`
- Keywords: "sui blockchain", "sui nft", "sui ecosystem", etc.
- Data collected:
  - Post title & content
  - Author & subreddit
  - Score & comments count
  - Creation date

### Twitter/X
- Hashtags: `#Sui`, `#SuiNetwork`, `#NFT`, `#Web3`
- Keywords search
- NFT discussions
- Data collected:
  - Tweet text
  - Author ID
  - Likes, retweets, replies
  - Creation date

---

## 🔧 Customization

### Add More Keywords/Topics

Edit `config.py`:
```python
KEYWORDS = [
    'sui blockchain',
    'sui nft',
    'sui ecosystem',
    'move language',        # Add new
    'mysten labs',         # Add new
]

SUBREDDITS = [
    'suinetwork',
    'nft',
    'cryptocurrency',
    'defi',
    'mycommunity',        # Add new
]

TWITTER_HASHTAGS = [
    '#Sui',
    '#SuiNetwork',
    '#NFT',
    '#MyHashtag',        # Add new
]
```

### Change Scrape Interval

Edit `.env`:
```env
SCRAPE_INTERVAL_HOURS=6    # Change to desired hours
MAX_RESULTS_PER_RUN=100    # Change max results
```

---

## 📋 Monitoring & Logs

### View Real-time Logs
```bash
tail -f scraper/logs/scraper.log
```

### View Last 50 lines
```bash
tail -50 scraper/logs/scraper.log
```

### Check MongoDB Data
```bash
mongosh

use sui_nft_scraper
db.reddit_posts.countDocuments()
db.twitter_posts.countDocuments()
db.reddit_posts.find().limit(5).pretty()
```

---

## ⚡ Troubleshooting

### MongoDB Connection Failed
```bash
# Check if MongoDB is running
systemctl status mongod

# Start MongoDB
sudo systemctl start mongod

# Or use MongoDB Atlas instead (free cloud option)
```

### Reddit/Twitter API Errors
- ✅ Verify credentials in `.env`
- ✅ Check API rate limits
- ✅ Review logs: `tail -f scraper/logs/scraper.log`
- ✅ Ensure API keys have correct permissions

### Python Virtual Environment Issues
```bash
# Deactivate current venv
deactivate

# Remove venv
rm -rf venv/

# Recreate
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Import Errors
```bash
# Make sure you're in the venv
source venv/bin/activate

# Reinstall requirements
pip install --upgrade -r requirements.txt
```

---

## 📈 Next Steps

1. **Dashboard**: Create Next.js dashboard to display scraped data
2. **Sentiment Analysis**: Analyze sentiment of posts/tweets
3. **Trending Topics**: Detect trending topics automatically
4. **Alerts**: Set up notifications for trending keywords
5. **API Endpoint**: Create REST API to query data
6. **Analytics**: Generate charts and insights

---

## 📚 File Descriptions

| File | Purpose |
|------|---------|
| `config.py` | Configuration, keywords, credentials |
| `storage.py` | MongoDB operations & data storage |
| `reddit_scraper.py` | Reddit scraping logic |
| `twitter_scraper.py` | Twitter/X scraping logic |
| `main.py` | Main entry point & scheduler |
| `exporter.py` | Data export to JSON/CSV |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment template |
| `setup.sh` | Automated setup script |

---

## 💡 Tips & Best Practices

1. **Start with `--once` flag** to test before scheduling
2. **Monitor logs** during first runs to catch errors
3. **Use MongoDB Atlas** for easy cloud storage (free tier available)
4. **Export data regularly** for backup and analysis
5. **Adjust `MAX_RESULTS_PER_RUN`** based on your needs
6. **Review keywords** periodically and update them

---

## 📞 Support

For issues, check:
- [QUICKSTART.md](./QUICKSTART.md) - Quick commands
- [README.md](./README.md) - Full documentation
- `scraper/logs/scraper.log` - Error logs
- API documentation links in this guide

Good luck! 🚀
