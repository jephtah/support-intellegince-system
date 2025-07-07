import asyncio
from datasets import load_dataset
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.support_ticket import SupportTicket
from app.utils.category_mapper import CategoryMapper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_database():
    """seeding db with sample data"""
    
    Base.metadata.create_all(bind=engine)
    
    # load dataset
    logger.info("loading dataset...")
    try:
        dataset = load_dataset("tobi-bueck/customer-support-tickets", split="train")
        logger.info(f"loaded {len(dataset)} records")
    except Exception as e:
        logger.error(f"failed to load dataset: {str(e)}")
        return
    
    # filter english
    english_data = dataset.filter(lambda x: x.get("language") == "en")
    logger.info(f"filtered to {len(english_data)} english records")
    
    db = SessionLocal()
    try:
        category_mapper = CategoryMapper()
        processed = 0
        
        # process in batches
        batch_size = 100
        for i in range(0, len(english_data), batch_size):
            batch = english_data[i:i+batch_size]
            
            for record in batch:
                ticket = SupportTicket(
                    subject=record.get("subject"),
                    body=record.get("body", ""),
                    original_queue=record.get("queue"),
                    original_priority=record.get("priority"),
                    language=record.get("language", "en"),
                    category=category_mapper.map_queue_to_category(record.get("queue", "")),
                    confidence_score=category_mapper.map_priority_to_confidence(record.get("priority", "")),
                    summary=record.get("answer", "")[:500] if record.get("answer") else None,
                    tag_1=record.get("tag_1"),
                    tag_2=record.get("tag_2"),
                    tag_3=record.get("tag_3"),
                    tag_4=record.get("tag_4"),
                    tag_5=record.get("tag_5"),
                    tag_6=record.get("tag_6"),
                    tag_7=record.get("tag_7"),
                    tag_8=record.get("tag_8"),
                    is_processed=True
                )
                
                db.add(ticket)
                processed += 1
            
            db.commit()
            logger.info(f"processed {processed} records...")
            
            # limit for demo
            if processed >= 1000:
                logger.info("reached limit of 1000 records")
                break
                
        logger.info(f"seeding done. total: {processed}")
        
    except Exception as e:
        logger.error(f"seeding failed: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()