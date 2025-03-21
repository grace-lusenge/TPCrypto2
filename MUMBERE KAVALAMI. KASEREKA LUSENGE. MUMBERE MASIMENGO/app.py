from flask import Flask, render_template, request
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from collections import Counter
import base64

app = Flask(__name__)

# Fréquence des lettres en français (pour l'analyse fréquentielle)
FREQ_FR = {
    'A': 8.15, 'B': 0.97, 'C': 3.15, 'D': 3.73, 'E': 17.39,
    'F': 1.12, 'G': 0.97, 'H': 0.85, 'I': 7.31, 'J': 0.45,
    'K': 0.02, 'L': 5.69, 'M': 2.87, 'N': 7.12, 'O': 5.28,
    'P': 2.77, 'Q': 1.21, 'R': 6.64, 'S': 8.14, 'T': 7.22,
    'U': 6.38, 'V': 1.64, 'W': 0.03, 'X': 0.41, 'Y': 0.28,
    'Z': 0.15
}

# Fonction pour déchiffrer un message avec l'algorithme de César
def decrypt_caesar(ciphertext, shift):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            shift_amount = shift % 26
            decrypted_char = chr((ord(char.upper()) - 65 - shift_amount) % 26 + 65)
            plaintext += decrypted_char
        else:
            plaintext += char
    return plaintext

# Fonction pour calculer le score de fréquence d'un texte
def frequency_score(text):
    text = text.upper()
    letter_counts = Counter(text)
    total_letters = sum(letter_counts.values())
    score = 0
    for letter, count in letter_counts.items():
        if letter in FREQ_FR:
            observed_freq = (count / total_letters) * 100
            expected_freq = FREQ_FR[letter]
            score += abs(observed_freq - expected_freq)
    return score

# Fonction pour trouver les 5 déchiffrements les plus probables
def find_top_5_decryptions(ciphertext):
    results = []
    for shift in range(26):
        decrypted_text = decrypt_caesar(ciphertext, shift)
        score = frequency_score(decrypted_text)
        results.append((decrypted_text, score, shift))
    
    # Trier les résultats par score (le plus bas est le meilleur)
    results.sort(key=lambda x: x[1])
    
    # Retourner les 5 meilleurs résultats
    return results[:5]

# Fonction pour chiffrer un message avec AES
def encrypt_aes(plaintext, key, mode, iv=None):
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    plaintext = pad(plaintext, AES.block_size)
    
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, AES.MODE_ECB)
    elif mode == AES.MODE_CBC:
        cipher = AES.new(key, AES.MODE_CBC, iv)
    elif mode == AES.MODE_CTR:
        if len(iv) != 8:
            raise ValueError("Le nonce doit être de 8 bytes pour le mode CTR")
        cipher = AES.new(key, AES.MODE_CTR, nonce=iv)
    elif mode == AES.MODE_OFB:
        cipher = AES.new(key, AES.MODE_OFB, iv)
    elif mode == AES.MODE_CFB:
        cipher = AES.new(key, AES.MODE_CFB, iv)
    else:
        raise ValueError("Mode de chiffrement non supporté")
    
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

# Fonction pour déchiffrer un message avec AES
def decrypt_aes(ciphertext, key, mode, iv=None):
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, AES.MODE_ECB)
    elif mode == AES.MODE_CBC:
        cipher = AES.new(key, AES.MODE_CBC, iv)
    elif mode == AES.MODE_CTR:
        if len(iv) != 8:
            raise ValueError("Le nonce doit être de 8 bytes pour le mode CTR")
        cipher = AES.new(key, AES.MODE_CTR, nonce=iv)
    elif mode == AES.MODE_OFB:
        cipher = AES.new(key, AES.MODE_OFB, iv)
    elif mode == AES.MODE_CFB:
        cipher = AES.new(key, AES.MODE_CFB, iv)
    else:
        raise ValueError("Mode de chiffrement non supporté")
    
    plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(plaintext, AES.block_size)
    return plaintext.decode('utf-8')

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour le déchiffrement de César
@app.route('/cesar', methods=['GET', 'POST'])
def cesar():
    if request.method == 'POST':
        ciphertext = request.form['ciphertext']
        results = find_top_5_decryptions(ciphertext)
        return render_template('cesar.html', results=results)
    return render_template('cesar.html')

