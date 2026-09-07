from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ValidationIssue(BaseModel):
    row_index: int
    player_id: str
    issue_type: str
    message: str

class ValidationReport(BaseModel):
    upload_id: int
    total_records: int
    valid_records: int
    unknown_players: int
    duplicates: int
    invalid_values: int
    issues: List[ValidationIssue] = []
    status: str = Field(..., description="'valid', 'invalid', 'pending'")
    
    # Optionally store the mapped valid results for the next phase
    valid_data: Optional[List[Dict[str, Any]]] = None
