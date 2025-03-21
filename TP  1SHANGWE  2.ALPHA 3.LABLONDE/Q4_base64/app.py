import base64

#  Pour sasir le Message encodé en Base64
message_encode = " "

# Décoder le message
try:
    message_clair = base64.b64decode(message_encode).decode('utf-8')
    # Afficher le message clair
    print("Message clair:", message_clair)
except Exception as e:
    print("Erreur lors du décodage:", e)