from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from core.models import AnalysisReport


DB_PATH = Path("data/cinevora.db")


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


def _ensure_extended_tables(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS collaboration_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_title TEXT NOT NULL,
            item_type TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            owner TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS talent_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT NOT NULL,
            skills TEXT NOT NULL,
            portfolio TEXT NOT NULL,
            contact TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS consultation_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_title TEXT NOT NULL,
            requester TEXT NOT NULL,
            topic TEXT NOT NULL,
            notes TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS university_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT NOT NULL,
            project_title TEXT NOT NULL,
            student_or_team TEXT NOT NULL,
            milestone TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS community_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )
    connection.commit()


def add_collaboration_item(project_title: str, item_type: str, title: str, body: str, owner: str, status: str) -> None:
    with _connect() as connection:
        _ensure_extended_tables(connection)
        connection.execute(
            "INSERT INTO collaboration_items(project_title,item_type,title,body,owner,status,created_at) VALUES (?,?,?,?,?,?,?)",
            (project_title, item_type, title, body, owner, status, datetime.now(timezone.utc).isoformat()),
        )
        connection.commit()


def list_collaboration_items(project_title: str = "") -> list[dict]:
    with _connect() as connection:
        _ensure_extended_tables(connection)
        connection.row_factory = sqlite3.Row
        if project_title:
            rows = connection.execute("SELECT * FROM collaboration_items WHERE project_title=? ORDER BY id DESC", (project_title,)).fetchall()
        else:
            rows = connection.execute("SELECT * FROM collaboration_items ORDER BY id DESC").fetchall()
    return [dict(row) for row in rows]


def add_talent_profile(name: str, role: str, location: str, skills: str, portfolio: str, contact: str) -> None:
    with _connect() as connection:
        _ensure_extended_tables(connection)
        connection.execute(
            "INSERT INTO talent_profiles(name,role,location,skills,portfolio,contact,created_at) VALUES (?,?,?,?,?,?,?)",
            (name, role, location, skills, portfolio, contact, datetime.now(timezone.utc).isoformat()),
        )
        connection.commit()


def list_talent_profiles() -> list[dict]:
    with _connect() as connection:
        _ensure_extended_tables(connection)
        connection.row_factory = sqlite3.Row
        rows = connection.execute("SELECT * FROM talent_profiles ORDER BY id DESC").fetchall()
    return [dict(row) for row in rows]


def add_consultation_request(project_title: str, requester: str, topic: str, notes: str, status: str = "Requested") -> None:
    with _connect() as connection:
        _ensure_extended_tables(connection)
        connection.execute(
            "INSERT INTO consultation_requests(project_title,requester,topic,notes,status,created_at) VALUES (?,?,?,?,?,?)",
            (project_title, requester, topic, notes, status, datetime.now(timezone.utc).isoformat()),
        )
        connection.commit()


def list_consultation_requests() -> list[dict]:
    with _connect() as connection:
        _ensure_extended_tables(connection)
        connection.row_factory = sqlite3.Row
        rows = connection.execute("SELECT * FROM consultation_requests ORDER BY id DESC").fetchall()
    return [dict(row) for row in rows]


def add_university_item(course: str, project_title: str, student_or_team: str, milestone: str, status: str, notes: str) -> None:
    with _connect() as connection:
        _ensure_extended_tables(connection)
        connection.execute(
            "INSERT INTO university_items(course,project_title,student_or_team,milestone,status,notes,created_at) VALUES (?,?,?,?,?,?,?)",
            (course, project_title, student_or_team, milestone, status, notes, datetime.now(timezone.utc).isoformat()),
        )
        connection.commit()


def list_university_items() -> list[dict]:
    with _connect() as connection:
        _ensure_extended_tables(connection)
        connection.row_factory = sqlite3.Row
        rows = connection.execute("SELECT * FROM university_items ORDER BY id DESC").fetchall()
    return [dict(row) for row in rows]


def add_community_post(author: str, category: str, title: str, body: str) -> None:
    with _connect() as connection:
        _ensure_extended_tables(connection)
        connection.execute(
            "INSERT INTO community_posts(author,category,title,body,created_at) VALUES (?,?,?,?,?)",
            (author, category, title, body, datetime.now(timezone.utc).isoformat()),
        )
        connection.commit()


def list_community_posts() -> list[dict]:
    with _connect() as connection:
        _ensure_extended_tables(connection)
        connection.row_factory = sqlite3.Row
        rows = connection.execute("SELECT * FROM community_posts ORDER BY id DESC LIMIT 100").fetchall()
    return [dict(row) for row in rows]
