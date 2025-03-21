from flask import Flask, render_template, request
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

app = Flask(__name__)

MODES = {
    'ECB': AES.MODE_ECB,
    'CBC': AES.MODE_CBC,
    'CTR': AES.MODE_CTR,
    'OFB': AES.MODE_OFB,
    'CFB': AES.MODE_CFB
}

def chiffrer_aes(texte, cle, mode):
    cipher = AES.new(cle, mode)
    if mode == AES.MODE_ECB:
        texte_chiffre = cipher.encrypt(pad(texte.encode(), AES.block_size))
    else:
        iv = cipher.iv
        texte_chiffre = iv + cipher.encrypt(pad(texte.encode(), AES.block_size))
    return base64.b64encode(texte_chiffre).decode()

def dechiffrer_aes(texte_chiffre, cle, mode):
    texte_chiffre = base64.b64decode(texte_chiffre)
    if mode == AES.MODE_ECB:
        cipher = AES.new(cle, mode)
        texte_dechiffre = unpad(cipher.decrypt(texte_chiffre), AES.block_size)
    else:
        iv = texte_chiffre[:AES.block_size]
        cipher = AES.new(cle, mode, iv=iv)
        texte_dechiffre = unpad(cipher.decrypt(texte_chiffre[AES.block_size:]), AES.block_size)
    return texte_dechiffre.decode()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        texte = request.form['texte']
        cle = request.form['cle'].encode()
        mode = MODES[request.form['mode']]
        action = request.form['action']
        if action == 'Chiffrer':
            result = chiffrer_aes(texte, cle, mode)
        elif action == 'Déchiffrer':
            result = dechiffrer_aes(texte, cle, mode)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
