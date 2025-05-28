# app.py
import sqlite3
from contextlib import closing
from pathlib import Path
import json

DB_PATH = Path(__file__).with_name("data.sqlite3")

def init_db() -> None:
    """테이블과 기본 설정(WAL)만 잡아둡니다."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute("PRAGMA journal_mode=WAL")          # 동시 읽기/쓰기 안전
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                uuid TEXT PRIMARY KEY,
                value TEXT NOT NULL,                     -- JSON 문자열
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_value(uuid_str: int, payload: dict) -> None:
    """uuid가 이미 있으면 갱신, 없으면 삽입(UPSERT)."""
    json_val = json.dumps(payload, ensure_ascii=False)
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute("""
            INSERT INTO user_data(uuid, value)
            VALUES (?, ?)
            ON CONFLICT(uuid) DO UPDATE
            SET value = excluded.value,
                updated_at = CURRENT_TIMESTAMP
        """, (uuid_str, json_val))
        conn.commit()

def get_value(uuid_str: int) -> dict | None:
    """없으면 {}."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.execute("SELECT value FROM user_data WHERE uuid = ?", (uuid_str,))
        row = cur.fetchone()
        return json.loads(row[0]) if row else {}

def update_value(uuid_str: int, **patch) -> None:
    """
    patch에 넘긴 키만 덮어쓰되, 나머지는 그대로 둡니다.
    ex) update_value(uid, score=77, nickname="trinity")
    """
    data = get_value(uuid_str) or {}          # 기존 dict
    data.update(patch)                        # 부분 수정
    save_value(uuid_str, data)                # 기존 save_value 재사용

# ────── 사용 예시 ──────
if __name__ == "__main__":
    init_db()

    #uid = 123
    #save_value(uid, {"score": 42, "nickname": "neo"})
    print(get_value(412827396027187211))        # {'score': 42, 'nickname': 'neo'}
