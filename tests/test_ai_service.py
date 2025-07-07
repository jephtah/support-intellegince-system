import pytest
from unittest.mock import patch, AsyncMock
from app.services.ai_service import AIService

@pytest.fixture
def ai_service():
    return AIService()

@pytest.mark.asyncio
async def test_classify_with_openai(ai_service):
    """test openai classification"""
    with patch('app.services.ai_service.openai') as mock_openai:
        # mock openai response
        mock_response = AsyncMock()
        mock_response.choices[0].message.content = '{"category": "technical", "confidence": 0.8, "summary": "Technical issue"}'
        mock_openai.ChatCompletion.acreate.return_value = mock_response
        
        result = await ai_service._classify_with_openai("server crashed")
        
        assert result["category"] == "technical"
        assert result["confidence"] == 0.8
        assert "summary" in result

def test_classify_with_rules(ai_service):
    """test rule-based classification"""
    # test technical
    result = ai_service._classify_with_rules("server crashed with error")
    assert result["category"] == "technical"
    assert result["confidence_score"] > 0
    
    # test billing
    result = ai_service._classify_with_rules("invoice payment issue")
    assert result["category"] == "billing"
    assert result["confidence_score"] > 0
    
    # test general
    result = ai_service._classify_with_rules("need help with information")
    assert result["category"] == "general"
    assert result["confidence_score"] > 0

@pytest.mark.asyncio
async def test_classify_and_summarize_fallback(ai_service):
    """test fallback to rules when openai fails"""
    with patch('app.services.ai_service.openai') as mock_openai:
        mock_openai.ChatCompletion.acreate.side_effect = Exception("API error")
        
        result = await ai_service.classify_and_summarize("server crashed")
        
        # should fallback to rules
        assert "category" in result
        assert "confidence_score" in result
        assert "summary" in result 