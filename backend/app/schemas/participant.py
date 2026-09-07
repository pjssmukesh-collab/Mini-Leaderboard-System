from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ParticipantBase(BaseModel):
    external_player_id: Optional[str] = Field(
        default=None,
        max_length=100,
        description="External player identifier (e.g., in-game handle/tag)",
        examples=["GamerTag123", "chess_master_99"]
    )

class ParticipantCreate(ParticipantBase):
    pass

class ParticipantResponse(ParticipantBase):
    id: int
    event_id: int
    user_id: Optional[int]
    joined_at: datetime
    status: str
    
    model_config = ConfigDict(from_attributes=True)
