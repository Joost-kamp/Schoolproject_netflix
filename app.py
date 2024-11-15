from flask import Flask, render_template, request, session, redirect, \
    url_for

app = Flask(__name__)
app.secret_key = 'geheime_sleutel'  # Zorg ervoor dat deze uniek is voor productie


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/keuzestress', methods=['GET', 'POST'])
def keuzestress():
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice in ['serie', 'film']:
            session['content_type'] = choice
            return redirect(url_for('samen_of_alleen'))
    return render_template('keuzestress.html',
                           message="Wil je een serie of een film kijken?")


@app.route('/samen_of_alleen', methods=['GET', 'POST'])
def samen_of_alleen():
    if request.method == 'POST':
        viewing_choice = request.form.get('viewing_choice')
        if viewing_choice in ['alleen', 'samen']:
            session['viewing_mode'] = viewing_choice
            return redirect(url_for('recommendation'))
    return render_template('samen_of_alleen.html',
                           message="Kijk je alleen of samen?")


@app.route('/recommendation')
def recommendation():
    content_type = session.get('content_type', 'onbekend')
    viewing_mode = session.get('viewing_mode', 'onbekend')
    # Aanbevelingen gebaseerd op keuzes
    recommendations = []
    if content_type == 'film':
        recommendations = ['Inception', 'The Dark Knight',
                           'Interstellar'] if viewing_mode == 'alleen' else [
            'Shrek', 'Avengers: Endgame', 'Frozen']
    elif content_type == 'serie':
        recommendations = ['Breaking Bad', 'Stranger Things',
                           'The Crown'] if viewing_mode == 'alleen' else [
            'Friends', 'The Office', 'Brooklyn Nine-Nine']
    return render_template('recommendation.html',
                           recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug=True)
