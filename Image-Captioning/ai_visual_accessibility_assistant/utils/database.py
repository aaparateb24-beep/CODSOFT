import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Tuple

class DatabaseManager:
    """
    Manages SQLite database initialization, insertion of processing history,
    retrieval of records, and aggregation for analytics.
    """
    def __init__(self, db_path: str = "data/database.db"):
        self.db_path = db_path
        # Ensure the directory exists
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        self.initialize_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Returns a sqlite3 connection with row factory enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        # Enable foreign key support
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def initialize_db(self):
        """Creates history and object_detections tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Create history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    resolution TEXT,
                    file_size_kb REAL,
                    caption TEXT,
                    caption_confidence REAL,
                    scene_category TEXT,
                    scene_explanation TEXT,
                    accessibility_description TEXT,
                    summary TEXT,
                    main_subject TEXT,
                    activity TEXT,
                    environment TEXT,
                    context TEXT,
                    use_case TEXT,
                    original_image_path TEXT,
                    annotated_image_path TEXT
                );
            """)

            # Create object_detections table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS object_detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    history_id INTEGER,
                    object_name TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    bbox_x1 REAL,
                    bbox_y1 REAL,
                    bbox_x2 REAL,
                    bbox_y2 REAL,
                    FOREIGN KEY (history_id) REFERENCES history(id) ON DELETE CASCADE
                );
            """)
            conn.commit()

    def save_record(self, record_data: Dict[str, Any], detections: List[Dict[str, Any]]) -> int:
        """
        Saves analysis results and detected objects in a single transaction.
        
        Args:
            record_data: Dictionary containing fields matching the history table.
            detections: List of dictionaries representing detected objects,
                        each containing 'name', 'confidence', and 'bbox'.
        Returns:
            The primary key (id) of the inserted history record.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Use current time if timestamp not provided
            if 'timestamp' not in record_data or not record_data['timestamp']:
                record_data['timestamp'] = datetime.now().isoformat()
            
            # Insert into history table
            columns = [
                'filename', 'timestamp', 'resolution', 'file_size_kb', 
                'caption', 'caption_confidence', 'scene_category', 'scene_explanation', 
                'accessibility_description', 'summary', 'main_subject', 'activity', 
                'environment', 'context', 'use_case', 'original_image_path', 'annotated_image_path'
            ]
            
            # Filter and prepare values
            val_placeholders = ", ".join(["?" for _ in columns])
            col_names = ", ".join(columns)
            values = [record_data.get(col) for col in columns]
            
            cursor.execute(
                f"INSERT INTO history ({col_names}) VALUES ({val_placeholders})",
                values
            )
            history_id = cursor.lastrowid
            
            # Insert into object_detections table
            for det in detections:
                bbox = det.get('bbox', [0, 0, 0, 0])
                # Safety checking for bbox structure
                x1, y1, x2, y2 = bbox if len(bbox) == 4 else (0, 0, 0, 0)
                
                cursor.execute("""
                    INSERT INTO object_detections (
                        history_id, object_name, confidence, bbox_x1, bbox_y1, bbox_x2, bbox_y2
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (history_id, det['name'], det['confidence'], x1, y1, x2, y2))
                
            conn.commit()
            return history_id

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves history records sorted by timestamp descending."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM history ORDER BY datetime(timestamp) DESC LIMIT ?", 
                (limit,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_record(self, history_id: int) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Retrieves a single history record and its associated object detections.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Fetch history record
            cursor.execute("SELECT * FROM history WHERE id = ?", (history_id,))
            hist_row = cursor.fetchone()
            if not hist_row:
                return {}, []
            
            history_dict = dict(hist_row)
            
            # Fetch object detections
            cursor.execute("""
                SELECT object_name as name, confidence, bbox_x1, bbox_y1, bbox_x2, bbox_y2
                FROM object_detections 
                WHERE history_id = ?
            """, (history_id,))
            det_rows = cursor.fetchall()
            
            detections = []
            for row in det_rows:
                detections.append({
                    "name": row["name"],
                    "confidence": row["confidence"],
                    "bbox": [row["bbox_x1"], row["bbox_y1"], row["bbox_x2"], row["bbox_y2"]]
                })
                
            return history_dict, detections

    def delete_record(self, history_id: int):
        """Deletes a history record and cascade-deletes its detections."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history WHERE id = ?", (history_id,))
            conn.commit()

    def clear_all_history(self):
        """Clears all history and detection records."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM object_detections")
            cursor.execute("DELETE FROM history")
            conn.commit()

    def get_analytics(self) -> Dict[str, Any]:
        """
        Computes various statistics for the analytics dashboard.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Total Images Processed
            cursor.execute("SELECT COUNT(*) FROM history")
            total_images = cursor.fetchone()[0]
            
            if total_images == 0:
                return {
                    "total_images": 0,
                    "top_objects": [],
                    "scene_distribution": {},
                    "avg_confidence": 0.0,
                    "recent_activity": []
                }
            
            # 2. Most Detected Objects
            cursor.execute("""
                SELECT object_name, COUNT(*) as count 
                FROM object_detections 
                GROUP BY object_name 
                ORDER BY count DESC 
                LIMIT 10
            """)
            top_objects = [{"object": r["object_name"], "count": r["count"]} for r in cursor.fetchall()]
            
            # 3. Scene Distribution
            cursor.execute("""
                SELECT scene_category, COUNT(*) as count 
                FROM history 
                WHERE scene_category IS NOT NULL AND scene_category != ''
                GROUP BY scene_category 
                ORDER BY count DESC
            """)
            scene_distribution = {r["scene_category"]: r["count"] for r in cursor.fetchall()}
            
            # 4. Average Caption Confidence
            cursor.execute("SELECT AVG(caption_confidence) FROM history WHERE caption_confidence IS NOT NULL")
            avg_cap_conf = cursor.fetchone()[0] or 0.0
            
            # 5. Average Detection Confidence
            cursor.execute("SELECT AVG(confidence) FROM object_detections")
            avg_det_conf = cursor.fetchone()[0] or 0.0
            
            # 6. Daily Processing History (last 7 days)
            cursor.execute("""
                SELECT strftime('%Y-%m-%d', timestamp) as date, COUNT(*) as count 
                FROM history 
                GROUP BY date 
                ORDER BY date DESC 
                LIMIT 7
            """)
            recent_activity = [{"date": r["date"], "count": r["count"]} for r in cursor.fetchall()]
            
            return {
                "total_images": total_images,
                "top_objects": top_objects,
                "scene_distribution": scene_distribution,
                "avg_caption_confidence": round(avg_cap_conf * 100, 2),
                "avg_detection_confidence": round(avg_det_conf * 100, 2),
                "recent_activity": recent_activity
            }
