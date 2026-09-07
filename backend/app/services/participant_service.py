from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.participant import Participant
from app.models.player_score import PlayerScore
from app.models.user import User
from app.schemas.participant import ParticipantCreate
from app.services.ranking_service import ranking_service

class ParticipantService:
    def join_event(self, db: Session, event_id: int, participant_in: ParticipantCreate, current_user: User) -> Participant:
        # 1. Check if event exists
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        # 2. Prevent joining closed/completed events
        if event.status not in ["active", "draft"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot join event with status: {event.status}"
            )

        # 3. Prevent duplicate participation for the user
        existing_participant = db.query(Participant).filter(
            Participant.event_id == event_id,
            Participant.user_id == current_user.id
        ).first()
        
        if existing_participant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already joined this event"
            )

        # 4. Prevent exceeding participant limit
        if event.participant_limit is not None:
            current_count = db.query(Participant).filter(Participant.event_id == event_id).count()
            if current_count >= event.participant_limit:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Event participant limit reached"
                )

        # 5. Create participant
        db_participant = Participant(
            event_id=event_id,
            user_id=current_user.id,
            external_player_id=participant_in.external_player_id,
            status="registered"
        )
        db.add(db_participant)
        db.commit()
        db.refresh(db_participant)

        # 6. Initialize initial score 0.0 and leaderboard ranking
        player_score = PlayerScore(
            event_id=event_id,
            participant_id=db_participant.id,
            score=0.0
        )
        db.add(player_score)
        db.commit()
        
        ranking_service.recalculate_rankings(db, event_id)
        
        return db_participant


    def list_participants(self, db: Session, event_id: int, skip: int = 0, limit: int = 100) -> List[Participant]:
        # Check if event exists first
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
            
        participants = db.query(Participant).filter(
            Participant.event_id == event_id
        ).offset(skip).limit(limit).all()
        
        return participants

    def get_user_participations(self, db: Session, user_id: int) -> List[Participant]:
        return db.query(Participant).filter(
            Participant.user_id == user_id
        ).all()

participant_service = ParticipantService()

