import json
import secrets
from Crypto.Random import get_random_bytes


# Générer une clé
key = secrets.token_bytes(16)
iv = get_random_bytes(16)


# Convertir la clé en une représentation hexadécimale
hex_key = key.hex()
hex_iv = iv.hex()

# Créer un dictionnaire contenant la clé
key_dict = {'key': hex_key,'iv' : hex_iv}

# Enregistrer le dictionnaire dans un fichier JSON
with open('key.json', 'w') as json_file:
    json.dump(key_dict, json_file)

print("Clé enregistrée avec succès dans key.json")
