from flask import Flask, render_template, request
import sqlite3

application = Flask(__name__)


def init_db():
    conn = sqlite3.connect('aquavista.db')
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

    conn = sqlite3.connect('aquavista.db')
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
    conn = sqlite3.connect('aquavista.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM reservasi')
    data_pengunjung = cursor.fetchall()

    conn.close()

    return render_template(
        'petugas.html',
        data_pengunjung=data_pengunjung
    )


if __name__ == '__main__':
    init_db()
    application.run(debug=True)