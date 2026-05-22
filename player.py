class Player:
  """Initialise un joueur
  name: nom du joueur
  color: 0 pour blanc, 1 pour noir"""
  self.name = name
  self.color = color
def askMove(self):
  """Demande au joueur de saisir son prochain mouvement
  Exemple de format attendu:
  Ra1 a4"""
  move = input("Entrez votre mouvement: ")
  return move
def chooseColor():
  """Demande au joueur de choisir la couleur"""
  color = input("Choisissez votre couleur(blanc/noir) : ")
  while color != "blanc" and color != "noir":
    print("Couleur invalide")
    color = input("Choisissez votre couleur (blanc/noir) : ")
  if color == "blanc":
    return 0
  else:
    return 1
