from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class RankingResponse(BaseModel):
    id: int
    event_id: int
    participant_id: int
    rank: int
    score: float
    
    # Optional fields for display purposes
    external_player_id: Optional[str] = None
    username: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class LeaderboardResponse(BaseModel):
    event_id: int
    total_participants: int
    rankings: List[RankingResponse]
