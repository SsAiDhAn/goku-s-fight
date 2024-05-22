import pyxel, random

pyxel.init(128, 128, title="goku's fight")
goku_x = 60
goku_y = 60
vies = 4
tirs_liste = []
ennemis_liste = []
pyxel.load("res.pyxres")

def reset_game():
    global goku_x, goku_y, vies, tirs_liste, ennemis_liste
    goku_x = 60
    goku_y = 60
    vies = 4
    tirs_liste = []
    ennemis_liste = []

def goku_deplacement(x, y):
    """prend en paramètres les valeurs des variables x et y 
    et renvoie les valeurs des variables x et y modifiées 
    suivant certaines touches du clavier."""
    if pyxel.btn(pyxel.KEY_RIGHT):
        if x < 120 :
            x = x + 1 
    if pyxel.btn(pyxel.KEY_LEFT):
        if x > 0:
            x = x - 1 
    if pyxel.btn(pyxel.KEY_DOWN):
        if y < 120 :
            y = y + 1 
    if pyxel.btn(pyxel.KEY_UP):
        if y > 0 :
            y = y - 1 
    return x, y

def tirs_creation(x, y, tirs_liste):
    """création d'un tir avec la barre d'espace"""
    if pyxel.btnr(pyxel.KEY_SPACE):
        tirs_liste.append([x, y - 4])
    return tirs_liste

def tirs_deplacement(tirs_liste):
    """déplacement des tirs vers le haut et suppression s'ils sortent du cadre"""
    for tir in tirs_liste:
        tir[1] -= 1
        if tir[1] < -8:
            tirs_liste.remove(tir)
    return tirs_liste

def ennemis_creation(ennemis_liste):
    """création aléatoire des ennemis"""
    if pyxel.frame_count % 30 == 0:
        ennemis_liste.append([random.randint(0, 120), 0])
    return ennemis_liste

def ennemis_deplacement(ennemis_liste):
    """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""
    for ennemi in ennemis_liste:
        ennemi[1] += 1
        if ennemi[1] > 128:
            ennemis_liste.remove(ennemi)
    return ennemis_liste

def goku_suppression(vies):
    """disparition du vaisseau et d'un ennemi si contact"""
    for ennemi in ennemis_liste:
        if ennemi[0] <= goku_x + 8 and ennemi[1] <= goku_y + 8 and ennemi[0] + 8 >= goku_x \
                and ennemi[1] + 8 >= goku_y:
            ennemis_liste.remove(ennemi)
            vies -= 1
    return vies

def ennemis_suppression():
    """disparition d'un ennemi et d'un tir si contact"""
    for ennemi in ennemis_liste:
        for tir in tirs_liste:
            if ennemi[0] <= tir[0] + 1 and ennemi[0] + 8 >= tir[0] and ennemi[1] + 8 >= tir[1]:
                ennemis_liste.remove(ennemi)
                tirs_liste.remove(tir)

def update():
    """mise à jour des variables (30 fois par seconde)"""
    global goku_x, goku_y, tirs_liste, ennemis_liste, vies
    if pyxel.play_pos(0) is None:
        pyxel.playm(0, loop=True)
    if pyxel.btnp(pyxel.KEY_R) and vies == 0:
        reset_game()
        pyxel.playm(0, loop=True)
    goku_x, goku_y = goku_deplacement(goku_x, goku_y)
    tirs_liste = tirs_creation(goku_x, goku_y, tirs_liste)
    tirs_liste = tirs_deplacement(tirs_liste)
    ennemis_liste = ennemis_creation(ennemis_liste)
    ennemis_liste = ennemis_deplacement(ennemis_liste)
    ennemis_suppression()
    vies = goku_suppression(vies)
    if vies == 0:
        pyxel.stop() 

def draw():
    """création des objets (30 fois par seconde)"""
    pyxel.cls(0)
    pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
    if vies > 0:
        pyxel.text(5, 5, 'Senzus:' + str(vies), 9)
        pyxel.blt(goku_x, goku_y, 0, 16, 32, 32, 45)
        for tir in tirs_liste:
            pyxel.blt(tir[0], tir[1], 2, 0, 0, 7, 10)
        for ennemi in ennemis_liste:
            pyxel.blt(ennemi[0], ennemi[1], 0, 0, 0, 15, 15)
    else:
        pyxel.text(40, 64, 'GOKU LOOSE...', 7)
        pyxel.text(2, 40, 'Appuie sur "R" pour recommencer le combat', 7)

pyxel.run(update, draw)
