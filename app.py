from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VENDOR_DIR = os.path.join(BASE_DIR, 'vendor')
if VENDOR_DIR not in sys.path:
    sys.path.insert(0, VENDOR_DIR)

application = Flask(__name__)

application.config['DB_NAME'] = os.path.join(BASE_DIR, 'database.db')


def open_db():
    conn = sqlite3.connect(application.config['DB_NAME'])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = open_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservasi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            jumlah INTEGER NOT NULL,
            jam_mulai TEXT NOT NULL,
            jam_selesai TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/form')
def form():
    return render_template('form.html')


@application.route('/submit', methods=['POST'])
def submit():
    nama = request.form['nama']
    jumlah = request.form['jumlah']
    jam_mulai = request.form['jam_mulai']
    jam_selesai = request.form['jam_selesai']

    conn = open_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO reservasi (nama, jumlah, jam_mulai, jam_selesai)
        VALUES (?, ?, ?, ?)
    ''', (nama, jumlah, jam_mulai, jam_selesai))

    conn.commit()
    conn.close()

    return render_template('rules.html', nama=nama)


@application.route('/success')
def success():
    return render_template('success.html')


@application.route('/petugas')
def petugas():
    conn = open_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM reservasi')
    data_pengunjung = cursor.fetchall()

    conn.close()

    return render_template(
        'petugas.html',
        data_pengunjung=data_pengunjung
    )


@application.route('/ubah/<int:id>', methods=['GET', 'POST'])
def ubah(id):
    conn = open_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        nama = request.form['nama']
        jumlah = request.form['jumlah']
        jam_mulai = request.form['jam_mulai']
        jam_selesai = request.form['jam_selesai']

        cursor.execute('''
            UPDATE reservasi
            SET nama = ?, jumlah = ?, jam_mulai = ?, jam_selesai = ?
            WHERE id = ?
        ''', (nama, jumlah, jam_mulai, jam_selesai, id))

        conn.commit()
        conn.close()

        return redirect(url_for('petugas'))

    cursor.execute('SELECT * FROM reservasi WHERE id = ?', (id,))
    data = cursor.fetchone()

    conn.close()

    return render_template('ubah.html', data=data)


@application.route('/hapus/<int:id>')
def hapus(id):
    conn = open_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM reservasi WHERE id = ?', (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('petugas'))


init_db()


if __name__ == '__main__':
    application.run(debug=True)