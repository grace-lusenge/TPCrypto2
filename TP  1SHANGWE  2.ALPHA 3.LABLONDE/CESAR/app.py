from flask import Flask, request, render_template

app = Flask(__name__)

def chiffrement_cesar(message, decalage):
    resultat = ""
    for lettre in message:
        if lettre.isalpha():
            decalage_base = ord('A') if lettre.isupper() else ord('a')
            resultat += chr((ord(lettre) - decalage_base + decalage) % 26 + decalage_base)
        else:
            resultat += lettre
    return resultat

@app.route('/', methods=['GET', 'POST'])
def index():
    message_chiffre = ""
    if request.method == 'POST':
        message = request.form['message']
        decalage = int(request.form['decalage'])
        message_chiffre = chiffrement_cesar(message, decalage)
    return render_template('index.html', message_chiffre=message_chiffre)

if __name__ == '__main__':
    app.run(debug=True)
