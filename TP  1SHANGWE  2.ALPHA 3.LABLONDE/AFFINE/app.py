from flask import Flask, request, render_template

app = Flask(__name__)

def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def chiffrement_affine(message, a, b):
    if pgcd(a, 26) != 1:
        return "Chiffrement impossible. Veuillez choisir un nombre a premier avec 26."
    
    resultat = ""
    for lettre in message:
        if lettre.isalpha():
            decalage_base = ord('A') if lettre.isupper() else ord('a')
            resultat += chr((a * (ord(lettre) - decalage_base) + b) % 26 + decalage_base)
        else:
            resultat += lettre
    return resultat

@app.route('/', methods=['GET', 'POST'])
def index():
    message_chiffre = ""
    if request.method == 'POST':
        message = request.form['message']
        a = int(request.form['a'])
        b = int(request.form['b'])
        message_chiffre = chiffrement_affine(message, a, b)
    return render_template('index.html', message_chiffre=message_chiffre)

if __name__ == '__main__':
    app.run(debug=True)
