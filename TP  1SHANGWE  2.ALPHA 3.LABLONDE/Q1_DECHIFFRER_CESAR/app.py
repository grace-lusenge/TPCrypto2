from flask import Flask, render_template, request
from collections import Counter
import string

app = Flask(__name__)

def dechiffrer_cesar(texte_chiffre, decalage):
    texte_dechiffre = ""
    for char in texte_chiffre:
        if char in string.ascii_letters:
            shifted = ord(char) - decalage
            if char.islower():
                texte_dechiffre += chr((shifted - 97) % 26 + 97)
            else:
                texte_dechiffre += chr((shifted - 65) % 26 + 65)
        else:
            texte_dechiffre += char
    return texte_dechiffre

def analyse_frequentielle(texte_chiffre):
    frequences = Counter(texte_chiffre)
    plus_courant = frequences.most_common(1)[0][0]
    decalage = ord(plus_courant) - ord('E')
    return decalage

@app.route('/', methods=['GET', 'POST'])
def index():
    resultats = []
    if request.method == 'POST':
        texte_chiffre = request.form['texte_chiffre']
        for decalage in range(1, 26):
            texte_dechiffre = dechiffrer_cesar(texte_chiffre, decalage)
            resultats.append((decalage, texte_dechiffre))
        resultats = sorted(resultats, key=lambda x: analyse_frequentielle(x[1]))[:5]
    return render_template('index.html', resultats=resultats)

if __name__ == '__main__':
    app.run(debug=True)
