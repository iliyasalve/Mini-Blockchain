import time
import base64
import ecdsa
import json


def generer_cles_ECDSA(file_path: str):
    '''
    Générer des clés privées et publiques
    '''

    cle_signe = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) # creation d'un signe (clé privée)
    cle_privee = cle_signe.to_string().hex() # convertir la clé privée en hexadécimal
	
    cle_verification = cle_signe.get_verifying_key() # creation de la clé de vérification (clé publique)
    cle_publique = cle_verification.to_string().hex() # convertir la clé publique en hexadécimal
    cle_publique = base64.b64encode(bytes.fromhex(cle_publique)) # encoder la clé publique 

    enregistrer_cles(file_path, cle_privee, cle_publique) 


def enregistrer_cles(file_path: str, cle_privee: str, cle_publique: str):
    '''
    Enregistrer les clés dans un fichier
    '''

    list_cles = [] 

    list_cles.append({
        'private': cle_privee,
        'public': cle_publique.decode()
    })

    with open(file_path, "w") as f:
        json.dump(list_cles, f)

    print(f"\nVotre nouvelles cles sont maintenant dans le fichier {file_path}\n")

	
def message_signer_ECDSA(cle_privee: str) -> tuple[str, str]:
    '''
    Créer une signature et un message où indiquer le timestamp du creation d'une signature
    '''

    message = str(round(time.time())) # obtenir l'horodatage et arrondissez-le
    bmessage = message.encode() # encoder le message

    cle_signe = ecdsa.SigningKey.from_string(bytes.fromhex(cle_privee), curve=ecdsa.SECP256k1) # creation d'un signe
    signature = base64.b64encode(cle_signe.sign(bmessage)) # encoder la signature
	
    return signature, message