# SUI Blockchain & NFT Scraper

Công cụ scraping dữ liệu từ Reddit và X (Twitter) về SUI blockchain và NFT.

## Setup

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình environment variables

Copy file `.env.example` thành `.env` và điền thông tin:

```bash
cp .env.example .env
```

#### Lấy Reddit API credentials:
1. Truy cập https://www.reddit.com/prefs/apps
2. Tạo "Script" app
3. Copy `client_id` và `client_secret`

#### Lấy Twitter/X API credentials:
1. Truy cập https://developer.twitter.com/
2. Tạo project và app
3. Copy các keys và tokens
4. Đảm bảo có quyền access v2 API

#### MongoDB:
- Nếu dùng local: `mongodb://localhost:27017`
- Nếu dùng MongoDB Atlas: Copy connection string từ dashboard

#### Ollama local AI (tuỳ chọn)
- Không cần package Python riêng; scraper dùng `requests` để gọi API của Ollama.
- Cài Ollama local:
  - Linux/macOS: `curl -fsSL https://ollama.com/install.sh | sh`
  - Windows: theo hướng dẫn tại https://ollama.com/docs
- Tải model local:
  - `ollama pull <model-name>`
- Khởi chạy Ollama API server:
  - `ollama serve <model-name>`
  - hoặc `ollama run <model-name> --listen 11434`
- Trong `.env`, đặt:
  - `OLLAMA_URL=http://127.0.0.1:11434`
  - `OLLAMA_MODEL=<model-name>`
- Nếu `OLLAMA_MODEL` được cấu hình, scraper sẽ dùng Ollama local thay vì Google AI.

### 3. Khởi chạy

**Chạy một lần:**
```bash
python main.py --once
```

**Chạy một lần chỉ riêng Twitter:**
```bash
python main.py --once --twitter-only
```

**Chạy scheduler (chạy mỗi N giờ):**
```bash
python main.py
```

## Project Structure

```
scraper/
├── config.py              # Cấu hình chính
├── storage.py             # MongoDB storage
├── reddit_scraper.py      # Reddit scraper
├── twitter_scraper.py     # Twitter scraper
├── main.py                # Entry point
├── requirements.txt       # Dependencies
├── .env.example           # Environment template
├── logs/                  # Log files
└── data/                  # Data exports (optional)
```

## Features

### Reddit Scraper
- Scrape từ các subreddit: r/suinetwork, r/nft, r/cryptocurrency, r/defi
- Tìm kiếm theo keywords
- Lưu: title, content, author, score, comments, URL

### Twitter/X Scraper
- Tìm kiếm tweets theo keywords
- Tìm kiếm theo hashtags (#Sui, #NFT, #Web3)
- Tìm kiếm discussions về NFT trên Sui
- Lưu: text, metrics (likes, retweets, replies), author, timestamp

### Storage
- MongoDB database
- Indexes tự động cho performance
- Duplicate detection (unique IDs)

## Thêm/Sửa Keywords

Chỉnh sửa trong `config.py`:

```python
KEYWORDS = [
    'sui blockchain',
    'sui nft',
    'sui ecosystem',
    # ... thêm keywords khác
]

SUBREDDITS = [
    'suinetwork',
    'nft',
    # ... thêm subreddits
]

TWITTER_HASHTAGS = [
    '#Sui',
    '#NFT',
    # ... thêm hashtags
]
```

## Logs

Logs được lưu trong `logs/scraper.log` và in ra console.

## Troubleshooting

**MongoDB connection failed:**
- Kiểm tra MongoDB service đang chạy: `systemctl status mongod`
- Hoặc dùng MongoDB Atlas: update `MONGODB_URI` trong `.env`

**Reddit/Twitter API errors:**
- Kiểm tra credentials trong `.env`
- Kiểm tra API rate limits
- Xem logs chi tiết trong `logs/scraper.log`

## Next Steps

- [ ] Thêm data export (CSV, JSON)
- [ ] Dashboard để xem data
- [ ] Sentiment analysis
- [ ] Trending topics detection
- [ ] Integrate vào Next.js app

## viết lại post
- python summarize_reddit_posts.py --post_id <POST_ID>