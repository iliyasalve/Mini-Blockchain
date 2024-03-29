import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests

from merkle import merkle_encode
from manipulation_de_cles import message_signer_ECDSA


class Blockchain:
    
    def __init__(self):
	    
        self.transactions_en_cours  = []
        self.chaine = []
        self.noeuds = set() 
        self.all_Hash = []
		
        # créer le bloc de genèse 
        self.nouveau_bloc(proof=101, precedent_hachage='01')


    def nouveau_bloc(self, proof: int, precedent_hachage: str) -> dict:
        '''
        Créer un nouveau bloc dans la Blockchain
        '''

		# créer une liste de hash
        len_chaine = len(self.chaine)
        self.all_Hash.append(precedent_hachage)
        list_hash = self.all_Hash[0:len_chaine+1]
        
        block = {
            'index': len(self.chaine) + 1,
            'timestamp': round(time()),
            'transactions': self.transactions_en_cours,
            'proof': proof,
            'precedent_hachage': precedent_hachage or self.hash(self.chaine[-1]),
            'merkle' : merkle_encode(list_hash),
        }

        self.transactions_en_cours  = [] # réinitialiser la liste actuelle des transactions 

        self.chaine.append(block)
		
        return block
	

    def nouvelle_transaction(self, cle_privee: str, expediteur: str, destinataire: str, montant: int) -> dict:
        '''
        Crée une nouvelle transaction pour aller dans le prochain bloc miné 
        '''
            
        signature, message = message_signer_ECDSA(cle_privee)
		
        self.transactions_en_cours.append({
            'expediteur': expediteur,
            'destinataire': destinataire ,
            'montant': montant,
			'signature': signature.decode(),
            'timestamp_message_info': message,
			
        })

		# renvoyer la valeur du dernier bloc
        return self.dernier_bloc ['index'] + 1


    def verifier_pieces_de_coins(self, blockchain: list, destinataire: str) -> int:
        '''
        Vérification des pièces de coins dont dispose d'un utilisateur
        '''

        somme = 0 

		# rechercher des transaction dans la chaîne
        for i in range(1, len(blockchain)):
            transaction = blockchain[i]['transactions']
            len_transaction = len(transaction)

			# rechercher des coins dans la transaction
            for n in range(len_transaction):
                ligne_transaction = transaction[n]
				
				# vérifier si l'utilisateur trouvé est celui que nous recherchons
                if (ligne_transaction['destinataire'] == destinataire):
                    somme = somme + ligne_transaction['montant'] # ajouter des coins au somme

        return somme


    @property
    def dernier_bloc (self):
        '''
        Renvoie le dernier bloc de la chaîne
        '''

        return self.chaine[-1]


    @staticmethod
    def hash(block: dict) -> str:
        '''
        Crée un hachage SHA-256 d'un bloc 
        '''

        # assurer que le dictionnaire est ordonné, sinon on aura des hachages incohérents 
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

	
    def proof_of_work(self, dernier_bloc: dict) -> int:
        '''
        Algorithme Proof of Work simple 
	    - Trouver un nombre p' tel que hash(pp') contienne 4 zéros en tête
        - Où p est la preuve précédente, et p' est la nouvelle preuve 
        '''

        precedent_proof = dernier_bloc['proof']
        precedent_hash = self.hash(dernier_bloc)
        proof = 0
		
		# vérifie si le résultat renvoyé est faux
        while not self.proof_valide(precedent_proof, proof, precedent_hash):
            proof += 1 # ajouter un en cas de fausse réponse

        return proof

	
    @staticmethod
    def proof_valide(precedent_proof: int, proof: int, precedent_hash: str) -> bool:
        '''
        Valide la preuve pour proof_of_work
        - envoyer vrai si la valeur de résultat de hachage contient-il 4 zéros en tête
        - sinon renvoyer faux
        '''

        deviner = f'{precedent_proof}{proof}{precedent_hash}'.encode() #encoder les valeurs
        deviner_hachage = hashlib.sha256(deviner).hexdigest() # obtenir le résultat de hachage
		
        return deviner_hachage[:4] == "0000"
		
	
    def register_node(self, address: str):
        '''
        Ajouter un nouveau noeud à la liste des noeuds 
        '''

        parsed_url = urlparse(address)
		
		# si l'adresse contient un nom de domaine (ex: 'https://example.com:80/search/', ou nom de domaine est 'example.com:80')
        if parsed_url.netloc:
            self.noeuds.add(parsed_url.netloc)
		
		# ou si l'adresse est un chemin (ex: 'example.com/search/', ou chemin est 'example.com/search/')
        elif parsed_url.path:
            self.noeuds.add(parsed_url.path)
		
		# sinon nous obtenons une erreur
        else:
            raise ValueError('Invalid URL')

	
    def chaine_valide(self, chaine: list) -> bool:
        '''
        Déterminer si une blockchain donnée est valide 
        - envoyer vrai si le hachage du bloc est correct et la preuve de travail est correcte
        - sinon renvoyer faux
        '''

        dernier_bloc  = chaine[0]
        index_actuel = 1

		# faire la boucle jusqu'à ce que toute la chaîne ait été explorée
        while index_actuel < len(chaine):
		
            block = chaine[index_actuel]
            dernier_bloc_hash = self.hash(dernier_bloc)

            # vérifiez que le hachage du bloc est correct 
            if block['precedent_hachage'] != dernier_bloc_hash:
                return False

            # vérifiez que la preuve de travail est correcte 
            if not self.proof_valide(dernier_bloc ['proof'], block['proof'], dernier_bloc_hash):
                return False

            dernier_bloc  = block
            index_actuel += 1

        return True


    def resoudre_conflicts(self) -> bool:
        '''
        Résolvent les conflits en remplaçant une chaîne par la plus longue du réseau
        - renvoyer vrai si on trouve la chaine plus longue que la chaine actuelle
        - sinon renvoyer faux
        '''

        voisins = self.noeuds
        nouveau_chaine = None
        max_longueur  = len(self.chaine)

        # saisissez et vérifiez les chaînes de tous les noeuds du réseau actuel
        for node in voisins:
			
            response = requests.get(f'http://{node}/chaine') # obtenir des valeurs de noeud
			
            if response.status_code == 200:
                longueur_voisin_node  = response.json()['longueur']
                chaine_voisin_node  = response.json()['chaine']

                if longueur_voisin_node > max_longueur and self.chaine_valide(chaine_voisin_node):
                    max_longueur  = longueur_voisin_node 
                    nouveau_chaine = chaine_voisin_node

        if nouveau_chaine:
            self.chaine = nouveau_chaine # remplacer la chaîne
            return True

        return False