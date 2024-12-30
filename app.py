from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# gejala
diseases = {
    'Bercak Daun': {
        'solution': 'Gunakan fungisida sesuai dosis dan pangkas daun yang terinfeksi.',
        'weight': 0.15  
    },
    'Karat Daun Kopi': {
        'solution': 'Gunakan fungisida, kontrol kelembapan dan hindari penyiraman berlebihan.',
        'weight': 0.2  
    },
    'Fusarium Wilt': {
        'solution': 'Perbaiki drainase tanah dan gunakan fungisida untuk pembusukan akar.',
        'weight': 0.1  
    },
    'Oidium': {
        'solution': 'Gunakan fungisida dan kurangi kelembapan berlebih.',
        'weight': 0.05  
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    answers = request.get_json()
    disease, solution, cf = calculate_cf(answers)
    return jsonify({
        'disease': disease,
        'solution': solution,
        'confidence': cf
    })

def calculate_cf(answers):
    disease_cf = {
        'Bercak Daun': 0.0,
        'Karat Daun Kopi': 0.0,
        'Fusarium Wilt': 0.0,
        'Oidium': 0.0,
    }

    for question, answer in answers.items():
        answer = float(answer)
        for disease in disease_cf:
# hitung cf
            disease_cf[disease] += answer * diseases[disease]['weight']

    max_cf = sum(diseases[d]['weight'] for d in diseases)
    disease_cf = {d: cf / max_cf for d, cf in disease_cf.items()}

    detected_disease = max(disease_cf, key=disease_cf.get)
    disease_solution = diseases[detected_disease]['solution']
    disease_confidence = disease_cf[detected_disease]

    return detected_disease, disease_solution, disease_confidence

if __name__ == '__main__':
    app.run(debug=True)
