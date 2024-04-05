import os

# remplacer la barre oblique inverse par la valeur pour éviter l'erreur
# SyntaxError: f-string expression part cannot include a backslash 
backslash = "\\"


if __name__ == '__main__':

	# message de bienvenue 
	print("\n\n ##### Bienvenue sur l'application mini-Blockchain! #####")
	input("\nAppuyez sur Entrée pour continuer...")

	while True:
		
		# effacer l'écran 
		os.system('cls' if os.name=='nt' else 'clear')
		
		# menu du programme 
		print(f"\n ### Menu du programme ### \n\n"
				f"1: Coins minières \n" 
				f"2: Faire une nouvelle transaction\n"
				f"3: Afficher la blockchain complète\n"
				f"4: Vérifier si la blockchain est valide\n"
				f"5: Ajouter un nouveau noeud à la liste des noeuds\n"
				f"6: Résout les conflits\n"
				f"7: Vérifier des pièces de coins d'un utilisateur\n"
				f"8: Terminer le programme")
		
		# sélection d'opération 
		cmd = input("\nChoisissez l'opération souhaitée: ")
		print("\n")

		match cmd:

			case "1": # coins minières

				port = input("Sélectionnez le port: ") 
				
				print("\n") 
				
				os.system(f"curl -X GET http://127.0.0.1:{port}/mien") 
				

			case "2": # faire une nouvelle transaction

				port = input("Sélectionnez le port: ")
				cle_privee = input("Entrez la clé privée: ")
				expediteur = input("Entrer l'expediteur: ")
				destinataire = input("Entrer le destinataire: ")
				montant = input("Entrer le montant: ")
				
				print("\n")
				
				os.system(f'curl -i -X POST -H "Content-Type: application/json" -d "{{{backslash}"cle_privee{backslash}":{backslash}"{cle_privee}{backslash}",{backslash}"expediteur{backslash}":{backslash}"{expediteur}{backslash}",{backslash}"destinataire{backslash}":{backslash}"{destinataire}{backslash}",{backslash}"montant{backslash}":{montant}}}" http://127.0.0.1:{port}/transactions/nouveau')

			
			case "3": # afficher la blockchain complète
		
				port = input("Sélectionnez le port: ")
				
				print("\n") 
				
				os.system(f"curl -X GET http://127.0.0.1:{port}/chaine") 
				
		
			case "4": # vérifier si la blockchain est valide
		
				port = input("Sélectionnez le port: ") 
				
				print("\n") 
				
				os.system(f"curl -X GET http://127.0.0.1:{port}/est_valide")
	

			case "5": # ajouter un nouveau noeud à la liste des noeuds
		
				port = input("Sélectionnez le port: ")
				noeud = input("Entrez l'adresse du noeud: ")
				
				print("\n") 

				os.system(f'curl -i -X POST -H "Content-Type: application/json" -d "{{{backslash}"noeuds{backslash}":[{backslash}"{noeud}{backslash}"]}}" http://127.0.0.1:{port}/noeuds/enregistrer')
				
		
			case "6": # résout les conflits
		
				port = input("Sélectionnez le port: ")
				
				print("\n")
				
				os.system(f"curl -X GET http://127.0.0.1:{port}/noeuds/resoudre")


			case "7": # vérifier des pièces de coins d'utilisateur
	
				port = input("Sélectionnez le port: ")
				id = input("Entrez la cle publique: ")
				
				print("\n") 

				os.system(f'curl -i -X POST -H "Content-Type: application/json" -d "{{{backslash}"id{backslash}":{backslash}"{id}{backslash}"}}" http://127.0.0.1:{port}/pieces_de_coins')
				

			case "8": # terminer le programme
			
				# un message d'adieu 
				print("Merci d'utiliser ce programme!")
				print("\nÀ la prochaine fois! ")
				
				input("\n\nAppuyez sur Entrée pour continuer...") # continuation  de cette opération
				
				break # sortie de l'application 
			

			case _: # gérer le cas où l'utilisateur a saisi une valeur d'opération invalide 
				print("Vous avez entré la mauvaise valeur") 


		input("\n\nAppuyez sur Entrée pour continuer...") # sortir d'opération actuel