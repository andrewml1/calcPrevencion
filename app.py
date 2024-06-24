from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def findrisc_form():
    if request.method == 'POST':
        age = int(request.form['age'])
        bmi = float(request.form['bmi'])
        waist = float(request.form['waist'])
        physical_activity = int(request.form['physical_activity'])
        fruit_vegetables = int(request.form['fruit_vegetables'])
        hypertension_meds = int(request.form['hypertension_meds'])
        high_glucose = int(request.form['high_glucose'])
        family_diabetes = int(request.form['family_diabetes'])

        score = age + bmi + waist + physical_activity + fruit_vegetables + hypertension_meds + high_glucose + family_diabetes

        if score < 7:
            risk = "Bajo (aproximadamente 1% de riesgo en los próximos 10 años)"
        elif 7 <= score <= 11:
            risk = "Ligeramente elevado (aproximadamente 4%)"
        elif 12 <= score <= 14:
            risk = "Moderado (aproximadamente 16%)"
        elif 15 <= score <= 20:
            risk = "Alto (aproximadamente 33%)"
        else:
            risk = "Muy alto (aproximadamente 50%)"

        return render_template('form.html', score=score, risk=risk)

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
