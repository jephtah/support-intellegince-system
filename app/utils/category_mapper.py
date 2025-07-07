from typing import Dict, List

class CategoryMapper:
    QUEUE_TO_CATEGORY: Dict[str, str] = {
        "Technical Support": "technical",
        "IT Support": "technical",
        "Billing and Payments": "billing",
        "Customer Service": "general",
        "Product Support": "general",
        "General Inquiry": "general",
        "Sales": "general"
    }
    
    PRIORITY_TO_CONFIDENCE: Dict[str, float] = {
        "Critical": 0.9,
        "High": 0.8,
        "Medium": 0.6,
        "Low": 0.4
    }
    
    @classmethod
    def map_queue_to_category(cls, queue: str) -> str:
        return cls.QUEUE_TO_CATEGORY.get(queue, "general")
    
    @classmethod
    def map_priority_to_confidence(cls, priority: str) -> float:
        return cls.PRIORITY_TO_CONFIDENCE.get(priority, 0.5)
    
    @classmethod
    def get_category_keywords(cls) -> Dict[str, List[str]]:
        return {
            "technical": [
                "crash", "error", "bug", "failed", "broken", "not working",
                "server", "database", "API", "code", "software", "system"
            ],
            "billing": [
                "invoice", "payment", "charge", "bill", "refund", "subscription",
                "pricing", "cost", "fee", "billing"
            ],
            "general": [
                "help", "support", "question", "how to", "information"
            ]
        }