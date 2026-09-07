import json
import os
import pandas as pd
from typing import List, Dict, Any
from fastapi import HTTPException

class ExtractionService:
    def extract(self, file_path: str, file_type: str, event_id: int) -> List[Dict[str, Any]]:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        if file_type == "csv":
            return self._extract_csv(file_path, event_id)
        elif file_type == "xlsx":
            return self._extract_excel(file_path, event_id)
        elif file_type == "json":
            return self._extract_json(file_path, event_id)
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type for extraction: {file_type}. Please upload CSV, Excel, or JSON."
            )

    def _extract_csv(self, file_path: str, event_id: int) -> List[Dict[str, Any]]:
        try:
            df = pd.read_csv(file_path)
            return self._dataframe_to_normalized(df, event_id)
        except Exception as e:
            raise ValueError(f"Failed to parse CSV: {str(e)}")

    def _extract_excel(self, file_path: str, event_id: int) -> List[Dict[str, Any]]:
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            return self._dataframe_to_normalized(df, event_id)
        except Exception as e:
            raise ValueError(f"Failed to parse Excel: {str(e)}")

    def _extract_json(self, file_path: str, event_id: int) -> List[Dict[str, Any]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Assuming JSON is a list of records
            if not isinstance(data, list):
                # If it's a single dict, wrap it
                if isinstance(data, dict):
                    if "player_id" in data or "metrics" in data:
                        data = [data]
                    else:
                        raise ValueError("JSON must be a list of records")
                else:
                    raise ValueError("JSON must be a list of records")

            normalized = []
            for record in data:
                # Handle case where JSON is already in normalized format
                if "metrics" in record and "player_id" in record:
                    normalized.append({
                        "event_id": event_id,
                        "player_id": str(record.get("player_id")),
                        "match_id": str(record.get("match_id", "")),
                        "metrics": record.get("metrics", {})
                    })
                else:
                    # Flat record
                    player_id = record.pop("player_id", None)
                    match_id = record.pop("match_id", "")
                    
                    if not player_id:
                        continue
                        
                    normalized.append({
                        "event_id": event_id,
                        "player_id": str(player_id),
                        "match_id": str(match_id),
                        "metrics": record
                    })
            return normalized
        except Exception as e:
            raise ValueError(f"Failed to parse JSON: {str(e)}")

    def _dataframe_to_normalized(self, df: pd.DataFrame, event_id: int) -> List[Dict[str, Any]]:
        normalized = []
        
        # Look for standard columns (including 'Player Name', 'username', 'name', etc.)
        player_id_col = next((col for col in df.columns if col.strip().lower() in [
            'player_id', 'player id', 'player', 'player name', 'player_name', 
            'id', 'user_id', 'user id', 'username', 'name', 'external_id'
        ]), None)
        match_id_col = next((col for col in df.columns if col.strip().lower() in [
            'match_id', 'match id', 'match', 'game_id', 'game id'
        ]), None)
        
        if not player_id_col:
            raise ValueError("Could not find a player identifier column (e.g. 'Player Name', 'player_id') in the file.")
            
        for _, row in df.iterrows():
            player_id = str(row[player_id_col])
            match_id = str(row[match_id_col]) if match_id_col else ""
            
            # All other columns are metrics
            metrics = {}
            for col in df.columns:
                if col != player_id_col and col != match_id_col:
                    val = row[col]
                    # Handle NaN / nulls
                    if pd.isna(val):
                        continue
                    metrics[col] = val
                    
            normalized.append({
                "event_id": event_id,
                "player_id": player_id,
                "match_id": match_id,
                "metrics": metrics
            })
            
        return normalized

extraction_service = ExtractionService()
