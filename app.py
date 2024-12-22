from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Definisi penyakit dan solusi
diseases = {
    'Bercak Daun': {
        'cf': 0.8,
        'solution': 'Gunakan fungisida sesuai dosis dan pangkas daun yang terinfeksi.'
    },
    'Karat Daun Kopi': {
        'cf': 0.9,
        'solution': 'Gunakan fungisida, kontrol kelembapan dan hindari penyiraman berlebihan.'
    },
    'Fusarium Wilt': {
        'cf': 0.7,
        'solution': 'Perbaiki drainase tanah dan gunakan fungisida untuk pembusukan akar.'
    },
    'Oidium': {
        'cf': 0.75,
        'solution': 'Gunakan fungisida dan kurangi kelembapan berlebih.'
    }
}

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint untuk menerima jawaban dan menghitung penyakit
@app.route('/diagnose', methods=['POST'])
def diagnose():
    answers = request.get_json()
    disease, solution, cf = calculate_cf(answers)
    return jsonify({
        'disease': disease,
        'solution': solution,
        'confidence': cf
    })

# Fungsi untuk menghitung Certainty Factor (CF)
def calculate_cf(answers):
    disease_cf = {
        'Bercak Daun': 0.0,
        'Karat Daun Kopi': 0.0,
        'Fusarium Wilt': 0.0,
        'Oidium': 0.0,
    }

    # Tentukan bobot dan penyakit yang sesuai dengan jawaban
    for question, answer in answers.items():
        if answer == '1':  # Ya
            disease_cf['Bercak Daun'] += 0.1
            disease_cf['Karat Daun Kopi'] += 0.15
            disease_cf['Fusarium Wilt'] += 0.05
            disease_cf['Oidium'] += 0.1
        elif answer == '0.7':  # Mungkin Iya
            disease_cf['Bercak Daun'] += 0.07
            disease_cf['Karat Daun Kopi'] += 0.1
            disease_cf['Fusarium Wilt'] += 0.03
            disease_cf['Oidium'] += 0.07
        elif answer == '0.4':  # Mungkin Tidak
            disease_cf['Bercak Daun'] += 0.03
            disease_cf['Karat Daun Kopi'] += 0.05
            disease_cf['Fusarium Wilt'] += 0.02
            disease_cf['Oidium'] += 0.05

    # Tentukan penyakit dengan CF tertinggi
    detected_disease = max(disease_cf, key=disease_cf.get)
    disease_solution = diseases[detected_disease]['solution']
    disease_confidence = disease_cf[detected_disease]

    return detected_disease, disease_solution, disease_confidence

if __name__ == '__main__':
    app.run(debug=True)
