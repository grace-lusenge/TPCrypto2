# Entrer la Représentation binaire
binary_message = " "

# Séparer les groupes de 8 bits
binary_list = binary_message.split()

# Convertir chaque groupe de 8 bits en caractère ASCII
message_clair = ''.join([chr(int(binary, 2)) for binary in binary_list])

# Afficher le message clair
print("Message clair:", message_clair)