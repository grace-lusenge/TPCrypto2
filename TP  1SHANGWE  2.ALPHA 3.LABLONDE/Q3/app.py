# Liste d'entiers représentant les codes ASCII
ascii_codes = [78, 79, 85, 83, 32, 89, 32, 65, 76, 76, 79, 78, 83, 32, 68, 69, 77, 65, 73, 78, 32, 77, 65, 84, 73, 78]

# Convertir chaque entier en caractère ASCII
message_clair = ''.join([chr(code) for code in ascii_codes])

# Afficher le message clair
print("Message clair:", message_clair)