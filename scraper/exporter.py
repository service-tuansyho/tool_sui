import logging
import json
import csv
from datetime import datetime
from pymongo import MongoClient
from config import MONGODB_URI, MONGODB_DB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataExporter:
    def __init__(self):
        try:
            self.client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            self.db = self.client[MONGODB_DB]
            logger.info("Connected to MongoDB for export")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def export_to_json(self, collection_name, filename=None):
        """Export collection to JSON"""
        try:
            if filename is None:
                filename = f"data/{collection_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            collection = self.db[collection_name]
            documents = list(collection.find({}, {"_id": 0}))
            
            # Convert datetime objects to strings
            for doc in documents:
                for key, value in doc.items():
                    if isinstance(value, datetime):
                        doc[key] = value.isoformat()
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(documents, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Exported {len(documents)} documents to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            return None

    def export_to_csv(self, collection_name, filename=None):
        """Export collection to CSV"""
        try:
            if filename is None:
                filename = f"data/{collection_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            collection = self.db[collection_name]
            documents = list(collection.find({}, {"_id": 0}))
            
            if not documents:
                logger.warning(f"No documents found in {collection_name}")
                return None
            
            # Get all keys from all documents
            keys = set()
            for doc in documents:
                keys.update(doc.keys())
            keys = sorted(list(keys))
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                
                for doc in documents:
                    # Convert datetime objects to strings
                    row = {}
                    for key, value in doc.items():
                        if isinstance(value, datetime):
                            row[key] = value.isoformat()
                        elif isinstance(value, dict):
                            row[key] = json.dumps(value)
                        else:
                            row[key] = value
                    writer.writerow(row)
            
            logger.info(f"Exported {len(documents)} documents to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return None

    def export_all(self):
        """Export all collections"""
        logger.info("Exporting all collections...")
        
        results = {
            "reddit_posts_json": self.export_to_json("reddit_posts"),
            "reddit_posts_csv": self.export_to_csv("reddit_posts"),
            "twitter_posts_json": self.export_to_json("twitter_posts"),
            "twitter_posts_csv": self.export_to_csv("twitter_posts"),
        }
        
        logger.info("All exports completed!")
        return results

    def get_statistics(self):
        """Get statistics about collected data"""
        try:
            reddit_count = self.db.reddit_posts.count_documents({})
            twitter_count = self.db.twitter_posts.count_documents({})
            
            reddit_latest = self.db.reddit_posts.find_one(
                sort=[("created_at", -1)]
            )
            twitter_latest = self.db.twitter_posts.find_one(
                sort=[("created_at", -1)]
            )
            
            stats = {
                "total_reddit_posts": reddit_count,
                "total_twitter_posts": twitter_count,
                "total_items": reddit_count + twitter_count,
                "latest_reddit": reddit_latest["created_at"] if reddit_latest else None,
                "latest_twitter": twitter_latest["created_at"] if twitter_latest else None,
            }
            
            logger.info(f"Statistics: {stats}")
            return stats
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return None

    def close(self):
        """Close MongoDB connection"""
        self.client.close()
        logger.info("MongoDB connection closed")


if __name__ == "__main__":
    import sys
    
    exporter = DataExporter()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--json":
            exporter.export_to_json(sys.argv[2] if len(sys.argv) > 2 else "reddit_posts")
        elif sys.argv[1] == "--csv":
            exporter.export_to_csv(sys.argv[2] if len(sys.argv) > 2 else "reddit_posts")
        elif sys.argv[1] == "--all":
            exporter.export_all()
        elif sys.argv[1] == "--stats":
            stats = exporter.get_statistics()
            print(json.dumps(stats, indent=2, default=str))
    else:
        exporter.export_all()
    
    exporter.close()
