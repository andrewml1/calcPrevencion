import os
from flask import Flask, render_template, request
from basedatos import guardar_datos, credenciales

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def findrisc_form():
    if request.method == 'POST':
        id_number = request.form['id_number']
        age = int(request.form['age'])
        height = float(request.form['height']) / 100  # convertir cm a metros
        weight = float(request.form['weight'])
        waist = float(request.form['waist'])  # Nuevo: perímetro abdominal en cm
        bmi = weight / (height * height)

        # Determinación de puntos basados en IMC
        if bmi < 25:
            bmi_score = 0
        elif 25 <= bmi < 30:
            bmi_score = 1
        else:
            bmi_score = 3

        # Determinación de puntos basados en perímetro abdominal
        if waist < 94 and request.form.get('gender') == 'male':
            waist_score = 0
        elif 94 <= waist <= 102 and request.form.get('gender') == 'male':
            waist_score = 3
        elif waist > 102 and request.form.get('gender') == 'male':
            waist_score = 4
        elif waist < 80 and request.form.get('gender') == 'female':
            waist_score = 0
        elif 80 <= waist <= 88 and request.form.get('gender') == 'female':
            waist_score = 3
        elif waist > 88 and request.form.get('gender') == 'female':
            waist_score = 4

        physical_activity = int(request.form['physical_activity'])
        fruit_vegetables = int(request.form['fruit_vegetables'])
        hypertension_meds = int(request.form['hypertension_meds'])
        high_glucose = int(request.form['high_glucose'])
        family_diabetes = int(request.form['family_diabetes'])

        # Determinación de puntos basados en edad
        if age < 45:
            age_score = 0
        elif 45 <= age < 55:
            age_score = 2
        elif 55 <= age < 65:
            age_score = 3
        else:
            age_score = 4

        score = age_score + bmi_score + waist_score + physical_activity + fruit_vegetables + hypertension_meds + high_glucose + family_diabetes

        if score < 7:
            risk = "Bajo (aproximadamente 1% de riesgo en los próximos 10 años)"
        elif 7 <= score <= 11:
            risk = "Ligeramente elevado (aproximadamente 4% de riesgo en los próximos 10 años)"
        elif 12 <= score <= 14:
            risk = "Moderado (aproximadamente 16% de riesgo en los próximos 10 años)"
        elif 15 <= score <= 20:
            risk = "Alto (aproximadamente 33% de riesgo en los próximos 10 años)"
        else:
            risk = "Muy alto (aproximadamente 50% de riesgo en los próximos 10 años)"

        baseDatos="prosalco"

        cred = credenciales(baseDatos)

        guardar_datos(id_number, age, height, weight, waist, request.form['gender'], bmi_score, waist_score,
                      physical_activity, fruit_vegetables, hypertension_meds, high_glucose,
                      family_diabetes, age_score, score, risk, bmi, cred)


        return render_template('form.html', score=score, risk=risk, id_number=id_number, bmi=round(bmi, 2))

    return render_template('form.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000))