# Route pour le chiffrement/déchiffrement AES
@app.route('/aes', methods=['GET', 'POST'])
def aes():
    if request.method == 'POST':
        action = request.form['action']
        plaintext = request.form['plaintext']
        key = request.form['key'].encode('utf-8')
        mode = int(request.form['mode'])
        iv = request.form['iv'].encode('utf-8') if 'iv' in request.form else None
        
        modes = {
            1: AES.MODE_ECB,
            2: AES.MODE_CBC,
            3: AES.MODE_CTR,
            4: AES.MODE_OFB,
            5: AES.MODE_CFB
        }
        mode = modes.get(mode, AES.MODE_ECB)
        
        try:
            if action == 'encrypt':
                ciphertext = encrypt_aes(plaintext, key, mode, iv)
                return render_template('aes.html', result=ciphertext.hex())
            elif action == 'decrypt':
                plaintext = decrypt_aes(bytes.fromhex(plaintext), key, mode, iv)
                return render_template('aes.html', result=plaintext)
        except Exception as e:
            return render_template('aes.html', error=str(e))
    
    return render_template('aes.html')

# Route pour la conversion ASCII
@app.route('/ascii', methods=['GET', 'POST'])
def ascii_conversion():
    if request.method == 'POST':
        try:
            # Récupérer la liste de nombres depuis le formulaire
            numbers = request.form['numbers']
            # Convertir la chaîne en une liste d'entiers
            numbers_list = list(map(int, numbers.split(',')))
            # Convertir les nombres en caractères ASCII
            message = ''.join([chr(num) for num in numbers_list])
            return render_template('ascii.html', message=message, numbers=numbers)
        except Exception as e:
            return render_template('ascii.html', error=str(e))
    return render_template('ascii.html')


# Fonction pour ajouter le padding manquant à une chaîne Base64
def add_padding(base64_string):
    padding = len(base64_string) % 4
    if padding:
        base64_string += '=' * (4 - padding)
    return base64_string

# Route pour le décodage Base64
@app.route('/base64', methods=['GET', 'POST'])
def base64_decoding():
    if request.method == 'POST':
        try:
            # Récupérer le message codé en Base64 depuis le formulaire
            encoded_message = request.form['encoded_message'].strip()  # Supprimer les espaces inutiles
            # Ajouter le padding manquant si nécessaire
            encoded_message = add_padding(encoded_message)
            # Décoder le message Base64 en bytes
            decoded_bytes = base64.b64decode(encoded_message)
            
            # Essayer de décoder en UTF-8
            try:
                decoded_message = decoded_bytes.decode('utf-8')
            except UnicodeDecodeError:
                # Si UTF-8 échoue, essayer ISO-8859-1 (Latin-1)
                try:
                    decoded_message = decoded_bytes.decode('iso-8859-1')
                except UnicodeDecodeError:
                    # Si ISO-8859-1 échoue aussi, afficher les données brutes en hexadécimal
                    decoded_message = f"Données binaires (hexadécimal) : {decoded_bytes.hex()}"
            
            return render_template('base64.html', decoded_message=decoded_message, encoded_message=encoded_message)
        except Exception as e:
            return render_template('base64.html', error=str(e))
    return render_template('base64.html')

# Route pour la conversion binaire
@app.route('/binary', methods=['GET', 'POST'])
def binary_conversion():
    if request.method == 'POST':
        try:
            # Récupérer la représentation binaire depuis le formulaire
            binary_input = request.form['binary_input'].strip()  # Supprimer les espaces inutiles
            # Convertir la représentation binaire en une chaîne de caractères
            binary_list = binary_input.split()
            ascii_chars = [chr(int(binary, 2)) for binary in binary_list]
            decoded_message = ''.join(ascii_chars)
            return render_template('binary.html', decoded_message=decoded_message, binary_input=binary_input)
        except Exception as e:
            return render_template('binary.html', error=str(e))
    return render_template('binary.html')

# Route pour les méthodes cryptanalytiques
@app.route('/cryptanalysis')
def cryptanalysis():
    return render_template('cryptanalysis.html')

# Démarrer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)