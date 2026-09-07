from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class UploadLogResponse(BaseModel):
    id: int
    upload_id: int
    action: str
    message: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ResultUploadResponse(BaseModel):
    id: int
    event_id: int
    uploaded_by: int
    filename: str
    file_type: str
    status: str
    uploaded_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class ResultUploadDetailResponse(ResultUploadResponse):
    logs: List[UploadLogResponse] = []
