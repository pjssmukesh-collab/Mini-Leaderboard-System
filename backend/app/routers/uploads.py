from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session

from app.core.deps import require_creator, get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.result_upload import ResultUploadResponse, ResultUploadDetailResponse
from app.services.upload_service import upload_service

router = APIRouter(tags=["Result Uploads"])

@router.post(
    "/events/{event_id}/results/upload",
    response_model=ResultUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload event results",
    description="Upload a result file (CSV, XLSX, JSON) for an event."
)
def upload_results(
    event_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_creator),
):
    return upload_service.upload_result(db, event_id, file, current_user)

@router.get(
    "/events/{event_id}/results",
    response_model=List[ResultUploadResponse],
    summary="List result uploads for an event",
    description="Returns a history of uploaded result files for the given event."
)
def list_event_uploads(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user), # Any authenticated user can view history for now or maybe just creator?
):
    # Assuming organizers/users can see the uploads. Access control can be tightened in service if needed.
    return upload_service.list_event_uploads(db, event_id)

@router.get(
    "/uploads/{upload_id}",
    response_model=ResultUploadDetailResponse,
    summary="Get upload details",
    description="Returns details about a specific upload including its processing logs."
)
def get_upload_detail(
    upload_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return upload_service.get_upload_detail(db, upload_id)
