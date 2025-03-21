from flask import Flask, request, render_template

app = Flask(__name__)

def chiffrement_rail_fence(message, rails):
    if rails == 1:
        return message

    rail = [''] * rails
    direction = None
    row = 0

    for char in message:
        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1

        rail[row] += char
        row += direction

    return ''.join(rail)

@app.route('/', methods=['GET', 'POST'])
def index():
    message_chiffre = ""
    if request.method == 'POST':
        message = request.form['message']
        rails = int(request.form['rails'])
        message_chiffre = chiffrement_rail_fence(message, rails)
    return render_template('index.html', message_chiffre=message_chiffre)

if __name__ == '__main__':
    app.run(debug=True)
