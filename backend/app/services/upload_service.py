import os
import shutil
from typing import List
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.result_upload import ResultUpload
from app.models.upload_log import UploadLog
from app.models.user import User

UPLOAD_DIR = "uploads"

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

class UploadService:
    def _detect_file_type(self, filename: str) -> str:
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        if ext in ["csv"]:
            return "csv"
        elif ext in ["xlsx"]:
            return "xlsx"
        elif ext in ["json"]:
            return "json"
        else:
            return "unknown"

    def upload_result(self, db: Session, event_id: int, file: UploadFile, current_user: User) -> ResultUpload:
        # Check if event exists and user is creator or admin
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
            
        if event.creator_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to upload results for this event"
            )
            
        # Detect file type
        file_type = self._detect_file_type(file.filename)
        if file_type == "unknown":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file format. Supported formats: CSV (.csv), Excel (.xlsx), and JSON (.json)."
            )
            
        # Create ResultUpload record
        db_upload = ResultUpload(
            event_id=event_id,
            uploaded_by=current_user.id,
            filename=file.filename,
            file_type=file_type,
            status="pending"
        )
        db.add(db_upload)
        db.commit()
        db.refresh(db_upload)
        
        # Save file to disk
        file_path = os.path.join(UPLOAD_DIR, f"{db_upload.id}_{file.filename}")
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                
            # Log action
            log = UploadLog(
                upload_id=db_upload.id,
                action="FILE_UPLOADED",
                message=f"File {file.filename} uploaded successfully."
            )
            db.add(log)
            db.commit()
            
        except Exception as e:
            db_upload.status = "failed"
            log = UploadLog(
                upload_id=db_upload.id,
                action="UPLOAD_ERROR",
                message=f"Failed to save file: {str(e)}"
            )
            db.add(log)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not save the uploaded file."
            )
            
        db.refresh(db_upload)
        return db_upload

    def list_event_uploads(self, db: Session, event_id: int) -> List[ResultUpload]:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
            
        return db.query(ResultUpload).filter(ResultUpload.event_id == event_id).order_by(ResultUpload.uploaded_at.desc()).all()

    def get_upload_detail(self, db: Session, upload_id: int) -> ResultUpload:
        upload = db.query(ResultUpload).filter(ResultUpload.id == upload_id).first()
        if not upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Upload record not found"
            )
        return upload

upload_service = UploadService()
