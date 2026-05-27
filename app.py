from flask import Flask, render_template, request

application = Flask(__name__)

data_pengunjung = []

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

    data = {
        'nama': nama,
        'jumlah': jumlah,
        'jam_mulai': jam_mulai,
        'jam_selesai': jam_selesai
    }

    data_pengunjung.append(data)

    return render_template(
        'rules.html',
        nama=nama
    )


@application.route('/success')
def success():
    return render_template('success.html')


@application.route('/petugas')
def petugas():
    return render_template(
        'petugas.html',
        data_pengunjung=data_pengunjung
    )


if __name__ == '__main__':
    application.run(debug=True)