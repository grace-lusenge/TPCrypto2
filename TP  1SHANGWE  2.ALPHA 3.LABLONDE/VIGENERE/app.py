from flask import Flask, request, render_template

app = Flask(__name__)

def chiffrement_vigenere(message, cle):
    resultat = []
    cle = cle.upper()
    cle_longueur = len(cle)
    for i, lettre in enumerate(message):
        if lettre.isalpha():
            decalage_base = ord('A') if lettre.isupper() else ord('a')
            decalage_cle = ord(cle[i % cle_longueur]) - ord('A')
            resultat.append(chr((ord(lettre) - decalage_base + decalage_cle) % 26 + decalage_base))
        else:
            resultat.append(lettre)
    return ''.join(resultat)

@app.route('/', methods=['GET', 'POST'])
def index():
    message_chiffre = ""
    if request.method == 'POST':
        message = request.form['message']
        cle = request.form['cle']
        message_chiffre = chiffrement_vigenere(message, cle)
    return render_template('index.html', message_chiffre=message_chiffre)

if __name__ == '__main__':
    app.run(debug=True)
