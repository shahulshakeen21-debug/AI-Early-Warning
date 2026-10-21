import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_FILE = Path(__file__).resolve().parent / "scan_history.db"


def get_db_connection() -> sqlite3.Connection:
    """Establish connection to local SQLite database with row factory."""
    conn = sqlite3.connect(str(DB_FILE))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize scan history table if not present."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scan_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_uuid TEXT UNIQUE NOT NULL,
                timestamp TEXT NOT NULL,
                selected_plant TEXT,
                scan_type TEXT NOT NULL,
                predicted_class TEXT,
                confidence REAL,
                model_version TEXT,
                is_uncertain INTEGER NOT NULL,
                weather_summary TEXT,
                notes TEXT
            )
        """)
        conn.commit()


def save_scan(
    scan_uuid: str,
    selected_plant: Optional[str],
    scan_type: str,
    predicted_class: Optional[str],
    confidence: Optional[float],
    model_version: str,
    is_uncertain: bool,
    weather_summary: Optional[str] = None,
    notes: Optional[str] = None
) -> int:
    """Save a verified scan record into SQLite database."""
    init_db()
    now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO scan_records (
                scan_uuid, timestamp, selected_plant, scan_type,
                predicted_class, confidence, model_version, is_uncertain,
                weather_summary, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            scan_uuid,
            now_iso,
            selected_plant,
            scan_type,
            predicted_class,
            float(confidence) if confidence is not None else None,
            model_version,
            1 if is_uncertain else 0,
            weather_summary,
            notes
        ))
        conn.commit()
        return cursor.lastrowid


def get_all_scans(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve previous scan history ordered by timestamp descending."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, scan_uuid, timestamp, selected_plant, scan_type,
                   predicted_class, confidence, model_version, is_uncertain,
                   weather_summary, notes
            FROM scan_records
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_scan_by_uuid(scan_uuid: str) -> Optional[Dict[str, Any]]:
    """Retrieve single scan record by UUID."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, scan_uuid, timestamp, selected_plant, scan_type,
                   predicted_class, confidence, model_version, is_uncertain,
                   weather_summary, notes
            FROM scan_records
            WHERE scan_uuid = ?
        """, (scan_uuid,))
        row = cursor.fetchone()
        return dict(row) if row else None


def delete_scan(scan_id: int) -> bool:
    """Delete a scan record by ID."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scan_records WHERE id = ?", (scan_id,))
        conn.commit()
        return cursor.rowcount > 0


def clear_all_scans():
    """Clear all records from scan history."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scan_records")
        conn.commit()


def generate_scan_report_text(scan_record: Dict[str, Any], plant_info: Optional[Dict[str, Any]] = None) -> str:
    """Generate a clean, structured text report for downloading."""
    conf_str = f"{scan_record['confidence'] * 100:.1f}%" if scan_record.get("confidence") is not None else "N/A"
    uncertain_str = "YES (Consult Agricultural Extension Officer or KVK)" if scan_record.get("is_uncertain") else "NO"
    
    report = [
        "=" * 70,
        "AI PLANT DOCTOR - AGRICULTURAL SCAN REPORT",
        "=" * 70,
        f"Scan Reference ID : {scan_record.get('scan_uuid')}",
        f"Scan Timestamp    : {scan_record.get('timestamp')}",
        f"Scan Type         : {scan_record.get('scan_type')}",
        f"Selected Plant    : {scan_record.get('selected_plant', 'Unspecified')}",
        f"Model Version     : {scan_record.get('model_version', 'MobileNetV2-1.0')}",
        f"Identified Result : {scan_record.get('predicted_class', 'Unknown')}",
        f"Confidence Score  : {conf_str}",
        f"Uncertain Result  : {uncertain_str}",
        "-" * 70
    ]

    if scan_record.get("weather_summary"):
        report.extend([
            "LIVE WEATHER ADVISORY CONTEXT AT SCAN:",
            f"{scan_record.get('weather_summary')}",
            "-" * 70
        ])

    if plant_info:
        report.extend([
            "BOTANICAL & CARE OVERVIEW (FROM KNOWLEDGE BASE):",
            f"Scientific Name : {plant_info.get('scientific_name', 'N/A')}",
            f"Plant Family    : {plant_info.get('family', 'N/A')}",
            f"Category        : {plant_info.get('category', 'N/A')}",
            f"Sunlight        : {plant_info.get('growing_conditions', {}).get('sunlight', 'N/A')}",
            f"Watering        : {plant_info.get('growing_conditions', {}).get('watering', 'N/A')}",
            f"Soil            : {plant_info.get('growing_conditions', {}).get('soil', 'N/A')}",
            "-" * 70
        ])

    report.extend([
        "AGRICULTURAL SAFETY & DECISION SUPPORT DISCLAIMER:",
        "1. Model confidence is an algorithmic metric, not a scientific or medical guarantee.",
        "2. Predictions may be less accurate on real field photos. This is decision support,",
        "   not a replacement for certified agricultural extension officers or KVK experts.",
        "3. Never mix or spray pesticides without verifying official product labels and",
        "   consulting your local Block Agricultural Officer.",
        "=" * 70
    ])

    return "\n".join(report)
