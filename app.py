from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['player_name'] = request.form['player_name']
        session['attempts_left'] = 10
        session['number'] = random.randint(1, 100)
        return redirect(url_for('game'))

    return render_template('player.html')


@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'number' not in session or 'attempts_left' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        guess = int(request.form['guess'])
        attempts_left = session['attempts_left']

        if guess == session['number']:
            session.pop('number')
            session.pop('attempts_left')
            return redirect(url_for('result', prompt='Congratulations', message='You guessed the correct number.'))
        elif guess < session['number']:
            message = 'Try again! The number is higher.'
        else:
            message = 'Try again! The number is lower.'

        attempts_left -= 1
        session['attempts_left'] = attempts_left

        if attempts_left == 0:
            session.pop('number')
            session.pop('attempts_left')
            return redirect(url_for('result', prompt='Nice Try...!', message='Game over! You ran out of attempts.'))
        else:
            return render_template('game.html', message=message, attempts_left=attempts_left)

    return render_template('game.html', attempts_left=session['attempts_left'])


@app.route('/result')
def result():
    if 'player_name' in session and 'number' not in session and 'attempts_left' not in session:
        message = request.args.get('message')
        return render_template('result.html', player_name=session['player_name'], message=message)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
