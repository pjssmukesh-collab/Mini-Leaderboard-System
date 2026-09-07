import re
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.event_rule import EventRule

logger = logging.getLogger(__name__)

def normalize_metric_name(name: str) -> str:
    if not name:
        return ""
    # Split camelCase
    s = re.sub(r'([a-z])([A-Z])', r'\1 \2', str(name))
    # Replace non-alphanumeric with space
    s = re.sub(r'[^a-zA-Z0-9]+', ' ', s).strip().lower()
    # Normalize simple plurals (e.g., 'submissions' -> 'submission', 'problems' -> 'problem')
    words = [w[:-1] if len(w) > 3 and w.endswith('s') and not w.endswith('ss') else w for w in s.split()]
    return " ".join(words)

class RuleEngine:
    def _find_metric_val(self, rule_metric: str, metrics: Dict[str, Any]) -> Any:
        # 1. Exact match
        if rule_metric in metrics:
            return metrics[rule_metric]
        
        # 2. Case-insensitive / normalized match (e.g. 'Problems Solved' vs 'problems_solved')
        norm_rule = normalize_metric_name(rule_metric)
        norm_metrics = {normalize_metric_name(k): v for k, v in metrics.items()}
        
        if norm_rule in norm_metrics:
            return norm_metrics[norm_rule]
            
        # 3. Partial / substring match fallback
        for k, v in norm_metrics.items():
            if norm_rule and (norm_rule in k or k in norm_rule):
                return v
                
        return None

    def evaluate_metrics(self, db: Session, event_id: int, metrics: Dict[str, Any]) -> float:
        """
        Loads rules for an event and calculates the total score based on the provided metrics.
        """
        # Load rules from database, ordered by priority (highest first)
        rules = db.query(EventRule).filter(EventRule.event_id == event_id).order_by(EventRule.priority.desc()).all()
        return self.calculate_score(rules, metrics)

    def calculate_score(self, rules: List[EventRule], metrics: Dict[str, Any]) -> float:
        """
        Evaluates a list of rules against a dictionary of metrics and returns the cumulative score.
        """
        total_score = 0.0

        for rule in rules:
            metric_val = self._find_metric_val(rule.metric, metrics)
            if metric_val is None:
                continue

            # Convert to appropriate types for comparison
            rule_val = rule.value
            try:
                # Try to treat the metric as a float for numeric comparisons
                num_metric_val = float(metric_val)
            except (ValueError, TypeError):
                num_metric_val = None

            try:
                num_rule_val = float(rule_val) if rule_val is not None else None
            except (ValueError, TypeError):
                num_rule_val = None

            operator = rule.operator.lower().strip()
            points_to_add = 0.0

            if operator in ["each", "multiplier"]:
                if num_metric_val is not None:
                    points_to_add = num_metric_val * rule.points
            elif operator in ["equals", "=="]:
                # String comparison fallback if numeric fails
                if num_metric_val is not None and num_rule_val is not None:
                    if num_metric_val == num_rule_val:
                        points_to_add = rule.points
                else:
                    if str(metric_val).strip().lower() == str(rule_val).strip().lower():
                        points_to_add = rule.points
            elif operator == "!=":
                if num_metric_val is not None and num_rule_val is not None:
                    if num_metric_val != num_rule_val:
                        points_to_add = rule.points
                else:
                    if str(metric_val).strip().lower() != str(rule_val).strip().lower():
                        points_to_add = rule.points
            elif operator == ">":
                if num_metric_val is not None and num_rule_val is not None:
                    if num_metric_val > num_rule_val:
                        points_to_add = rule.points
            elif operator == "<":
                if num_metric_val is not None and num_rule_val is not None:
                    if num_metric_val < num_rule_val:
                        points_to_add = rule.points
            elif operator == ">=":
                if num_metric_val is not None and num_rule_val is not None:
                    if num_metric_val >= num_rule_val:
                        points_to_add = rule.points
            elif operator == "<=":
                if num_metric_val is not None and num_rule_val is not None:
                    if num_metric_val <= num_rule_val:
                        points_to_add = rule.points
            else:
                logger.warning(f"Unknown operator: {operator}")

            total_score += points_to_add

        return total_score

rule_engine = RuleEngine()
