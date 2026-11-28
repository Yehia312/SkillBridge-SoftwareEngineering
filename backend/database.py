
import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "skillbridge.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            skills TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def insert_candidate(name, email, skills):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO candidates (name, email, skills)
            VALUES (?, ?, ?)
        """, (name, email, skills))

        connection.commit()

    except sqlite3.IntegrityError:
        raise ValueError("Candidate email already exists!")

    finally:
        connection.close()


def get_all_candidates():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM candidates")
    rows = cursor.fetchall()

    candidates = []

    for row in rows:
        candidates.append({
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "skills": json.loads(row["skills"])
        })

    connection.close()
    return candidates


def update_candidate(candidate_id, name, email, skills):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE candidates
            SET name = ?, email = ?, skills = ?
            WHERE id = ?
        """, (name, email, skills, candidate_id))

        connection.commit()
        return cursor.rowcount > 0

    except sqlite3.IntegrityError:
        raise ValueError("Candidate email already exists!")

    finally:
        connection.close()


def delete_candidate(candidate_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM candidates WHERE id = ?",
        (candidate_id,)
    )

    connection.commit()
    deleted = cursor.rowcount > 0
    connection.close()

    return deleted
