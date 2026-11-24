"""History service for storing and retrieving job analysis results."""

import json
from datetime import datetime
from pathlib import Path


class HistoryService:
    """Service for managing job analysis history."""

    def __init__(self, storage_path: str = "data/history.json"):
        """Initialize history service with storage path."""
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize storage file if it doesn't exist
        if not self.storage_path.exists():
            self._write_history([])

    def _read_history(self) -> list[dict]:
        """Read history from storage."""
        try:
            with open(self.storage_path, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_history(self, history: list[dict]) -> None:
        """Write history to storage."""
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def save_analysis(
        self,
        cv_text: str,
        job_description: str,
        analysis: dict,
        cover_letter: str,
    ) -> str:
        """
        Save a job analysis to history.

        Args:
            cv_text: User's CV text
            job_description: Job description
            analysis: Analysis results from AI
            cover_letter: Generated cover letter

        Returns:
            ID of the saved analysis
        """
        history = self._read_history()

        # Generate ID based on timestamp
        analysis_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Extract job title from analysis
        job_title = (
            analysis.get("job", {}).get("title", "Unknown Position")
            if isinstance(analysis, dict)
            else "Unknown Position"
        )

        # Create history entry
        entry = {
            "id": analysis_id,
            "timestamp": datetime.now().isoformat(),
            "job_title": job_title,
            "fit_score": (analysis.get("fit_score", 0) if isinstance(analysis, dict) else 0),
            "cv_preview": cv_text[:200] + "..." if len(cv_text) > 200 else cv_text,
            "job_preview": (
                job_description[:200] + "..." if len(job_description) > 200 else job_description
            ),
            "cv_text": cv_text,
            "job_description": job_description,
            "analysis": analysis,
            "cover_letter": cover_letter,
        }

        # Add to history (newest first)
        history.insert(0, entry)

        # Keep only last 50 analyses
        history = history[:50]

        self._write_history(history)
        return analysis_id

    def get_history(self, limit: int = 20) -> list[dict]:
        """
        Get list of recent analyses.

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of analysis summaries
        """
        history = self._read_history()

        # Return only summary fields
        summaries = []
        for entry in history[:limit]:
            summaries.append(
                {
                    "id": entry["id"],
                    "timestamp": entry["timestamp"],
                    "job_title": entry["job_title"],
                    "fit_score": entry["fit_score"],
                    "cv_preview": entry["cv_preview"],
                    "job_preview": entry["job_preview"],
                }
            )

        return summaries

    def get_analysis(self, analysis_id: str) -> dict | None:
        """
        Get a specific analysis by ID.

        Args:
            analysis_id: ID of the analysis

        Returns:
            Full analysis data or None if not found
        """
        history = self._read_history()

        for entry in history:
            if entry["id"] == analysis_id:
                return entry

        return None

    def delete_analysis(self, analysis_id: str) -> bool:
        """
        Delete an analysis from history.

        Args:
            analysis_id: ID of the analysis to delete

        Returns:
            True if deleted, False if not found
        """
        history = self._read_history()
        initial_length = len(history)

        history = [entry for entry in history if entry["id"] != analysis_id]

        if len(history) < initial_length:
            self._write_history(history)
            return True

        return False

    def clear_history(self) -> None:
        """Clear all history."""
        self._write_history([])
