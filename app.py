# from flask import Flask, render_template, request, jsonify

# app = Flask(__name__)

# # Definisi penyakit, solusi, dan bobot penyakit
# diseases = {
#     'Bercak Daun': {
#         'solution': 'Gunakan fungisida sesuai dosis dan pangkas daun yang terinfeksi.',
#         'weight': 0.3  # Bobot penyakit Bercak Daun
#     },
#     'Karat Daun Kopi': {
#         'solution': 'Gunakan fungisida, kontrol kelembapan dan hindari penyiraman berlebihan.',
#         'weight': 0.4  # Bobot penyakit Karat Daun Kopi
#     },
#     'Fusarium Wilt': {
#         'solution': 'Perbaiki drainase tanah dan gunakan fungisida untuk pembusukan akar.',
#         'weight': 0.2  # Bobot penyakit Fusarium Wilt
#     },
#     'Oidium': {
#         'solution': 'Gunakan fungisida dan kurangi kelembapan berlebih.',
#         'weight': 0.1  # Bobot penyakit Oidium
#     }
# }

# # Route utama untuk halaman awal
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Endpoint untuk menerima jawaban dan menghitung penyakit
# @app.route('/diagnose', methods=['POST'])
# def diagnose():
#     answers = request.get_json()
#     disease, solution, cf = calculate_cf(answers)
#     return jsonify({
#         'disease': disease,
#         'solution': solution,
#         'confidence': cf
#     })

# # Fungsi untuk menghitung Certainty Factor (CF)
# def calculate_cf(answers):
#     # Menginisialisasi CF penyakit dengan nilai awal 0.0
#     disease_cf = {
#         'Bercak Daun': 0.0,
#         'Karat Daun Kopi': 0.0,
#         'Fusarium Wilt': 0.0,
#         'Oidium': 0.0,
#     }

#     # Tentukan bobot dan penyakit yang sesuai dengan jawaban
#     for question, answer in answers.items():
#         # Pembobotan berdasarkan jawaban

#         if answer == '1':  # Ya
#             disease_cf['Bercak Daun'] += (0.3 + diseases['Bercak Daun']['weight'])  # Menambahkan bobot penyakit
#             disease_cf['Karat Daun Kopi'] += (0.4 + diseases['Karat Daun Kopi']['weight'])
#             disease_cf['Fusarium Wilt'] += (0.2 + diseases['Fusarium Wilt']['weight'])
#             disease_cf['Oidium'] += (0.2 + diseases['Oidium']['weight'])
#         elif answer == '0.7':  # Mungkin Iya
#             disease_cf['Bercak Daun'] += (0.2 + diseases['Bercak Daun']['weight'])
#             disease_cf['Karat Daun Kopi'] += (0.3 + diseases['Karat Daun Kopi']['weight'])
#             disease_cf['Fusarium Wilt'] += (0.1 + diseases['Fusarium Wilt']['weight'])
#             disease_cf['Oidium'] += (0.2 + diseases['Oidium']['weight'])
#         elif answer == '0.4':  # Mungkin Tidak
#             disease_cf['Bercak Daun'] += (0.1 + diseases['Bercak Daun']['weight'])
#             disease_cf['Karat Daun Kopi'] += (0.1 + diseases['Karat Daun Kopi']['weight'])
#             disease_cf['Fusarium Wilt'] += (0.05 + diseases['Fusarium Wilt']['weight'])
#             disease_cf['Oidium'] += (0.1 + diseases['Oidium']['weight'])
#         elif answer == '0':  # Tidak
#             disease_cf['Bercak Daun'] += (0.05 + diseases['Bercak Daun']['weight'])
#             disease_cf['Karat Daun Kopi'] += (0.05 + diseases['Karat Daun Kopi']['weight'])
#             disease_cf['Fusarium Wilt'] += (0.0 + diseases['Fusarium Wilt']['weight'])
#             disease_cf['Oidium'] += (0.05 + diseases['Oidium']['weight'])

#     # Tentukan penyakit dengan CF tertinggi
#     detected_disease = max(disease_cf, key=disease_cf.get)
#     disease_solution = diseases[detected_disease]['solution']
#     disease_confidence = disease_cf[detected_disease]

#     return detected_disease, disease_solution, disease_confidence

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load data dari file JSON
with open('data/soal.json', 'r') as f:
    questions = json.load(f)

with open('data/gejala.json', 'r') as f:
    symptoms = json.load(f)

with open('data/solusi.json', 'r') as f:
    solutions = json.load(f)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def process_diagnosis():  # Nama fungsi diubah dari diagnose ke process_diagnosis
    answers = request.get_json()
    disease, solution, cf = calculate_cf(answers)
    return jsonify({
        'disease': disease,
        'solution': solution,
        'confidence': cf
    })



def calculate_cf(answers):
    # Load gejala dari gejala.json
    with open('gejala.json', 'r') as f:
        gejala = json.load(f)

    # Menginisialisasi CF penyakit
    disease_cf = {disease: 0.0 for disease in gejala}

    # Perhitungan CF berdasarkan jawaban
    for question_id, answer in answers.items():
        for disease, data in gejala.items():
            if question_id in data['gejala']:  # Hanya gejala relevan
                disease_cf[disease] += float(answer) * data['weight']

    # Tentukan penyakit dengan CF tertinggi
    detected_disease = max(disease_cf, key=disease_cf.get)
    disease_solution = diseases[detected_disease]['solution']
    disease_confidence = disease_cf[detected_disease]

    return detected_disease, disease_solution, disease_confidence


@app.route('/diagnose', methods=['POST'])
def diagnose():
    answers = request.get_json()

    # Validasi apakah semua pertanyaan dijawab
    if len(answers) < len(questions):  # Pastikan semua pertanyaan dijawab
        return jsonify({
            'error': 'Belum semua pertanyaan dijawab.'
        }), 400

    disease, solution, cf = calculate_cf(answers)
    return jsonify({
        'disease': disease,
        'solution': solution,
        'confidence': cf
    })
