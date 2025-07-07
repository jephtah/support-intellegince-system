import openai
from typing import Dict, Optional
from app.config import settings
from app.utils.category_mapper import CategoryMapper
import logging

logger = logging.getLogger(__name__)

class AIService:
    """ai service for classification and summary"""

    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        self.category_mapper = CategoryMapper()


    async def classify_and_summarize(self, text: str, subject: Optional[str] = None) -> Dict:
        """classify and summarize text"""
        try:
            # prep text
            full_text = f"Subject: {subject}\n\nBody: {text}" if subject else text

            # try openai first
            if settings.OPENAI_API_KEY:
                return await self._classify_with_openai(full_text)
            else:
                logger.warning("no openai key, using rules")
                return self._classify_with_rules(full_text)
        except Exception as e:
            logger.error(f"classification error: {str(e)}")
            return self._classify_with_rules(full_text)
            
        
    async def _classify_with_openai(self, text: str) -> Dict:
        """use openai api"""
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "classify this support request as technical, billing, or general. technical = software/hardware issues, billing = payment/invoice stuff, general = everything else. also give a short summary."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                max_tokens=150,
                temperature=0.3,
            )

            import json
            # TODO: handle json parsing errors better
            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            logger.error(f"openai failed: {str(e)}")
            # TODO: add metrics for ai failures
            return self._classify_with_rules(text)

    def _classify_with_rules(self, text: str) -> Dict:
        """rule based fallback"""
        text_lower = text.lower()
        category_keywords = self.category_mapper.category_keywords()

        # score categories
        scores = {}
        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword.lower() in text_lower)
            scores[category] = score

        # get best category
        if not scores or max(scores.values()) == 0:
            category = "general"
            confidence = 0.3
        else:
            category = max(scores, key=scores.get)
            max_score = scores[category]
            # scale confidence
            confidence = min(0.9, 0.4 + (max_score * 0.1))

        # make summary
        summary = f"This request is classified as {category} with a confidence score of {confidence:.2f}."

        return {
            "category": category,
            "confidence_score": confidence,
            "summary": summary,
        }
        
