from flask import Flask, request, render_template
import numpy as np

app = Flask(__name__)

def chiffrement_hill(message, key):
    key_matrix = np.array(key).reshape(2, 2)
    message_vector = [ord(char) - ord('A') for char in message.upper()]
    
    if len(message_vector) % 2 != 0:
        message_vector.append(ord('X') - ord('A'))

    message_matrix = np.array(message_vector).reshape(-1, 2).T
    cipher_matrix = np.dot(key_matrix, message_matrix) % 26
    cipher_text = ''.join(chr(int(num) + ord('A')) for num in cipher_matrix.T.flatten())
    
    return cipher_text

@app.route('/', methods=['GET', 'POST'])
def index():
    message_chiffre = ""
    if request.method == 'POST':
        message = request.form['message']
        key = list(map(int, request.form['key'].split(',')))
        message_chiffre = chiffrement_hill(message, key)
    return render_template('index.html', message_chiffre=message_chiffre)

if __name__ == '__main__':
    app.run(debug=True)
