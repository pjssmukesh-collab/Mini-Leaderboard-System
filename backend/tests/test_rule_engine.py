import pytest
from app.services.rule_engine import RuleEngine
from app.models.event_rule import EventRule

@pytest.fixture
def engine():
    return RuleEngine()

def test_rule_engine_each_operator(engine):
    rules = [
        EventRule(metric="kills", operator="each", value=None, points=2.0),
        EventRule(metric="headshots", operator="each", value=None, points=5.0)
    ]
    metrics = {"kills": 10, "headshots": 3}
    
    score = engine.calculate_score(rules, metrics)
    assert score == 35.0  # (10 * 2) + (3 * 5)

def test_rule_engine_equals_operator_numeric(engine):
    rules = [
        EventRule(metric="placement", operator="equals", value="1", points=10.0),
        EventRule(metric="placement", operator="equals", value="2", points=5.0)
    ]
    
    # 1st place
    score1 = engine.calculate_score(rules, {"placement": 1})
    assert score1 == 10.0
    
    # 2nd place
    score2 = engine.calculate_score(rules, {"placement": 2})
    assert score2 == 5.0
    
    # 3rd place (no rule)
    score3 = engine.calculate_score(rules, {"placement": 3})
    assert score3 == 0.0

def test_rule_engine_equals_operator_string(engine):
    rules = [
        EventRule(metric="result", operator="equals", value="WIN", points=3.0),
        EventRule(metric="result", operator="equals", value="DRAW", points=1.0),
        EventRule(metric="result", operator="equals", value="LOSS", points=0.0)
    ]
    
    assert engine.calculate_score(rules, {"result": "WIN"}) == 3.0
    assert engine.calculate_score(rules, {"result": "draw"}) == 1.0 # test case insensitivity
    assert engine.calculate_score(rules, {"result": "LOSS"}) == 0.0
    assert engine.calculate_score(rules, {"result": "UNKNOWN"}) == 0.0

def test_rule_engine_greater_than_less_than(engine):
    rules = [
        EventRule(metric="score", operator=">", value="100", points=5.0),
        EventRule(metric="time", operator="<", value="60", points=10.0)
    ]
    
    assert engine.calculate_score(rules, {"score": 101, "time": 59}) == 15.0
    assert engine.calculate_score(rules, {"score": 100, "time": 60}) == 0.0
    assert engine.calculate_score(rules, {"score": 99, "time": 61}) == 0.0

def test_rule_engine_negative_points(engine):
    rules = [
        EventRule(metric="problems_solved", operator="each", value=None, points=10.0),
        EventRule(metric="wrong_submissions", operator="each", value=None, points=-2.0)
    ]
    
    score = engine.calculate_score(rules, {"problems_solved": 5, "wrong_submissions": 2})
    assert score == 46.0  # (5 * 10) + (2 * -2)

def test_rule_engine_missing_metrics(engine):
    rules = [
        EventRule(metric="kills", operator="each", value=None, points=2.0)
    ]
    
    score = engine.calculate_score(rules, {"deaths": 5}) # 'kills' is missing
    assert score == 0.0

def test_rule_engine_mixed_rules_complex(engine):
    rules = [
        EventRule(metric="kills", operator="each", value=None, points=2.0),
        EventRule(metric="placement", operator="equals", value="1", points=20.0),
        EventRule(metric="placement", operator="equals", value="2", points=15.0),
        EventRule(metric="survival_time", operator=">=", value="300", points=5.0)
    ]
    
    metrics = {
        "kills": 8,
        "placement": 2,
        "survival_time": 350
    }
    
    # (8 * 2) + 15 + 5 = 16 + 15 + 5 = 36
    score = engine.calculate_score(rules, metrics)
    assert score == 36.0
