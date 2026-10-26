import sqlite3
import tkinter as tk
from tkinter import messagebox

DB_NAME = "nilai_siswa.db"

def buat_tabel():
    """Membuat tabel nilai_siswa jika belum ada."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS nilai_siswa (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_siswa        TEXT    NOT NULL,
                biologi           REAL    NOT NULL,
                fisika            REAL    NOT NULL,
                inggris           REAL    NOT NULL,
                prediksi_fakultas TEXT    NOT NULL
            )
            """
        )