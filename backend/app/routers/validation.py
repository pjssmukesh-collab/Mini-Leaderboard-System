from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import require_creator
from app.database.database import get_db
from app.models.user import User
from app.schemas.validation import ValidationReport
from app.services.validation_service import validation_service

router = APIRouter(tags=["Validation"])

@router.post(
    "/uploads/{upload_id}/validate",
    response_model=ValidationReport,
    summary="Validate an upload",
    description="Extracts data from the uploaded file and validates it against the event's participants and rules."
)
def validate_upload(
    upload_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_creator),
):
    return validation_service.validate_upload(db, upload_id)

@router.get(
    "/uploads/{upload_id}/validation",
    response_model=ValidationReport,
    summary="Get validation report",
    description="Retrieves the latest validation report for a specific upload."
)
def get_validation_report(
    upload_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_creator),
):
    return validation_service.get_validation_report(db, upload_id)

@router.post(
    "/uploads/{upload_id}/process",
    summary="Process and calculate scores for an upload",
    description="Calculates player scores and recalculates rankings for the event."
)
def process_upload(
    upload_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_creator),
):
    return validation_service.process_upload(db, upload_id)
