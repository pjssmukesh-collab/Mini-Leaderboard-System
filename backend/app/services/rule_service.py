from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.event_rule import EventRule
from app.models.event import Event
from app.models.user import User
from app.schemas.rule import EventRuleCreate, EventRuleUpdate

class RuleService:
    def _check_event_ownership(self, db: Session, event_id: int, user: User) -> Event:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        if event.creator_id != user.id and user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to modify rules for this event"
            )
        return event

    def create_rule(self, db: Session, event_id: int, rule_in: EventRuleCreate, current_user: User) -> EventRule:
        self._check_event_ownership(db, event_id, current_user)
        
        db_rule = EventRule(
            event_id=event_id,
            metric=rule_in.metric,
            condition=rule_in.condition,
            operator=rule_in.operator,
            value=rule_in.value,
            points=rule_in.points,
            priority=rule_in.priority
        )
        db.add(db_rule)
        db.commit()
        db.refresh(db_rule)
        return db_rule

    def list_rules(self, db: Session, event_id: int) -> List[EventRule]:
        # Anyone can view rules for an event
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        
        rules = db.query(EventRule).filter(EventRule.event_id == event_id).order_by(EventRule.priority.desc()).all()
        return rules

    def update_rule(self, db: Session, rule_id: int, rule_in: EventRuleUpdate, current_user: User) -> EventRule:
        db_rule = db.query(EventRule).filter(EventRule.id == rule_id).first()
        if not db_rule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rule not found"
            )
        
        self._check_event_ownership(db, db_rule.event_id, current_user)

        update_data = rule_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_rule, key, value)
            
        db.commit()
        db.refresh(db_rule)
        return db_rule

    def delete_rule(self, db: Session, rule_id: int, current_user: User) -> None:
        db_rule = db.query(EventRule).filter(EventRule.id == rule_id).first()
        if not db_rule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rule not found"
            )
            
        self._check_event_ownership(db, db_rule.event_id, current_user)
        
        db.delete(db_rule)
        db.commit()

rule_service = RuleService()
