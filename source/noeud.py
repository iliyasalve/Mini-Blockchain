import json
import os

from uuid import uuid4
from flask import Flask, jsonify, request
from sys import argv

from blockchain import Blockchain
from manipulation_de_cles import generer_cles_ECDSA

app = Flask(__name__)

blockchain = Blockchain()


@app.route('/mien', methods=['GET'])
def mien():
    '''
    Coins minières
    '''

    dernier_bloc  = blockchain.dernier_bloc 
    proof = blockchain.proof_of_work(dernier_bloc)

    blockchain.nouvelle_transaction(
	    cle_privee = cle_privee,
        expediteur = "system", # ici, l'expéditeur est "system" pour signifier que ce noeud a miné un nouveau coin
        destinataire = cle_public,
        montant=1,
    )

    precedent_hachage = blockchain.hash(dernier_bloc )
    bloc = blockchain.nouveau_bloc(proof, precedent_hachage)

	# afficher un message indiquant que la tâche a réussi
    response = {
        'message': "Nouveau bloc forge",
        'index': bloc['index'],
        'transactions': bloc['transactions'],
        'proof': bloc['proof'],
        'precedent_hachage': bloc['precedent_hachage'],
    }
	
    return jsonify(response), 200

	
@app.route('/transactions/nouveau', methods=['POST'])
def nouvelle_transaction():
    '''
    Mise en place d'une nouvelle transaction 
    '''

    valeurs = request.get_json()
	
    # vérifiez que les champs obligatoires sont bien dans les données "POST" 
    required = ['cle_privee', 'expediteur', 'destinataire', 'montant']
    if not all(k in valeurs for k in required):
        return jsonify({'Erreur': 'Valeurs manquantes'}), 400

    index = blockchain.nouvelle_transaction(valeurs['cle_privee'], valeurs['expediteur'], valeurs['destinataire'], valeurs['montant'])

    response = {'message': f'La transaction sera ajoutee au bloc {index}'}

    return jsonify(response), 201

	 
@app.route('/chaine', methods=['GET'])
def chaine_complete():
    '''
    Afficher la blockchain complète et sa longueur
    '''

    response = {
        'chaine': blockchain.chaine,
        'longueur': len(blockchain.chaine),
    }
	
    return jsonify(response), 200


@app.route('/est_valide', methods=['GET'])
def est_valide():
    '''
    Vérifier si Blockchain est valide
    '''

    est_valide = blockchain.chaine_valide(blockchain.chaine)

    if est_valide:
        response = {'message': "La Blockchain est valide."}
    else:
        response = {'message': "La Blockchain n'est pas valide."}

    return jsonify(response), 200


@app.route('/noeuds/enregistrer', methods=['POST'])
def enregistrer_noeuds ():
    '''
    Ajouter un nouveau noeud à la liste des noeuds 
    '''

    valeurs = request.get_json()
    noeuds = valeurs.get('noeuds')
	
    if noeuds is None:
        return jsonify({'Erreur':'Veuillez fournir une liste valide de noeuds'}), 400

	# ajouter des noeuds à la blockchain
    for node in noeuds:
        blockchain.register_node(node)

    response = {
        'message': 'De nouveaux noeuds ont ete ajoutes',
        'total_noeuds': list(blockchain.noeuds),
    }
	
    return jsonify(response), 201


@app.route('/noeuds/resoudre', methods=['GET'])
def consensus():
    '''
    Résolvent les conflits en remplaçant une chaîne par la plus longue du réseau
    '''

    remplace = blockchain.resoudre_conflicts()

	# vérifier si la chaîne doit être remplacée
    if remplace:
        response = {
            'message': 'Chaine a ete remplacee',
            'nouveau_chaine': blockchain.chaine
        }
    else:
        response = {
            'message': 'Chaine fait autorite',
            'chaine': blockchain.chaine
        }

    return jsonify(response), 200
	

@app.route('/pieces_de_coins', methods=['POST'])
def pieces_de_coins_utilisateur():
    '''
    Vérifier des pièces de coins d'un utilisateur
    '''
 
    valeurs = request.get_json()
    destinataire = valeurs.get('id')
	
	# vérifier si le destinataire est vide
    if destinataire is None:
        return jsonify({'Erreur' : 'Veuillez fournir une destinataire valide'}), 400

    response = {
        'somme': blockchain.verifier_pieces_de_coins(blockchain.chaine, destinataire)
    }
	
    return jsonify(response), 201


# lancement du noeud
if __name__ == '__main__':
	
	# obtenir des valeurs de la console
    port = argv[1] # port
    file_cles = argv[2] # le nom du fichier où nous devons enregistrer les clés
    file_path = 'data/' + file_cles + '.data'
	
    # verifier si les clés sont déjà créées
    if not os.path.exists(file_path):
        generer_cles_ECDSA(file_path)

	# lire les clés du fichier reçues
    with open(file_path) as json_file:
        gener_cles = json.load(json_file)
		
	# initialisation des clés
    cle_privee = gener_cles[0]['private']
    cle_public = gener_cles[0]['public']
	
	# lancement du noeud
    app.run(debug=True, port=port)
