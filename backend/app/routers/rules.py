from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_creator
from app.database.database import get_db
from app.models.user import User
from app.schemas.rule import EventRuleCreate, EventRuleUpdate, EventRuleResponse
from app.services.rule_service import rule_service

router = APIRouter(tags=["Rules"])

@router.post(
    "/events/{event_id}/rules",
    response_model=EventRuleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a scoring rule for an event",
    description="Adds a new dynamic scoring rule to a specific event. Only the event creator or an Admin can add rules."
)
def create_rule(
    event_id: int,
    rule_in: EventRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_creator),
):
    return rule_service.create_rule(db, event_id, rule_in, current_user)

@router.get(
    "/events/{event_id}/rules",
    response_model=List[EventRuleResponse],
    summary="List scoring rules for an event",
    description="Returns all scoring rules configured for a specific event."
)
def list_rules(
    event_id: int,
    db: Session = Depends(get_db)
):
    return rule_service.list_rules(db, event_id)

@router.put(
    "/rules/{rule_id}",
    response_model=EventRuleResponse,
    summary="Update a scoring rule",
    description="Updates an existing scoring rule. Only the event creator or an Admin can perform this action."
)
def update_rule(
    rule_id: int,
    rule_in: EventRuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_creator),
):
    return rule_service.update_rule(db, rule_id, rule_in, current_user)

@router.delete(
    "/rules/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a scoring rule",
    description="Deletes a scoring rule. Only the event creator or an Admin can perform this action."
)
def delete_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_creator),
):
    rule_service.delete_rule(db, rule_id, current_user)
    return None
