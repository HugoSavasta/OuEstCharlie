import time
from tkinter import * 
from timeit import default_timer


### Jeu Où est Chalie ?
### 5 niveaux
### avec 5 chances pour le trouver ou 30 secondes
### Bonnne chance !

# on créer la fenêtre 
root = Tk()
root.title("OU est Charlie ?")

Hauteur=750
Largeur=750

# ici on mets les différentes images dans une liste
# elles vont constituer les différents niveaux
levels = [["image/ouestcharlie.gif", 510, 440], ["image/charlie_niv2.gif", 515, 430], ["image/charlie_niv3.gif", 730, 250], ["image/charlie_niv4.gif", 55, 350]]


marge_error = 20
maxClick = 5
gameOver = False
curentLevel = 0

Dessin=Canvas(root,height=Hauteur,width=Largeur,bg="black")
Dessin.pack()

img = Dessin.create_image((0,100), anchor="nw")

objectCanvas = []
tx = Dessin.create_text(Largeur/2, Hauteur-25)

start = default_timer()
text_clock = Dessin.create_text(Largeur/Largeur+70, 20)

error_count = 0
gagne=0


# en appelant les différentes fonctions qui suivent
# cette fonction nous permet de réinitialiser
# le chronomètre, le nombre d'erreurs,
# ainsi que tout ce qui ce trouve dans le Canvas,
# comme les croix et les ronds 
def restartLevel():
    global error_count, gameOver
    
    if curentLevel != 4:
        error_count = 0
        gameOver = False
        restartTimer()
        changeLevel()
        deleteAllObjects()
        Dessin.itemconfig(error_clic, text="Erreurs: " + str(error_count))
        Dessin.itemconfig(tx, text="")
    else:
        gameOver = True

# ici on supprime les éléments contenus dans
# le Canvas grâce à la variable objectCanvas
def deleteAllObjects():
    global objectCanvas
    for e in objectCanvas:
        Dessin.delete(e)


# ici on change de niveau
# on va changer l'image constituant un nouveau niveau 
def changeLevel():
    global levels, curentLevel, charlie_posx, charlie_posy,photo,gameOver
    
    if curentLevel != 4:
        photo = PhotoImage(file=levels[curentLevel][0])
        photo.zoom(10)
        Dessin.itemconfigure(img, image=photo)
        charlie_posx = levels[curentLevel][1]
        charlie_posy = levels[curentLevel][2]
    

# ici on recommence le chronomètre
def restartTimer():
    global start
    start = default_timer()


# ici on gère le chronomètre
# en fonction de si les 5 essais ont été exécutés
# ou si les 30 secondes ont été écoulées
# ou encore si l'on a trouvé charlie,
# et que le niveau change
def updateTime():
    global gameOver, error_count, maxClick,gagne
    
    print(gagne)
    if gagne==0:
        now = default_timer() - start
        minutes, seconds = divmod(now, 60)
        hours, minutes = divmod(minutes, 60)

        if (error_count == maxClick):
            Dessin.itemconfig(tx, text="GAME OVER", font="LatinModernMono 20", fill="cyan")
            gameOver = True

        if (seconds <= 31 and gameOver == False):
            str_time = "%d:%02d:%02d" % (hours, minutes, seconds)
            Dessin.itemconfigure(text_clock, text=str_time,fill = "white",font="Arial 20 bold")
            root.after(1000, updateTime)
        else:
            gameOver = True
            Dessin.itemconfig(tx, text="GAVE OVER", font="LatinModernMono 20", fill="cyan")
    
changeLevel()


# ici on regarde si les coordonées du clic
# correspondent ou non avec celles de Charlie
# selon si c'est les mêmes on :
# dessine une croix rouge si ce ne sont pas les mêmes
# si oui on :
# dessine un rond violet autour de charlie
def mouse_xy(event):
    global charlie_posx, charlie_posy,error_count,gagne, curentLevel, objectCanvas
    
    if gagne==0:
        clic = event.x, event.y
        print(clic)
        if ((clic[0] <= (charlie_posx + marge_error))
            and (clic[0] >= (charlie_posx - marge_error))
            and (clic[1] <= (charlie_posy + marge_error))
            and (clic[1] >= (charlie_posy - marge_error))) and error_count < maxClick and gameOver == False:
            objectCanvas.append(Dessin.create_oval(clic[0]-25,clic[1]-25,clic[0]+25,clic[1]+25,width=7,outline='purple'))
            Dessin.itemconfig(tx, text="Bravo tu as trouvé Charlie en " + str(error_count + 1) + " essai(s) !", font="LatinModernMono 20", fill="cyan")
            curentLevel += 1
            Dessin.after(1000, restartLevel)
        elif error_count < maxClick and gameOver == False:
            error_count += 1
            Dessin.itemconfig(error_clic, text="Erreurs: " + str(error_count), fill="black")
            objectCanvas.append(Dessin.create_line(clic[0]-10, clic[1]-10, clic[0]+10, clic[1]+10,width=7,fill='red'))
            objectCanvas.append(Dessin.create_line(clic[0]+10, clic[1]-10, clic[0]-10, clic[1]+10,width=7,fill='red'))
        else:
            gagne = 1
            Dessin.itemconfig(tx, text="GAVE OVER", font="LatinModernMono 20", fill="cyan")
   
        

Dessin.bind("<Button-1>",mouse_xy)

# ici cette fonction va nous permettre d'écrire du texte
def texte(x,y,text,c):
    f ="LatinModernMono 20"; p=(x,y); rayon=2
    return Dessin.create_text(p,text=text,anchor="center",font=f,fill=c)


texte(Largeur/2,50,"Mais ou est Charlie ? Clic sur Charlie","cyan")
error_clic = texte(Largeur/Largeur+70,Hauteur-60,"Erreurs: 0","white")

updateTime()
root.mainloop()