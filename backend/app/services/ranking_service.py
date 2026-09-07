from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.event import Event
from app.models.participant import Participant
from app.models.player_score import PlayerScore
from app.models.ranking import Ranking
from app.models.user import User
from app.services.rule_engine import rule_engine

class RankingService:
    def process_validated_results(self, db: Session, event_id: int, valid_records: List[Dict[str, Any]], upload_id: Optional[int] = None):
        """
        Takes validated records, records PlayerResults, calculates scores, 
        saves updated PlayerScores, and recalculates the leaderboard.
        """
        from app.models.player_result import PlayerResult

        match_tag = f"upload_{upload_id}" if upload_id else "upload_batch"

        # If upload_id is provided, delete any previous results from this upload to avoid duplicate scores on re-run
        if upload_id:
            db.query(PlayerResult).filter(
                PlayerResult.event_id == event_id,
                PlayerResult.match_id == match_tag
            ).delete()

        # Insert new PlayerResult records
        for record in valid_records:
            participant_id = record.get("mapped_participant_id")
            metrics = record.get("metrics", {})
            match_id = record.get("match_id") or match_tag
            
            if not participant_id:
                continue

            pr = PlayerResult(
                event_id=event_id,
                participant_id=participant_id,
                match_id=match_id,
                metrics=metrics,
                validation_status="valid"
            )
            db.add(pr)

        db.commit()

        # Recalculate PlayerScores for all event participants based on all their valid results
        participants = db.query(Participant).filter(Participant.event_id == event_id).all()
        for p in participants:
            p_results = db.query(PlayerResult).filter(
                PlayerResult.event_id == event_id,
                PlayerResult.participant_id == p.id,
                PlayerResult.validation_status == "valid"
            ).all()

            total_score = sum(rule_engine.evaluate_metrics(db, event_id, res.metrics) for res in p_results)

            player_score = db.query(PlayerScore).filter(
                PlayerScore.event_id == event_id,
                PlayerScore.participant_id == p.id
            ).first()

            if not player_score:
                player_score = PlayerScore(
                    event_id=event_id,
                    participant_id=p.id,
                    score=total_score
                )
                db.add(player_score)
            else:
                player_score.score = total_score
            
        db.commit()
        
        # Recalculate Ranking
        self.recalculate_rankings(db, event_id)

    def recalculate_rankings(self, db: Session, event_id: int):
        """
        Recalculates the rankings for all participants in an event based on their current scores.
        Ensures all registered participants have at least an initial 0.0 score and rank.
        Handles ties correctly (e.g., 1, 2, 2, 4).
        """
        # 1. Ensure all registered participants have a PlayerScore
        participants = db.query(Participant).filter(Participant.event_id == event_id).all()
        for p in participants:
            ps = db.query(PlayerScore).filter(
                PlayerScore.event_id == event_id,
                PlayerScore.participant_id == p.id
            ).first()
            if not ps:
                db.add(PlayerScore(
                    event_id=event_id,
                    participant_id=p.id,
                    score=0.0
                ))
        db.commit()

        # 2. Get all scores for the event, ordered by score descending
        scores = db.query(PlayerScore).filter(PlayerScore.event_id == event_id).order_by(desc(PlayerScore.score), PlayerScore.participant_id.asc()).all()
        
        current_rank = 1
        current_score = None
        tied_count = 0
        
        for idx, p_score in enumerate(scores):
            if current_score is None:
                current_score = p_score.score
                
            if p_score.score < current_score:
                current_rank += tied_count + 1
                current_score = p_score.score
                tied_count = 0
            elif idx > 0:
                tied_count += 1
                
            # Update or create Ranking record
            ranking = db.query(Ranking).filter(
                Ranking.event_id == event_id,
                Ranking.participant_id == p_score.participant_id
            ).first()
            
            if not ranking:
                ranking = Ranking(
                    event_id=event_id,
                    participant_id=p_score.participant_id,
                    rank=current_rank,
                    score=p_score.score
                )
                db.add(ranking)
            else:
                ranking.rank = current_rank
                ranking.score = p_score.score
                
        db.commit()

    def get_leaderboard(self, db: Session, event_id: int, skip: int = 0, limit: int = 100, search: Optional[str] = None):
        """
        Fetches the leaderboard for an event, guaranteeing all registered participants are ranked.
        """
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
            
        # Ensure any registered participants without ranking are synced
        participant_count = db.query(Participant).filter(Participant.event_id == event_id).count()
        ranking_count = db.query(Ranking).filter(Ranking.event_id == event_id).count()
        if participant_count != ranking_count:
            self.recalculate_rankings(db, event_id)

        query = db.query(Ranking, Participant, User).join(
            Participant, Ranking.participant_id == Participant.id
        ).outerjoin(
            User, Participant.user_id == User.id
        ).filter(Ranking.event_id == event_id)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Participant.external_player_id.ilike(search_term)) |
                (User.name.ilike(search_term))
            )
            
        query = query.order_by(Ranking.rank.asc()).offset(skip).limit(limit)
        results = query.all()
        
        rankings = []
        for ranking, participant, user in results:
            display_name = (user.name if user else None) or participant.external_player_id or f"Player #{participant.id}"
            rankings.append({
                "id": ranking.id,
                "event_id": ranking.event_id,
                "participant_id": ranking.participant_id,
                "rank": ranking.rank,
                "score": ranking.score,
                "external_player_id": participant.external_player_id,
                "username": display_name
            })
            
        total_participants = db.query(Ranking).filter(Ranking.event_id == event_id).count()
            
        return {
            "event_id": event_id,
            "total_participants": total_participants,
            "rankings": rankings
        }

    def get_player_rank(self, db: Session, event_id: int, player_id: str):
        """
        Gets the specific rank for a player.
        player_id can be external_player_id or username or participant ID.
        """
        # Ensure ranks are up-to-date
        participant_count = db.query(Participant).filter(Participant.event_id == event_id).count()
        ranking_count = db.query(Ranking).filter(Ranking.event_id == event_id).count()
        if participant_count != ranking_count:
            self.recalculate_rankings(db, event_id)

        # Try finding participant
        query = db.query(Ranking, Participant, User).join(
            Participant, Ranking.participant_id == Participant.id
        ).outerjoin(
            User, Participant.user_id == User.id
        ).filter(Ranking.event_id == event_id)
        
        # Apply search condition
        condition = (Participant.external_player_id == player_id) | (User.name == player_id)
        if player_id.isdigit():
            condition = condition | (Participant.id == int(player_id))
            
        result = query.filter(condition).first()
        
        if not result:
            raise HTTPException(status_code=404, detail="Player rank not found in this event")
            
        ranking, participant, user = result
        display_name = (user.name if user else None) or participant.external_player_id or f"Player #{participant.id}"
        return {
            "id": ranking.id,
            "event_id": ranking.event_id,
            "participant_id": ranking.participant_id,
            "rank": ranking.rank,
            "score": ranking.score,
            "external_player_id": participant.external_player_id,
            "username": display_name
        }

ranking_service = RankingService()
