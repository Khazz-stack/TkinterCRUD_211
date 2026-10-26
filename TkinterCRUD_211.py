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

def simpan_data(nama, biologi, fisika, inggris, prediksi):
    """Menyimpan satu baris data siswa ke tabel nilai_siswa."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO nilai_siswa "
            "(nama_siswa, biologi, fisika, inggris, prediksi_fakultas) "
            "VALUES (?, ?, ?, ?, ?)",
            (nama, biologi, fisika, inggris, prediksi),
        )

def prediksi_fakultas(biologi, fisika, inggris):
    """Fakultas ditentukan dari nilai yang paling tinggi.

    Jika ada nilai yang sama tinggi, urutan prioritas:
    Biologi > Fisika > Inggris.
    """
    if biologi >= fisika and biologi >= inggris:
        return "Kedokteran"
    if fisika >= inggris:
        return "Teknik"
    return "Bahasa"