from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.ranking import LeaderboardResponse, RankingResponse
from app.services.ranking_service import ranking_service

router = APIRouter(prefix="/events/{event_id}", tags=["Leaderboard"])

@router.get(
    "/leaderboard",
    response_model=LeaderboardResponse,
    summary="Get full leaderboard",
    description="Retrieves the leaderboard for an event. Supports pagination and searching by player name/ID."
)
def get_leaderboard(
    event_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None, description="Search by username or external player ID"),
    db: Session = Depends(get_db)
):
    return ranking_service.get_leaderboard(db, event_id, skip, limit, search)

@router.get(
    "/leaderboard/top/{n}",
    response_model=LeaderboardResponse,
    summary="Get top N players",
    description="Retrieves the top N players on the leaderboard."
)
def get_top_n_leaderboard(
    event_id: int,
    n: int,
    db: Session = Depends(get_db)
):
    return ranking_service.get_leaderboard(db, event_id, skip=0, limit=n)

@router.get(
    "/players/{player_id}/rank",
    response_model=RankingResponse,
    summary="Get player rank",
    description="Retrieves the current rank and score for a specific player in an event."
)
def get_player_rank(
    event_id: int,
    player_id: str,
    db: Session = Depends(get_db)
):
    return ranking_service.get_player_rank(db, event_id, player_id)
