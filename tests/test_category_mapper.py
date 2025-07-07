import pytest
from app.utils.category_mapper import CategoryMapper

def test_queue_to_category_mapping():
    """test queue to category mapping"""
    mapper = CategoryMapper()
    
    # test technical mappings
    assert mapper.map_queue_to_category("Technical Support") == "technical"
    assert mapper.map_queue_to_category("IT Support") == "technical"
    
    # test billing mapping
    assert mapper.map_queue_to_category("Billing and Payments") == "billing"
    
    # test general mappings
    assert mapper.map_queue_to_category("Customer Service") == "general"
    assert mapper.map_queue_to_category("Product Support") == "general"
    
    # test unknown defaults to general
    assert mapper.map_queue_to_category("Unknown") == "general"

def test_priority_to_confidence():
    """test priority to confidence mapping"""
    mapper = CategoryMapper()
    
    assert mapper.map_priority_to_confidence("Critical") == pytest.approx(0.9)
    assert mapper.map_priority_to_confidence("High") == pytest.approx(0.8)
    assert mapper.map_priority_to_confidence("Medium") == pytest.approx(0.6)
    assert mapper.map_priority_to_confidence("Low") == pytest.approx(0.4)
    
    # test unknown defaults
    assert mapper.map_priority_to_confidence("Unknown") == pytest.approx(0.5)

def test_category_keywords():
    """test category keywords exist"""
    mapper = CategoryMapper()
    keywords = mapper.get_category_keywords()
    
    assert "technical" in keywords
    assert "billing" in keywords
    assert "general" in keywords
    
    # check some expected keywords
    assert "crash" in keywords["technical"]
    assert "invoice" in keywords["billing"]
    assert "help" in keywords["general"] 