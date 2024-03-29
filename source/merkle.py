import hashlib
import codecs


def merkle_root(lst: list):
    '''
    Creation d'une racine Merkle (c'est le hachage de tous les hachages de toutes les transactions qui font partie d'un bloc dans un réseau blockchain.)
    '''

    # blockchain utilise deux passes SHA-256 et une réorganisation des octets pour coller les hachages ensemble 
    sha256d = lambda x: hashlib.sha256(hashlib.sha256(x).digest()).digest()
    hash_pair = lambda x, y: sha256d(x[::-1] + y[::-1])[::-1]

    if len(lst) == 1: return lst[0] # renvoie le premier élément de la liste si la longueur de la liste est 1

    """ les éléments en double dans l'arborescence entraînent une vulnérabilité intéressante 
     - il s'avère que différentes listes de transactions peuvent avoir le même hachage. """

    # si le nombre d'éléments de la liste est impair, ajouter la dernière valeur à la fin de la liste
    if len(lst) % 2 == 1:
        lst.append(lst[-1])

    # appeler récursivement une fonction pour traiter la liste mise à jour
    return merkle_root([hash_pair(x, y)
                        for x, y in zip(*[iter(lst)] * 2)])


def merkle_encode(text: list):
    '''
    Encoder du texte pour une utilisation ultérieure dans une fonction merkle_root
    '''

    txt_merkle = []

    for h in range(len(text)):
        txt_merkle.append(codecs.decode(text[h], 'hex'))

    return codecs.encode(merkle_root(txt_merkle), 'hex').decode('ascii')

