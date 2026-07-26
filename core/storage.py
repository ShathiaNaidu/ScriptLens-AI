from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from core.models import AnalysisReport


DB_PATH = Path("data/scriptlens.db")


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            writer TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_hash TEXT NOT NULL,
            model_used TEXT NOT NULL,
            created_at TEXT NOT NULL,
            report_json TEXT NOT NULL
        )
        """
    )
    connection.commit()
    return connection


def save_analysis(
    report: AnalysisReport,
    filename: str,
    file_hash: str,
    model_used: str,
) -> int:
    with _connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO analyses
            (title, writer, filename, file_hash, model_used, created_at, report_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                report.metadata.title,
                report.metadata.writer,
                filename,
                file_hash,
                model_used,
                datetime.now(timezone.utc).isoformat(),
                report.model_dump_json(),
            ),
        )
        connection.commit()
        return int(cursor.lastrowid)


def list_analyses(limit: int = 20) -> list[dict]:
    with _connect() as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT id, title, writer, filename, model_used, created_at
            FROM analyses
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def load_analysis(analysis_id: int) -> AnalysisReport:
    with _connect() as connection:
        row = connection.execute(
            "SELECT report_json FROM analyses WHERE id = ?", (analysis_id,)
        ).fetchone()
    if not row:
        raise KeyError(f"Analysis {analysis_id} was not found.")
    return AnalysisReport.model_validate_json(row[0])


def delete_analysis(analysis_id: int) -> None:
    with _connect() as connection:
        connection.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
        connection.commit()


def export_record(report: AnalysisReport) -> str:
    return json.dumps(report.model_dump(mode="json"), ensure_ascii=False, indent=2)
