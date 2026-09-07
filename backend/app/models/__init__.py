# app/models/__init__.py
# ──────────────────────────────────────────────
# SQLAlchemy database models package
#
# Exporting all models here allows Base.metadata.create_all()
# to discover and register all tables automatically.
# ──────────────────────────────────────────────

from app.models.user import User
from app.models.event import Event
from app.models.event_rule import EventRule
from app.models.participant import Participant
from app.models.result_upload import ResultUpload
from app.models.raw_result import RawResult
from app.models.player_result import PlayerResult
from app.models.player_score import PlayerScore
from app.models.ranking import Ranking
from app.models.upload_log import UploadLog

__all__ = [
    "User",
    "Event",
    "EventRule",
    "Participant",
    "ResultUpload",
    "RawResult",
    "PlayerResult",
    "PlayerScore",
    "Ranking",
    "UploadLog",
]
