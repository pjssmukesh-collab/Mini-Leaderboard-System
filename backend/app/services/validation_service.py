import json
import os
from typing import List, Dict, Any, Tuple
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.result_upload import ResultUpload
from app.models.participant import Participant
from app.models.user import User
from app.schemas.validation import ValidationReport, ValidationIssue
from app.services.extraction_service import extraction_service

from app.services.ranking_service import ranking_service

UPLOAD_DIR = "uploads"

class ValidationService:
    def validate_upload(self, db: Session, upload_id: int) -> ValidationReport:
        upload = db.query(ResultUpload).filter(ResultUpload.id == upload_id).first()
        if not upload:
            raise HTTPException(status_code=404, detail="Upload not found")
            
        file_path = os.path.join(UPLOAD_DIR, f"{upload.id}_{upload.filename}")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Uploaded file not found on disk")
            
        # Extract normalized data
        try:
            records = extraction_service.extract(file_path, upload.file_type, upload.event_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Extraction failed: {str(e)}")

        issues = []
        valid_records = []
        
        # Load participants for mapping
        participants = db.query(Participant).filter(Participant.event_id == upload.event_id).all()
        # Create lookup maps
        participant_by_ext_id = {p.external_player_id: p for p in participants if p.external_player_id}
        participant_by_id = {str(p.id): p for p in participants}
        
        # For name matching, we might need user info
        user_ids = [p.user_id for p in participants if p.user_id]
        users = db.query(User).filter(User.id.in_(user_ids)).all() if user_ids else []
        participant_by_username = {u.username: next(p for p in participants if p.user_id == u.id) for u in users}
        participant_by_name = {u.name.lower().strip(): next(p for p in participants if p.user_id == u.id) for u in users if u.name}

        seen_matches = set()
        
        for idx, record in enumerate(records):
            player_id_raw = str(record.get("player_id", "")).strip()
            match_id_raw = str(record.get("match_id", "")).strip()
            metrics = record.get("metrics", {})
            
            # Required fields
            if not player_id_raw:
                issues.append(ValidationIssue(row_index=idx, player_id=player_id_raw, issue_type="MISSING_FIELD", message="player_id is required"))
                continue
                
            # Mapping player
            mapped_participant = None
            if player_id_raw in participant_by_ext_id:
                mapped_participant = participant_by_ext_id[player_id_raw]
            elif player_id_raw in participant_by_id:
                mapped_participant = participant_by_id[player_id_raw]
            elif player_id_raw in participant_by_username:
                mapped_participant = participant_by_username[player_id_raw]
            elif player_id_raw.lower() in participant_by_name:
                mapped_participant = participant_by_name[player_id_raw.lower()]
                
            if not mapped_participant:
                issues.append(ValidationIssue(row_index=idx, player_id=player_id_raw, issue_type="UNKNOWN_PLAYER", message=f"Player ID '{player_id_raw}' could not be mapped to any registered participant"))
                continue
                
            # Missing or Invalid Values in metrics
            has_invalid_metric = False
            for k, v in metrics.items():
                if v is None or str(v).strip() == "":
                    issues.append(ValidationIssue(row_index=idx, player_id=player_id_raw, issue_type="MISSING_VALUE", message=f"Metric '{k}' has a missing value"))
                    has_invalid_metric = True
                    
            if has_invalid_metric:
                continue
                
            # Duplicate checks
            match_key = f"{mapped_participant.id}_{match_id_raw}"
            if match_key in seen_matches:
                issues.append(ValidationIssue(row_index=idx, player_id=player_id_raw, issue_type="DUPLICATE_RESULT", message=f"Duplicate result for player in match '{match_id_raw}'"))
                continue
            
            seen_matches.add(match_key)
            
            # If all checks pass
            record["mapped_participant_id"] = mapped_participant.id
            valid_records.append(record)
            
        # Summarize
        unknown_players_count = len([i for i in issues if i.issue_type == "UNKNOWN_PLAYER"])
        duplicates_count = len([i for i in issues if i.issue_type == "DUPLICATE_RESULT"])
        invalid_values_count = len([i for i in issues if i.issue_type in ["MISSING_VALUE", "MISSING_FIELD", "INVALID_VALUE"]])
        
        status = "valid" if len(issues) == 0 else "invalid"
        
        report = ValidationReport(
            upload_id=upload_id,
            total_records=len(records),
            valid_records=len(valid_records),
            unknown_players=unknown_players_count,
            duplicates=duplicates_count,
            invalid_values=invalid_values_count,
            issues=issues,
            status=status,
            valid_data=valid_records
        )
        
        # Save report to disk
        report_path = os.path.join(UPLOAD_DIR, f"{upload_id}_validation.json")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(exclude={"valid_data"}))  # don't save raw valid data in report summary
            
        # Automatically process and update scores if valid records are present
        if valid_records:
            ranking_service.process_validated_results(
                db=db,
                event_id=upload.event_id,
                valid_records=valid_records,
                upload_id=upload.id
            )

        upload.status = "processed" if status == "valid" else "validation_failed"
        db.commit()
        
        return report

    def process_upload(self, db: Session, upload_id: int) -> Dict[str, Any]:
        """
        Explicitly triggers score calculation and leaderboard update for an upload.
        """
        upload = db.query(ResultUpload).filter(ResultUpload.id == upload_id).first()
        if not upload:
            raise HTTPException(status_code=404, detail="Upload not found")
            
        report = self.validate_upload(db, upload_id)
        if report.valid_records == 0 and len(report.issues) > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Upload has {len(report.issues)} validation issues and no valid records to score."
            )
            
        return {
            "upload_id": upload.id,
            "event_id": upload.event_id,
            "status": upload.status,
            "scored_records": report.valid_records,
            "message": f"Successfully calculated scores for {report.valid_records} participants."
        }

    def get_validation_report(self, db: Session, upload_id: int) -> ValidationReport:
        upload = db.query(ResultUpload).filter(ResultUpload.id == upload_id).first()
        if not upload:
            raise HTTPException(status_code=404, detail="Upload not found")
            
        report_path = os.path.join(UPLOAD_DIR, f"{upload_id}_validation.json")
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail="Validation report not found (has it been validated yet?)")
            
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return ValidationReport(**data)

validation_service = ValidationService()
