from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.participant import ParticipantCreate, ParticipantResponse
from app.services.participant_service import participant_service

router = APIRouter(tags=["Participants"])

@router.get(
    "/participants/me",
    response_model=List[ParticipantResponse],
    summary="List current user's participations",
    description="Returns all tournament participations for the logged-in user."
)
def get_my_participations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return participant_service.get_user_participations(db, current_user.id)

@router.post(
    "/events/{event_id}/join",
    response_model=ParticipantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Join an event",
    description="Registers the current user as a participant in an event. Can optionally provide an external_player_id."
)
def join_event(
    event_id: int,
    participant_in: ParticipantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return participant_service.join_event(db, event_id, participant_in, current_user)

@router.get(
    "/events/{event_id}/participants",
    response_model=List[ParticipantResponse],
    summary="List event participants",
    description="Returns a list of participants for a specific event."
)
def list_participants(
    event_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return participant_service.list_participants(db, event_id, skip, limit)

