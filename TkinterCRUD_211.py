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

class Aplikasi:
    FIELD = [
        ("Nama Siswa", "nama"),
        ("Biologi", "biologi"),
        ("Fisika", "fisika"),
        ("Inggris", "inggris"),
    ]
    def __init__(self, root):
        self.root = root
        root.title("Prediksi Fakultas")
        root.resizable(False, False)

        tk.Label(root, text="Aplikasi Prediksi Fakultas",
                font=("Arial", 16, "bold")).pack(pady=(15, 5))

        form = tk.Frame(root)
        form.pack(padx=20, pady=10)

        self.entry = {}
        for baris, (teks, kunci) in enumerate(self.FIELD):
            tk.Label(form, text=teks + ":", anchor="e", width=12).grid(
                row=baris, column=0, padx=5, pady=5)
            e = tk.Entry(form, width=25)
            e.grid(row=baris, column=1, padx=5, pady=5)
            self.entry[kunci] = e

    def baca_nilai(self, kunci):
        """Mengambil nilai angka 0-100 dari entry, error jika tidak valid."""
        teks = self.entry[kunci].get().strip().replace(",", ".")
        try:
            nilai = float(teks)
        except ValueError:
            raise ValueError(f"Nilai {kunci.capitalize()} harus berupa angka.")
        if not 0 <= nilai <= 100:
            raise ValueError(f"Nilai {kunci.capitalize()} harus antara 0 dan 100.")
        return nilai

    def submit(self):
        nama = self.entry["nama"].get().strip()
        if not nama:
            messagebox.showwarning("Peringatan", "Nama siswa harus diisi.")
            return

        try:
            biologi = self.baca_nilai("biologi")
            fisika = self.baca_nilai("fisika")
            inggris = self.baca_nilai("inggris")
        except ValueError as err:
            messagebox.showwarning("Peringatan", str(err))
            return

        hasil = prediksi_fakultas(biologi, fisika, inggris)
        simpan_data(nama, biologi, fisika, inggris, hasil)

        self.label_hasil.config(text=f"Prediksi Fakultas: {hasil}")
        messagebox.showinfo("Berhasil", f"Data {nama} berhasil disimpan.")
        self.kosongkan_form()

    def kosongkan_form(self):
        for e in self.entry.values():
            e.delete(0, tk.END)
        self.entry["nama"].focus()