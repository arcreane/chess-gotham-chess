class Player:
  """Classe qui represente un jour d'echecs"""
  def __init__(self, name, color):
    """Initialise un joueur
    name: nom du joueur
    color: 0 pour blanc, 1 pour noir"""
    self.name = name
    self.color = color
    #玩家的名字和颜色
  def askMove(self):
    """Demande au joueur de saisir son prochain mouvement
    Exemple de format attendu:
    Ra1 a4"""
    move = input("Entrez votre mouvement: ")
    return move
    #让玩家用input输入移动
def chooseColor():
  """Demande au joueur de choisir la couleur"""
  color = input("Choisissez votre couleur(blanc/noir) : ")
  color = color.lower().strip()
  #flexible，大小写都可以识别
  while color != "blanc" and color != "noir":
    print("Couleur invalide")
    color = input("Choisissez votre couleur (blanc/noir) : ")
    color = color.lower().strip()
  if color == "blanc":
    return 0
  else:
    return 1
    #让玩家选择颜色
