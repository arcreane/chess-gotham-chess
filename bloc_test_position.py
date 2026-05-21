#Bloc test
if __name__ == "__main__":
    print("--- Début des tests pour la classe Position ---")
    
    # Test 1 : Création et affichage
    pos1 = Position("e", 4)
    print(f"Test 1 (Affichage attendu 'e4') : {pos1}")
    
    # Test 2 : Récupération de l'index chiffré
    print(f"Test 2 (Index de 'e' attendu 4) : {pos1.get_column_idx()}")
    
    # Test 3 : Comparaison de deux positions identiques
    pos2 = Position("e", 4)
    print(f"Test 3 (Comparaison '==' attendu True) : {pos1 == pos2}")
    
    # Test 4 : Vérification de la sécurité contre les mauvaises cases
    try:
        pos_erreur = Position("z", 9)
        print("Erreur : Le code a accepté une case hors du plateau !")
    except ValueError as e:
        print(f"Test 4 (Sécurité attendue réussie) : Capturé l'erreur -> {e}")