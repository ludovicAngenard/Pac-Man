from tkinter import *
from tkinter import messagebox
from random import *
import pickle
import time
import pygame
#Créer une fenêtre, lui met un titre et une toile a l'intérieur (le canvas)
fenetre=Tk()
fenetre.title("RUN FOR YOUR LIFE !")
canvas5 = Canvas(fenetre,width=840, height=700)
#font pour les règles du jeux
fontregle="-family System -size 16 -weight bold -underline 1 -overstrike 0"

with open('donnees', 'rb') as fichier:           #Cela va lire le fichier "donnees" qui contient les valeurs des variables level, bonus, argent et point!
    mon_depickler = pickle.Unpickler(fichier)
    score_recupere = mon_depickler.load()

level=score_recupere['level']                    #Cette variable sert a indiquer le niveau du joueur, le niveau augmente a chaque fois qu'il mange 777 billes jaunes.
bonus=score_recupere['bonus']                    #Cette variable sert à savoir quel bonus le joeur peut acheter.
argent=score_recupere['argent']
point=score_recupere['point']

with open('récompenses', 'rb') as fichier2:     #Cela va lire le fichier  "récompenses" qui contient les valeurs des variables debloque1 à debloque8 et actif
    mon_depickler_recompenses = pickle.Unpickler(fichier2)
    debloque_recompense = mon_depickler_recompenses.load()

debloque1=debloque_recompense['debloque1']      #le premier bonus est acheté
debloque2=debloque_recompense['debloque2']      #Le deuxième bonus est acheté
debloque3=debloque_recompense['debloque3']      #le troisième bonus est acheté
debloque4=debloque_recompense['debloque4']      #Le quatrième bonus est acheté
debloque5=debloque_recompense['debloque5']      #Le cinquième bonus est acheté
debloque6=debloque_recompense['debloque6']      #Le sixième bonus est acheté
debloque7=debloque_recompense['debloque7']      #Le septième bonus est acheté
debloque8=debloque_recompense['debloque8']      #le huitième bonus est acheté
actif=debloque_recompense['actif']              # La variable sert à savoir quel bonus le joueur a choisit d'équiper
#son
pygame.init()
sons_blop=pygame.mixer.Sound("sons/bubul.wav")
sons_point=pygame.mixer.Sound("sons/bruitperdu.wav")
sons_clap=pygame.mixer.Sound("sons/clap.wav")
sons_argent=pygame.mixer.Sound("sons/bipargent.wav")
sons_musiquerun=pygame.mixer.Sound("sons/Kubbi-Ember-04Cascade.wav")
sons_apparition=pygame.mixer.Sound("sons/apparition.wav")
#volume des sons
sons_blop.set_volume(0.2)
sons_point.set_volume(0.3)
sons_clap.set_volume(0.5)
sons_argent.set_volume(0.5)
sons_musiquerun.set_volume(0.2)
sons_apparition.set_volume(0.7)

def piece():                            #Cette fonction sert a savoir quand faire arriver la pièce dans la partie
    global point,LC
    if point%200==0:                    #la pièce arrive a chaque fois que le joueur récupère 200 billes jaunes
        if point !=0:                   #Cette condition évite qu'une pièce arrive dès le début de la partie
            if LC[17][20]!=4:           # 4 étant la pièce, il ne peut pas avoir une pièce sur une pièce
                sons_apparition.play()  #ce son intervient pour marquer l'arrivée de la pièce
                canvas5.create_oval((20*20),(17*20),(20 *20+20),(17*20+20),fill="orange", outline="orange",tag= "piece")            #création graphique de la pièce
                canvas5.create_oval((20*20+5),(17*20+5),(20*20+15),(17*20+15),fill="white", outline="orange",tag= "piece")
                LC[17][20]=4            #si il n'y'a pas de pièce, que le joueur a récupéré 200 billes jaunes et qu'il n'est pas a 0 points alors on met 4 a la case [17][20] ce qui représente une pièce


def lois(): #cette fonction sert à remettre les pions à leur état initial et à empecher le joueur de déplacer le pac man a l'aide des flèches directionnelles
    #toutes les variables dont j'ai besoin pour cette fonction sont en global
    global point,argent,bonus,level,mort,positionb,position,positionr,positionv,positionj,fin, futurjx, futurjy,futurby,futurbx,futurrx,futurry,futurvy,futurvx, LC,a,positionp , futurpx,futurpy,futurnx,futurny,positionn,positionn2,futurn2x,futurn2y,positionn3,futurn3x,futurn3y,futurn4y,futurn4x,positionn4
    mort=1 # quand mort prend la valeur 1 cela veut dire que le joueur est mort sinon il est à 0
    niveaux={
          "level":    level,                      #[
          "bonus":   bonus,
          "argent":   argent,
          "point":  point,                              # tout cela sert a enregistrer la progression du joueur après sa mort dans un fichier
        }
    with open('donnees', 'wb') as fichier:
        mon_pickler = pickle.Pickler(fichier)
        mon_pickler.dump(niveaux)                 #]

    sons_point.play()

    for i in range(a):                          # a est la variable qui indique le nombre total de case.
        canvas5.delete("bubul"+str(i))          #cela supprime toutes les billes du canvas
        canvas5.delete("block"+str(i))          #Cela suprimme tous les bloques du canvas

    canvas5.unbind("<KeyRelease>")              #empêche le joueur d'utiliser les flèches directionnelles
    canvas5.delete("fantomej")                  #[
    canvas5.delete("fantomer")
    canvas5.delete("fantomev")
    canvas5.delete("fantomeb")
    canvas5.delete("fantomep")                      #supprime les fantômes et le pac man
    canvas5.delete("fantomen")
    canvas5.delete("fantomen2")
    canvas5.delete("fantomen3")
    canvas5.delete("fantomen4")
    canvas5.delete("pacman")                    #]
    futurjx = 0                                 #[
    futurjy = 0
    futurbx=0
    futurby=0
    futurrx=0
    futurry=0                                          # remet les valeurs à 0
    futurvx=0
    futurvy=0
    futurpx=0
    futurpy=0                                   #]



def arbitre():
    global positionb,position,positionr,positionv,positionj,fin,positionp ,futurnx,futurny,positionn,positionn2,futurn2x,futurn2y,positionn3,futurn3x,futurn3y,futurn4y,futurn4x,positionn4,level
    if fin==0:
        if level<8:
            if positionb==position or positionr==position or positionv==position or positionj==position or positionp==position:
                lois()
                commencer()
            else:
                fenetre.after(10,arbitre)

        if level>=8:
            if positionb==position or positionr==position or positionv==position or positionj==position or positionp==position or positionn==position or positionn2==position or positionn3==position or positionn4==position:
                lois()
                futurnx=0
                futurny=0
                futurn2x=0
                futurn2y=0
                futurn3x=0
                futurn3y=0
                futurn4x=0
                futurn4y=0
                commencer()

            else:
                fenetre.after(10,arbitre)


def bouchefermée():
    global bouche,sens,x,y,mort,fin
    if mort==0 and fin ==0:
        canvas5.delete("pacman")
        propalskinBF()
        bouche=0
        fenetre.after(250, boucheouverte)

def boucheouverte():
    global bouche,sens,x,y,mort,fin
    if mort==0 and fin==0:
        canvas5.delete("pacman")
        propalskinBO()
        bouche=1
        fenetre.after(250, bouchefermée)


#définition qui prend une direction aléatoire au fantôme et qui redirige dans la définition verificationbleu
def mouvementbleu():
    global bx,by,futurbx,futurby,mouvementb,fin,mort
    if fin ==0 and mort==0:
        listemouv=[1,2,3,4]
        mouvementb=choice(listemouv)
        if mouvementb==1:
            futurby=by-1
            futurbx=bx
        if mouvementb==2:
            futurby=by+1
            futurbx=bx
        if mouvementb==3:
            futurby=by
            futurbx=bx-1
        if mouvementb==4:
            futurby=by
            futurbx=bx+1
        fenetre.after(200,vérificationbleu)

def vérificationbleu():
    global bx,by, futurbx,futurby,LC,positionb,mouvementb

    if LC[futurby][futurbx]==0 or LC[futurby][futurbx]==3:
        canvas5.delete("fantomeb")

        bx=futurbx
        by=futurby
        canvas5.create_polygon((bx*20+5,by*20+14),(bx*20,by*20+18),(bx*20,by*20+5),(bx*20+5,by*20),(bx*20+14,by*20),(bx*20+19,by*20+5),(bx*20+19,by*20+18),(bx*20+14,by*20+14),(bx*20+9,by*20+18), fill="#57aeff", outline="#57aeff", width=3, tag="fantomeb")
        canvas5.create_oval((bx*20+1),(by*20+2.5),(bx*20+8.5),(by*20+12),fill="white", outline="#57aeff",tag= "fantomeb")
        canvas5.create_oval((bx*20+9.5),(by*20+2.5),(bx*20+17),(by*20+12),fill="white", outline="#57aeff",tag= "fantomeb")
        canvas5.create_oval((bx*20+4.5),(by*20+7),(bx*20+8.5),(by*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomeb")
        canvas5.create_oval((bx*20+13),(by*20+7),(bx*20+17),(by*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomeb")
        if mouvementb==1:
            positionb=positionb-42
        if mouvementb==2:
            positionb=positionb+42
        if mouvementb==3:
            positionb=positionb-1
        if mouvementb==4:
            positionb=positionb+1

        mouvementbleu()

    else:
        mouvementbleu()

#mouvement pour le fantome rouge
def mouvementrouge():
    global rx,ry,futurrx,futurry,mouvementr,fin,mort
    if fin==0 and  mort==0:
        listemouv=[1,2,3,4]
        mouvementr=choice(listemouv)
        if mouvementr==1:
            futurry=ry-1
            futurrx=rx
        if mouvementr==2:
            futurry=ry+1
            futurrx=rx
        if mouvementr==3:
            futurry=ry
            futurrx=rx-1
        if mouvementr==4:
            futurry=ry
            futurrx=rx+1
        fenetre.after(200,vérificationrouge)


def vérificationrouge():
    global rx,ry, futurrx,futurry,LC,positionr,mouvementr

    if LC[futurry][futurrx]==0 or LC[futurry][futurrx]==3:
        canvas5.delete("fantomer")
        rx=futurrx
        ry=futurry
        canvas5.create_polygon((rx*20+5,ry*20+14),(rx*20,ry*20+18),(rx*20,ry*20+5),(rx*20+5,ry*20),(rx*20+14,ry*20),(rx*20+19,ry*20+5),(rx*20+19,ry*20+18),(rx*20+14,ry*20+14),(rx*20+9,ry*20+18), fill="#ff5805", outline="#ff5805", width=3, tag="fantomer")
        canvas5.create_oval((rx*20+1),(ry*20+2.5),(rx*20+8.5),(ry*20+12),fill="white", outline="#ff5805",tag= "fantomer")
        canvas5.create_oval((rx*20+9.5),(ry*20+2.5),(rx*20+17),(ry*20+12),fill="white", outline="#ff5805",tag= "fantomer")
        canvas5.create_oval((rx*20+4.5),(ry*20+7),(rx*20+8.5),(ry*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomer")
        canvas5.create_oval((rx*20+13),(ry*20+7),(rx*20+17),(ry*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomer")
        if mouvementr==1:
            positionr=positionr-42
        if mouvementr==2:
            positionr=positionr+42
        if mouvementr==3:
            positionr=positionr-1
        if mouvementr==4:
            positionr=positionr+1

        mouvementrouge()

    else:
        mouvementrouge()


#mouvement pour le fantome vert
def mouvementvert():
    global vx,vy,futurvx,futurvy,mouvementv,fin,mort
    if fin==0 and mort==0:
        listemouv=[1,2,3,4]
        mouvementv=choice(listemouv)
        if mouvementv==1:
            futurvy=vy-1
            futurvx=vx
        if mouvementv==2:
            futurvy=vy+1
            futurvx=vx
        if mouvementv==3:
            futurvy=vy
            futurvx=vx-1
        if mouvementv==4:
            futurvy=vy
            futurvx=vx+1

        fenetre.after(200,vérificationvert)

def vérificationvert():
    global vx,vy, futurvx,futurvy,LC,positionv,mouvementv

    if LC[futurvy][futurvx]==0 or LC[futurvy][futurvx]==3:
        canvas5.delete("fantomev")
        vx=futurvx
        vy=futurvy
        canvas5.create_polygon((vx*20+5,vy*20+14),(vx*20,vy*20+18),(vx*20,vy*20+5),(vx*20+5,vy*20),(vx*20+14,vy*20),(vx*20+19,vy*20+5),(vx*20+19,vy*20+18),(vx*20+14,vy*20+14),(vx*20+9,vy*20+18), fill="#27b827", outline="#27b827", width=3, tag="fantomev")
        canvas5.create_oval((vx*20+1),(vy*20+2.5),(vx*20+8.5),(vy*20+12),fill="white", outline="#27b827",tag= "fantomev")
        canvas5.create_oval((vx*20+9.5),(vy*20+2.5),(vx*20+17),(vy*20+12),fill="white", outline="#27b827",tag= "fantomev")
        canvas5.create_oval((vx*20+4.5),(vy*20+7),(vx*20+8.5),(vy*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomev")
        canvas5.create_oval((vx*20+13),(vy*20+7),(vx*20+17),(vy*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomev")
        if mouvementv==1:
            positionv=positionv-42
        if mouvementv==2:
            positionv=positionv+42
        if mouvementv==3:
            positionv=positionv-1
        if mouvementv==4:
            positionv=positionv+1

        mouvementvert()

    else:
        mouvementvert()

#mouvement pour le fantome jaune
def mouvementjaune():
    global jx,jy,futurjx,futurjy,mouvementj,fin,mort
    if fin==0 and mort==0:
        listemouv=[1,2,3,4]
        mouvementj=choice(listemouv)
        if mouvementj==1:
            futurjy=jy-1
            futurjx=jx
        if mouvementj==2:
            futurjy=jy+1
            futurjx=jx
        if mouvementj==3:
            futurjy=jy
            futurjx=jx-1
        if mouvementj==4:
            futurjy=jy
            futurjx=jx+1
        fenetre.after(200,vérificationjaune)


def vérificationjaune():
    global jx,jy, futurjx,futurjy,LC,positionj,mouvementj

    if LC[futurjy][futurjx]==0 or LC[futurjy][futurjx]==3:
        canvas5.delete("fantomej")
        jx=futurjx
        jy=futurjy
        canvas5.create_polygon((jx*20+5,jy*20+14),(jx*20,jy*20+18),(jx*20,jy*20+5),(jx*20+5,jy*20),(jx*20+14,jy*20),(jx*20+19,jy*20+5),(jx*20+19,jy*20+18),(jx*20+14,jy*20+14),(jx*20+9,jy*20+18), fill="#c9a71e", outline="#c9a71e", width=3, tag="fantomej")
        canvas5.create_oval((jx*20+1),(jy*20+2.5),(jx*20+8.5),(jy*20+12),fill="white", outline="#c9a71e",tag= "fantomej")
        canvas5.create_oval((jx*20+9.5),(jy*20+2.5),(jx*20+17),(jy*20+12),fill="white", outline="#c9a71e",tag= "fantomej")
        canvas5.create_oval((jx*20+4.5),(jy*20+7),(jx*20+8.5),(jy*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomej")
        canvas5.create_oval((jx*20+13),(jy*20+7),(jx*20+17),(jy*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomej")
        if mouvementj==1:
            positionj=positionj-42
        if mouvementj==2:
            positionj=positionj+42
        if mouvementj==3:
            positionj=positionj-1
        if mouvementj==4:
            positionj=positionj+1

        mouvementjaune()

    else:
        mouvementjaune()

def mouvementpink():
    global px,py,futurpx,futurpy,mouvementp,fin,mort
    if fin==0 and mort==0:
        listemouv=[1,2,3,4]
        mouvementp=choice(listemouv)
        if mouvementp==1:
            futurpy=py-1
            futurpx=px
        if mouvementp==2:
            futurpy=py+1
            futurpx=px
        if mouvementp==3:
            futurpy=py
            futurpx=px-1
        if mouvementp==4:
            futurpy=py
            futurpx=px+1
        fenetre.after(200,vérificationpink)

def vérificationpink():
    global px,py, futurpx,futurpy,LC,positionp,mouvementp

    if LC[futurpy][futurpx]==0 or LC[futurpy][futurpx]==3:
        canvas5.delete("fantomep")
        px=futurpx
        py=futurpy
        canvas5.create_polygon((px*20+5,py*20+14),(px*20,py*20+18),(px*20,py*20+5),(px*20+5,py*20),(px*20+14,py*20),(px*20+19,py*20+5),(px*20+19,py*20+18),(px*20+14,py*20+14),(px*20+9,py*20+18), fill="pink", outline="pink", width=3, tag="fantomep")
        canvas5.create_oval((px*20+1),(py*20+2.5),(px*20+8.5),(py*20+12),fill="white", outline="pink",tag= "fantomep")
        canvas5.create_oval((px*20+9.5),(py*20+2.5),(px*20+17),(py*20+12),fill="white", outline="pink",tag= "fantomep")
        canvas5.create_oval((px*20+4.5),(py*20+7),(px*20+8.5),(py*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomep")
        canvas5.create_oval((px*20+13),(py*20+7),(px*20+17),(py*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomep")
        if mouvementp==1:
            positionp=positionp-42
        if mouvementp==2:
            positionp=positionp+42
        if mouvementp==3:
            positionp=positionp-1
        if mouvementp==4:
            positionp=positionp+1

        mouvementpink()

    else:
        mouvementpink()

def mouvementnoir():
    global nx,ny,futurnx,futurny,mouvementn,fin,mort
    if fin==0 and mort==0:
        listemouv=[1,2,3,4]
        mouvementn=choice(listemouv)
        if mouvementn==1:
            futurny=ny-1
            futurnx=nx
        if mouvementn==2:
            futurny=ny+1
            futurnx=nx
        if mouvementn==3:
            futurny=ny
            futurnx=nx-1
        if mouvementn==4:
            futurny=ny
            futurnx=nx+1
        fenetre.after(200,vérificationnoir)

def vérificationnoir():
    global nx,ny, futurnx,futurny,LC,positionn,mouvementn

    if LC[futurny][futurnx]==0 or LC[futurny][futurnx]==3:
        canvas5.delete("fantomen")
        nx=futurnx
        ny=futurny
        canvas5.create_polygon((nx*20+5,ny*20+14),(nx*20,ny*20+18),(nx*20,ny*20+5),(nx*20+5,ny*20),(nx*20+14,ny*20),(nx*20+19,ny*20+5),(nx*20+19,ny*20+18),(nx*20+14,ny*20+14),(nx*20+9,ny*20+18), fill="black", outline="black", width=3, tag="fantomen")
        canvas5.create_oval((nx*20+1),(ny*20+2.5),(nx*20+8.5),(ny*20+12),fill="white", outline="black",tag= "fantomen")
        canvas5.create_oval((nx*20+9.5),(ny*20+2.5),(nx*20+17),(ny*20+12),fill="white", outline="black",tag= "fantomen")
        canvas5.create_oval((nx*20+4.5),(ny*20+7),(nx*20+8.5),(ny*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen")
        canvas5.create_oval((nx*20+13),(ny*20+7),(nx*20+17),(ny*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen")
        if mouvementn==1:
            positionn=positionn-42
        if mouvementn==2:
            positionn=positionn+42
        if mouvementn==3:
            positionn=positionn-1
        if mouvementn==4:
            positionn=positionn+1

        mouvementnoir()

    else:
        mouvementnoir()

def mouvementnoir2():
    global n2x,n2y,futurn2x,futurn2y,mouvementn2,fin,mort
    if fin==0 and mort==0:
        listemouv=[1,2,3,4]
        mouvementn2=choice(listemouv)
        if mouvementn2==1:
            futurn2y=n2y-1
            futurn2x=n2x
        if mouvementn2==2:
            futurn2y=n2y+1
            futurn2x=n2x
        if mouvementn2==3:
            futurn2y=n2y
            futurn2x=n2x-1
        if mouvementn2==4:
            futurn2y=n2y
            futurn2x=n2x+1
        fenetre.after(200,vérificationnoir2)

def vérificationnoir2():
    global n2x,n2y, futurn2x,futurn2y,LC,positionn2,mouvementn2

    if LC[futurn2y][futurn2x]==0 or LC[futurn2y][futurn2x]==3:
        canvas5.delete("fantomen2")
        n2x=futurn2x
        n2y=futurn2y
        canvas5.create_polygon((n2x*20+5,n2y*20+14),(n2x*20,n2y*20+18),(n2x*20,n2y*20+5),(n2x*20+5,n2y*20),(n2x*20+14,n2y*20),(n2x*20+19,n2y*20+5),(n2x*20+19,n2y*20+18),(n2x*20+14,n2y*20+14),(n2x*20+9,n2y*20+18), fill="black", outline="black", width=3, tag="fantomen2")
        canvas5.create_oval((n2x*20+1),(n2y*20+2.5),(n2x*20+8.5),(n2y*20+12),fill="white", outline="black",tag= "fantomen2")
        canvas5.create_oval((n2x*20+9.5),(n2y*20+2.5),(n2x*20+17),(n2y*20+12),fill="white", outline="black",tag= "fantomen2")
        canvas5.create_oval((n2x*20+4.5),(n2y*20+7),(n2x*20+8.5),(n2y*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen2")
        canvas5.create_oval((n2x*20+13),(n2y*20+7),(n2x*20+17),(n2y*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen2")
        if mouvementn2==1:
            positionn2=positionn2-42
        if mouvementn2==2:
            positionn2=positionn2+42
        if mouvementn2==3:
            positionn2=positionn2-1
        if mouvementn2==4:
            positionn2=positionn2+1

        mouvementnoir2()

    else:
        mouvementnoir2()

def mouvementnoir3():
    global n3x,n3y,futurn3x,futurn3y,mouvementn3,fin,mort
    if fin==0 and mort==0:
        listemouv=[1,2,3,4]
        mouvementn3=choice(listemouv)
        if mouvementn3==1:
            futurn3y=n3y-1
            futurn3x=n3x
        if mouvementn3==2:
            futurn3y=n3y+1
            futurn3x=n3x
        if mouvementn3==3:
            futurn3y=n3y
            futurn3x=n3x-1
        if mouvementn3==4:
            futurn3y=n3y
            futurn3x=n3x+1
        fenetre.after(200,vérificationnoir3)

def vérificationnoir3():
    global n3x,n3y, futurn3x,futurn3y,LC,positionn3,mouvementn3

    if LC[futurn3y][futurn3x]==0 or LC[futurn3y][futurn3x]==3:
        canvas5.delete("fantomen3")
        n3x=futurn3x
        n3y=futurn3y
        canvas5.create_polygon((n3x*20+5,n3y*20+14),(n3x*20,n3y*20+18),(n3x*20,n3y*20+5),(n3x*20+5,n3y*20),(n3x*20+14,n3y*20),(n3x*20+19,n3y*20+5),(n3x*20+19,n3y*20+18),(n3x*20+14,n3y*20+14),(n3x*20+9,n3y*20+18), fill="black", outline="black", width=3, tag="fantomen3")
        canvas5.create_oval((n3x*20+1),(n3y*20+2.5),(n3x*20+8.5),(n3y*20+12),fill="white", outline="black",tag= "fantomen3")
        canvas5.create_oval((n3x*20+9.5),(n3y*20+2.5),(n3x*20+17),(n3y*20+12),fill="white", outline="black",tag= "fantomen3")
        canvas5.create_oval((n3x*20+4.5),(n3y*20+7),(n3x*20+8.5),(n3y*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen3")
        canvas5.create_oval((n3x*20+13),(n3y*20+7),(n3x*20+17),(n3y*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen3")
        if mouvementn3==1:
            positionn3=positionn3-42
        if mouvementn3==2:
            positionn3=positionn3+42
        if mouvementn3==3:
            positionn3=positionn3-1
        if mouvementn3==4:
            positionn3=positionn3+1

        mouvementnoir3()
    else:
        mouvementnoir3()

def mouvementnoir4():
    global n4x,n4y,futurn4x,futurn4y,mouvementn4,fin,mort
    if fin==0 and mort==0:
        listemouv=[1,2,3,4]
        mouvementn4=choice(listemouv)
        if mouvementn4==1:
            futurn4y=n4y-1
            futurn4x=n4x
        if mouvementn4==2:
            futurn4y=n4y+1
            futurn4x=n4x
        if mouvementn4==3:
            futurn4y=n4y
            futurn4x=n4x-1
        if mouvementn4==4:
            futurn4y=n4y
            futurn4x=n4x+1
        fenetre.after(200,vérificationnoir4)

def vérificationnoir4():
    global n4x,n4y, futurn4x,futurn4y,LC,positionn4,mouvementn4

    if LC[futurn4y][futurn4x]==0 or LC[futurn4y][futurn4x]==3:
        canvas5.delete("fantomen4")
        n4x=futurn4x
        n4y=futurn4y
        canvas5.create_polygon((n4x*20+5,n4y*20+14),(n4x*20,n4y*20+18),(n4x*20,n4y*20+5),(n4x*20+5,n4y*20),(n4x*20+14,n4y*20),(n4x*20+19,n4y*20+5),(n4x*20+19,n4y*20+18),(n4x*20+14,n4y*20+14),(n4x*20+9,n4y*20+18), fill="black", outline="black", width=3, tag="fantomen4")
        canvas5.create_oval((n4x*20+1),(n4y*20+2.5),(n4x*20+8.5),(n4y*20+12),fill="white", outline="black",tag= "fantomen4")
        canvas5.create_oval((n4x*20+9.5),(n4y*20+2.5),(n4x*20+17),(n4y*20+12),fill="white", outline="black",tag= "fantomen4")
        canvas5.create_oval((n4x*20+4.5),(n4y*20+7),(n4x*20+8.5),(n4y*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen4")
        canvas5.create_oval((n4x*20+13),(n4y*20+7),(n4x*20+17),(n4y*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen4")
        if mouvementn4==1:
            positionn4=positionn4-42
        if mouvementn4==2:
            positionn4=positionn4+42
        if mouvementn4==3:
            positionn4=positionn4-1
        if mouvementn4==4:
            positionn4=positionn4+1

        mouvementnoir4()

    else:
        mouvementnoir4()

def fleche(event):
    global x,y,futury,futurx,sens
    touche=event.keysym
    if touche =="Up" or touche=="Down" or touche=="Right" or touche== "Left":
        clavier=1 #la variable clavier est ici pour savoir si seulement les flèches sont tapper et non les autres touches du clavier faisant bugger le code.
    else:
        clavier=0
    while clavier ==1:
        if touche =="Up":
            sens=1
            futury=y-1
            futurx=x

        elif touche =="Down":
            sens=2
            futury=y+1
            futurx=x

        elif touche =="Left":
            sens=3
            futury=y
            futurx=x-1


        elif touche =="Right":
            sens=4
            futury=y
            futurx=x+1
        clavier=0
        vérification()



def vérification():
    global x,y,LC,pacman,futurx,futurbx,futurjx,futurrx,futurpy,futurvx,futurby,futurjy,futurpx,futurry,futurvy,futury,bouche,sens,position,point,level,actif,i,j,fin,argent,bonus,a
    if LC[futury][futurx]==0 or LC[futury][futurx]==3 or LC[futury][futurx]==4 :
        continuer=0
        j=0
        i=0
        LC[y][x]=3
        x=futurx
        y=futury
        canvas5.delete("pacman")
        if bouche==1:
            propalskinBF()
        elif bouche==0:
            propalskinBO()
        else:
            if actif==4:
                canvas5.create_polygon((x*20+5,y*20+14),(x*20,y*20+18),(x*20,y*20+5),(x*20+5,y*20),(x*20+14,y*20),(x*20+19,y*20+5),(x*20+19,y*20+18),(x*20+14,y*20+14),(x*20+9,y*20+18), fill="yellow", outline="yellow", width=3, tag="pacman")
                canvas5.create_oval((x*20+1),(y*20+2.5),(x*20+8.5),(y*20+12),fill="white", outline="yellow",tag= "pacman")
                canvas5.create_oval((x*20+9.5),(y*20+2.50),(x*20+17),(y*20+12),fill="white", outline="yellow",tag= "pacman")
                canvas5.create_oval((x*20+4.5),(y*20+7),(x*20+8.5),(y*20+12),fill="#588ffc", outline="#588ffc",tag= "pacman")
                canvas5.create_oval((x*20+13),(y*20+7),(x*20+17),(y*20+12),fill="#588ffc", outline="#588ffc",tag= "pacman")
            elif actif==5:
                canvas5.create_polygon((x*20+5,y*20+14),(x*20,y*20+18),(x*20,y*20+5),(x*20+5,y*20),(x*20+14,y*20),(x*20+19,y*20+5),(x*20+19,y*20+18),(x*20+14,y*20+14),(x*20+9,y*20+18), fill="white", outline="white", width=3, tag="pacman")
                canvas5.create_oval((x*20+1),(y*20+2.5),(x*20+8.5),(y*20+12),fill="white", outline="white",tag= "pacman")
                canvas5.create_oval((x*20+9.5),(y*20+2.50),(x*20+17),(y*20+12),fill="white", outline="white",tag= "pacman")
                canvas5.create_oval((x*20+4.5),(y*20+7),(x*20+8.5),(y*20+12),fill="#588ffc", outline="#588ffc",tag= "pacman")
                canvas5.create_oval((x*20+13),(y*20+7),(x*20+17),(y*20+12),fill="#588ffc", outline="#588ffc",tag= "pacman")
            elif actif==6:
                canvas5.create_polygon((x*20+5,y*20+14),(x*20,y*20+18),(x*20,y*20+5),(x*20+5,y*20),(x*20+14,y*20),(x*20+19,y*20+5),(x*20+19,y*20+18),(x*20+14,y*20+14),(x*20+9,y*20+18), fill="red", outline="white", width=3, tag="pacman")
                canvas5.create_oval((x*20+1),(y*20+2.5),(x*20+8.5),(y*20+12),fill="white", outline="white",tag= "pacman")
                canvas5.create_oval((x*20+9.5),(y*20+2.50),(x*20+17),(y*20+12),fill="white", outline="white",tag= "pacman")
                canvas5.create_oval((x*20+4.5),(y*20+7),(x*20+8.5),(y*20+12),fill="darkred", outline="darkred",tag= "pacman")
                canvas5.create_oval((x*20+13),(y*20+7),(x*20+17),(y*20+12),fill="darkred", outline="darkred",tag= "pacman")

        if sens==1:
            position=position-42
        elif sens==2:
            position=position+42
        elif sens==3:
            position=position-1
        elif sens==4:
            position=position+1
        piece()
        if LC[futury][futurx]==0:
            sons_blop.play()
            canvas5.delete("bubul"+str(position-1))
            point=point+1
            canvas5.delete("score")
            canvas5.create_text(420,650,text="SCORE:"+''+str(point),fill="#08155c",font=fontregle,tags="score")

            if point%777==0:
                canvas5.delete("level")
                level=level+1
                canvas5.create_text(420,630,text="LEVEL:"+''+str(level),fill="#08155c",font=fontregle,tags="level")
                bonus+=1


        elif  LC[futury][futurx]==4:
                sons_argent.play()
                canvas5.delete("piece")
                argent=argent+1

                canvas5.delete("argent")
                canvas5.create_oval((400),(660),(420),(680),fill="orange", outline="orange",tag= "argent")
                canvas5.create_oval((405),(665),(415),(675),fill="white", outline="orange",tag= "argent")
                canvas5.create_text(430,670,text=":"+''+str(argent),fill="black",font=fontregle,tags="argent")
        while j < 29:
            while i<42:
                if LC[j][i]==0 :
                    continuer=continuer+1
                i=i+1
            i=0
            j=j+1
        if continuer==0:
            sons_clap.play()
            fin=1
            for i in range(a):
                canvas5.delete("bubul"+str(i))
                canvas5.delete("block"+str(i))
            canvas5.unbind("<KeyRelease>")
            canvas5.delete("fantomej")
            canvas5.delete("fantomer")
            canvas5.delete("fantomev")
            canvas5.delete("fantomeb")
            canvas5.delete("fantomep")
            canvas5.delete("fantomen")
            canvas5.delete("fantomen2")
            canvas5.delete("fantomen3")
            canvas5.delete("fantomen4")
            canvas5.delete("pacman")
            futurjx = 0
            futurjy = 0
            futurbx=0
            futurby=0
            futurrx=0
            futurry=0
            futurvx=0
            futurvy=0
            futurpx=0
            futurpy=0
            niveaux={
                  "level":    level,
                  "bonus":   bonus,
                  "argent":   argent,
                  "point":  point,
                }
            with open('donnees', 'wb') as fichier:
                mon_pickler = pickle.Pickler(fichier)
                mon_pickler.dump(niveaux)
            commencer()


def commencer():
    global LC,sens,position,x,y,bx,by,positionb,mort,rx,ry,positionr,vx,vy,positionv,jx,jy,px,py,positionp,a,argent,point,actif,positionj,nx,ny,positionn,level,n2x,n2y,positionn2,n3x,n3y,positionn3,n4x,n4y,positionn4
    sons_musiquerun.stop()
    #reset
    canvas5.delete("bonus")
    canvas5.delete("piece")
    canvas5.delete("regle")
    canvas5.unbind("<Button-1>")
    canvas5.delete("prix1")
    canvas5.delete("prix2")
    canvas5.delete("prix3")
    canvas5.delete("prix4")
    canvas5.delete("prix5")
    canvas5.delete("prix6")
    canvas5.delete("prix7")
    canvas5.delete("prix8")
    x=20
    y=17
    bx=20
    by=14
    rx=1
    ry=1
    vx=40
    vy=27
    jx=1
    jy=27
    px=40
    py=1

    nx=19
    ny=22
    n2x=21
    n2y=22
    n3x=10
    n3y=5
    n4x=31
    n4y=5
    i=0
    j=0
    a=0
    #le sens est la variable définnissant la direction de la bouche du pacman. sens1=bouche en haut sens2=bouche en bas sens 3= bouche a gauche sens4=bouche a droite
    sens=4
    #position du pacman en fonction du nombre de la case
    position=735
    positionb=609
    positionr=44
    positionp=83
    positionv=1175
    positionj=1136
    positionn=944
    positionn2=946
    positionn3=221
    positionn4=242
    #création du fantome bleu
    canvas5.create_polygon((bx*20+5,by*20+14),(bx*20,by*20+18),(bx*20,by*20+5),(bx*20+5,by*20),(bx*20+14,by*20),(bx*20+19,by*20+5),(bx*20+19,by*20+18),(bx*20+14,by*20+14),(bx*20+9,by*20+18), fill="#57aeff", outline="#57aeff", width=3, tag="fantomeb")
    canvas5.create_oval((bx*20+1),(by*20+2.5),(bx*20+8.5),(by*20+12),fill="white", outline="#57aeff",tag= "fantomeb")
    canvas5.create_oval((bx*20+9.5),(by*20+2.5),(bx*20+17),(by*20+12),fill="white", outline="#57aeff",tag= "fantomeb")
    canvas5.create_oval((bx*20+4.5),(by*20+7),(bx*20+8.5),(by*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomeb")
    canvas5.create_oval((bx*20+13),(by*20+7),(bx*20+17),(by*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomeb")
    #création du fantome rouge
    canvas5.create_polygon((rx*20+5,ry*20+14),(rx*20,ry*20+18),(rx*20,ry*20+5),(rx*20+5,ry*20),(rx*20+14,ry*20),(rx*20+19,ry*20+5),(rx*20+19,ry*20+18),(rx*20+14,ry*20+14),(rx*20+9,ry*20+18), fill="#ff5805", outline="#ff5805", width=3, tag="fantomer")
    canvas5.create_oval((rx*20+1),(ry*20+2.5),(rx*20+8.5),(ry*20+12),fill="white", outline="#ff5805",tag= "fantomer")
    canvas5.create_oval((rx*20+9.5),(ry*20+2.5),(rx*20+17),(ry*20+12),fill="white", outline="#ff5805",tag= "fantomer")
    canvas5.create_oval((rx*20+4.5),(ry*20+7),(rx*20+8.5),(ry*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomer")
    canvas5.create_oval((rx*20+13),(ry*20+7),(rx*20+17),(ry*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomer")
    #création du fantome vert
    canvas5.create_polygon((vx*20+5,vy*20+14),(vx*20,vy*20+18),(vx*20,vy*20+5),(vx*20+5,vy*20),(vx*20+14,vy*20),(vx*20+19,vy*20+5),(vx*20+19,vy*20+18),(vx*20+14,vy*20+14),(vx*20+9,vy*20+18), fill="#27b827", outline="#27b827", width=3, tag="fantomev")
    canvas5.create_oval((vx*20+1),(vy*20+2.5),(vx*20+8.5),(vy*20+12),fill="white", outline="#27b827",tag= "fantomev")
    canvas5.create_oval((vx*20+9.5),(vy*20+2.5),(vx*20+17),(vy*20+12),fill="white", outline="#27b827",tag= "fantomev")
    canvas5.create_oval((vx*20+4.5),(vy*20+7),(vx*20+8.5),(vy*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomev")
    canvas5.create_oval((vx*20+13),(vy*20+7),(vx*20+17),(vy*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomev")
    #création du fantome jaune pas beau
    canvas5.create_polygon((jx*20+5,jy*20+14),(jx*20,jy*20+18),(jx*20,jy*20+5),(jx*20+5,jy*20),(jx*20+14,jy*20),(jx*20+19,jy*20+5),(jx*20+19,jy*20+18),(jx*20+14,jy*20+14),(jx*20+9,jy*20+18), fill="#c9a71e", outline="#c9a71e", width=3, tag="fantomej")
    canvas5.create_oval((jx*20+1),(jy*20+2.5),(jx*20+8.5),(jy*20+12),fill="white", outline="#c9a71e",tag= "fantomej")
    canvas5.create_oval((jx*20+9.5),(jy*20+2.5),(jx*20+17),(jy*20+12),fill="white", outline="#c9a71e",tag= "fantomej")
    canvas5.create_oval((jx*20+4.5),(jy*20+7),(jx*20+8.5),(jy*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomej")
    canvas5.create_oval((jx*20+13),(jy*20+7),(jx*20+17),(jy*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomej")
    #création du fantôme rose
    canvas5.create_polygon((px*20+5,py*20+14),(px*20,py*20+18),(px*20,py*20+5),(px*20+5,py*20),(px*20+14,py*20),(px*20+19,py*20+5),(px*20+19,py*20+18),(px*20+14,py*20+14),(px*20+9,py*20+18), fill="pink", outline="pink", width=3, tag="fantomep")
    canvas5.create_oval((px*20+1),(py*20+2.5),(px*20+8.5),(py*20+12),fill="white", outline="pink",tag= "fantomep")
    canvas5.create_oval((px*20+9.5),(py*20+2.5),(px*20+17),(py*20+12),fill="white", outline="pink",tag= "fantomep")
    canvas5.create_oval((px*20+4.5),(py*20+7),(px*20+8.5),(py*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomep")
    canvas5.create_oval((px*20+13),(py*20+7),(px*20+17),(py*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomep")


    #spray des pièces
    canvas5.create_oval((400),(660),(420),(680),fill="orange", outline="orange",tag= "argent")
    canvas5.create_oval((405),(665),(415),(675),fill="white", outline="orange",tag= "argent")
    canvas5.create_text(430,670,text=":"+''+str(argent),fill="black",font=fontregle,tags="argent")
    canvas5.create_text(420,650,text="SCORE:"+''+str(point),fill="#08155c",font=fontregle,tags="score")

    LC=[
    #0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],#0
    [1,3,3,3,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,3,3,3,1],#1
    [1,3,3,3,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,3,3,3,1],#2
    [1,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,1],#3
    [1,0,0,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,0,1],#4
    [1,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,0,1],#5
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],#6
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],#7
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],#8
    [1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],#9
    [1,1,1,1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,1,3,3,3,1,1,1,1,1,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1],#0
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,3,3,3,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],#1
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,3,3,1,3,3,3,1,3,3,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],#2
    [1,0,0,0,0,0,1,0,0,1,0,0,1,0,0,1,3,3,3,3,3,3,3,3,3,1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,1],#3
    [1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,3,3,3,3,3,3,3,3,3,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],#4
    [1,0,0,1,1,1,1,0,0,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,1,1,1,1,0,0,1],#5
    [1,0,0,1,0,0,0,0,0,1,1,1,0,0,1,1,3,3,3,3,3,3,3,3,3,1,1,0,0,1,1,1,0,0,0,0,0,0,1,0,0,1],#6
    [1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],#7
    [1,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1],#8
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],#9
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],#0
    [1,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,1],#1
    [1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1],#2
    [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],#3
    [1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1],#4
    [1,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,1],#5
    [1,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,1],#6
    [1,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,1],#7
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]#8

    #affiche les niveaux
    canvas5.create_text(420,630,text="LEVEL:"+''+str(level),fill="#08155c",font=fontregle,tags="level")
    while j < 29:
        while i<42:

            if LC[j][i]==1 or LC[j][i]==0 or LC[j][i]==3:

                if LC[j][i]==1:
                    canvas5.create_rectangle(i*20,j*20,i*20+20,j*20+20,fill='black',tag="block"+str(a))


                if LC[j][i]==0:
                    canvas5.create_oval(i*20,j*20,i*20+10,j*20+10,fill= "yellow",tag="bubul"+str(a))
                # a est le nombre a laquelle la case est positionné
                a=a+1
            i=i+1
        i=0
        j=j+1
    #affichage des boutons
    canvas5.create_window(95,650, window=btcommencer, tags = "menu")
    canvas5.create_window(750,650, window=btskin, tags = "menu")
    canvas5.create_window(275,650, window=btregle, tags = "menu")
    #ajout de fantome selon le niveau
    if level>=8:
        #création du fantome noir
        canvas5.create_polygon((nx*20+5,ny*20+14),(nx*20,ny*20+18),(nx*20,ny*20+5),(nx*20+5,ny*20),(nx*20+14,ny*20),(nx*20+19,ny*20+5),(nx*20+19,ny*20+18),(nx*20+14,ny*20+14),(nx*20+9,ny*20+18), fill="black", outline="black", width=3, tag="fantomen")
        canvas5.create_oval((nx*20+1),(ny*20+2.5),(nx*20+8.5),(ny*20+12),fill="white", outline="black",tag= "fantomen")
        canvas5.create_oval((nx*20+9.5),(ny*20+2.5),(nx*20+17),(ny*20+12),fill="white", outline="black",tag= "fantomen")
        canvas5.create_oval((nx*20+4.5),(ny*20+7),(nx*20+8.5),(ny*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen")
        canvas5.create_oval((nx*20+13),(ny*20+7),(nx*20+17),(ny*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen")
        #création du fantome noir2
        canvas5.create_polygon((n2x*20+5,n2y*20+14),(n2x*20,n2y*20+18),(n2x*20,n2y*20+5),(n2x*20+5,n2y*20),(n2x*20+14,n2y*20),(n2x*20+19,n2y*20+5),(n2x*20+19,n2y*20+18),(n2x*20+14,n2y*20+14),(n2x*20+9,n2y*20+18), fill="black", outline="black", width=3, tag="fantomen2")
        canvas5.create_oval((n2x*20+1),(n2y*20+2.5),(n2x*20+8.5),(n2y*20+12),fill="white", outline="black",tag= "fantomen2")
        canvas5.create_oval((n2x*20+9.5),(n2y*20+2.5),(n2x*20+17),(n2y*20+12),fill="white", outline="black",tag= "fantomen2")
        canvas5.create_oval((n2x*20+4.5),(n2y*20+7),(n2x*20+8.5),(n2y*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen2")
        canvas5.create_oval((n2x*20+13),(n2y*20+7),(n2x*20+17),(n2y*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen2")
        #création du fantome noir3
        canvas5.create_polygon((n3x*20+5,n3y*20+14),(n3x*20,n3y*20+18),(n3x*20,n3y*20+5),(n3x*20+5,n3y*20),(n3x*20+14,n3y*20),(n3x*20+19,n3y*20+5),(n3x*20+19,n3y*20+18),(n3x*20+14,n3y*20+14),(n3x*20+9,n3y*20+18), fill="black", outline="black", width=3, tag="fantomen3")
        canvas5.create_oval((n3x*20+1),(n3y*20+2.5),(n3x*20+8.5),(n3y*20+12),fill="white", outline="black",tag= "fantomen3")
        canvas5.create_oval((n3x*20+9.5),(n3y*20+2.5),(n3x*20+17),(n3y*20+12),fill="white", outline="black",tag= "fantomen3")
        canvas5.create_oval((n3x*20+4.5),(n3y*20+7),(n3x*20+8.5),(n3y*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen3")
        canvas5.create_oval((n3x*20+13),(n3y*20+7),(n3x*20+17),(n3y*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen3")
        #création du fantome noir4
        canvas5.create_polygon((n4x*20+5,n4y*20+14),(n4x*20,n4y*20+18),(n4x*20,n4y*20+5),(n4x*20+5,n4y*20),(n4x*20+14,n4y*20),(n4x*20+19,n4y*20+5),(n4x*20+19,n4y*20+18),(n4x*20+14,n4y*20+14),(n4x*20+9,n4y*20+18), fill="black", outline="black", width=3, tag="fantomen4")
        canvas5.create_oval((n4x*20+1),(n4y*20+2.5),(n4x*20+8.5),(n4y*20+12),fill="white", outline="black",tag= "fantomen4")
        canvas5.create_oval((n4x*20+9.5),(n4y*20+2.5),(n4x*20+17),(n4y*20+12),fill="white", outline="black",tag= "fantomen4")
        canvas5.create_oval((n4x*20+4.5),(n4y*20+7),(n4x*20+8.5),(n4y*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen4")
        canvas5.create_oval((n4x*20+13),(n4y*20+7),(n4x*20+17),(n4y*20+12),fill="#588ffc", outline="#588ffc",tag= "fantomen4")

    #affichage des monstres
    if actif ==0:
        canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=45,fill= "yellow",tag= "pacman")
    elif actif==1:
        canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=45,fill= "green",tag= "pacman")
        canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="green",tag= "pacman")
        canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="black", outline="black",tag= "pacman")
    elif actif==2:
        canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=45,fill= "blue",tag= "pacman")
        canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="blue",tag= "pacman")
        canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="black", outline="black",tag= "pacman")
    elif actif==3:
        canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=45,fill= "red",tag= "pacman")
        canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="red",tag= "pacman")
        canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="black", outline="black",tag= "pacman")
        canvas5.create_oval((x*20+2),(y*20+6),(x*20+6),(y*20+10),fill="black", outline="black",tag= "pacman")
        canvas5.create_oval((x*20+14),(y*20+13),(x*20+18),(y*20+17),fill="black", outline="black",tag= "pacman")
        canvas5.create_oval((x*20+7),(y*20+12),(x*20+11),(y*20+16),fill="black", outline="black",tag= "pacman")
    elif actif==4:
        canvas5.create_polygon((x*20+5,y*20+14),(x*20,y*20+18),(x*20,y*20+5),(x*20+5,y*20),(x*20+14,y*20),(x*20+19,y*20+5),(x*20+19,y*20+18),(x*20+14,y*20+14),(x*20+9,y*20+18), fill="yellow", outline="yellow", width=3, tag="pacman")
        canvas5.create_oval((x*20+1),(y*20+2.5),(x*20+8.5),(y*20+12),fill="white", outline="yellow",tag= "pacman")
        canvas5.create_oval((x*20+9.5),(y*20+2.50),(x*20+17),(y*20+12),fill="white", outline="yellow",tag= "pacman")
        canvas5.create_oval((x*20+4.5),(y*20+7),(x*20+8.5),(y*20+12),fill="#588ffc", outline="#588ffc",tag= "pacman")
        canvas5.create_oval((x*20+13),(y*20+7),(x*20+17),(y*20+12),fill="#588ffc", outline="#588ffc",tag= "pacman")
    elif actif==5:
        canvas5.create_polygon((x*20+5,y*20+14),(x*20,y*20+18),(x*20,y*20+5),(x*20+5,y*20),(x*20+14,y*20),(x*20+19,y*20+5),(x*20+19,y*20+18),(x*20+14,y*20+14),(x*20+9,y*20+18), fill="white", outline="white", width=3, tag="pacman")
        canvas5.create_oval((x*20+1),(y*20+2.5),(x*20+8.5),(y*20+12),fill="white", outline="white",tag= "pacman")
        canvas5.create_oval((x*20+9.5),(y*20+2.50),(x*20+17),(y*20+12),fill="white", outline="white",tag= "pacman")
        canvas5.create_oval((x*20+4.5),(y*20+7),(x*20+8.5),(y*20+12),fill="#588ffc", outline="#588ffc",tag= "pacman")
        canvas5.create_oval((x*20+13),(y*20+7),(x*20+17),(y*20+12),fill="#588ffc", outline="#588ffc",tag= "pacman")
    elif actif==6:
        canvas5.create_polygon((x*20+5,y*20+14),(x*20,y*20+18),(x*20,y*20+5),(x*20+5,y*20),(x*20+14,y*20),(x*20+19,y*20+5),(x*20+19,y*20+18),(x*20+14,y*20+14),(x*20+9,y*20+18), fill="red", outline="white", width=3, tag="pacman")
        canvas5.create_oval((x*20+1),(y*20+2.5),(x*20+8.5),(y*20+12),fill="white", outline="white",tag= "pacman")
        canvas5.create_oval((x*20+9.5),(y*20+2.50),(x*20+17),(y*20+12),fill="white", outline="white",tag= "pacman")
        canvas5.create_oval((x*20+4.5),(y*20+7),(x*20+8.5),(y*20+12),fill="darkred", outline="darkred",tag= "pacman")
        canvas5.create_oval((x*20+13),(y*20+7),(x*20+17),(y*20+12),fill="darkred", outline="darkred",tag= "pacman")
    elif actif==7:
        canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=45,fill= "yellow",tag= "pacman")
        canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="yellow",tag= "pacman")
        canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="orange", outline="orange",tag= "pacman")
        canvas5.create_oval((x*20+2),(y*20+6),(x*20+6),(y*20+10),fill="orange", outline="orange",tag= "pacman")
        canvas5.create_oval((x*20+14),(y*20+13),(x*20+18),(y*20+17),fill="orange", outline="orange",tag= "pacman")
        canvas5.create_oval((x*20+7),(y*20+12),(x*20+11),(y*20+16),fill="orange", outline="orange",tag= "pacman")
    elif actif==8:
        canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=45,fill= "yellow",tag= "pacman")
        canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="white",tag= "pacman")
        canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="black", outline="black",tag= "pacman")

def regledujeu():
    global a
    canvas5.delete("menu")
    canvas5.delete("fantomej")
    canvas5.delete("fantomer")
    canvas5.delete("fantomeb")
    canvas5.delete("fantomev")
    canvas5.delete("fantomep")
    canvas5.delete("fantomen")
    canvas5.delete("fantomen2")
    canvas5.delete("fantomen3")
    canvas5.delete("fantomen4")
    canvas5.delete("pacman")
    canvas5.delete("level")
    canvas5.delete("argent")
    for i in range(a):
        canvas5.delete("bubul"+str(i))
        canvas5.delete("block"+str(i))

    #bouton
    canvas5.create_window(420,650, window=btretour, tags = "bonus")
    #texte
    canvas5.create_text(400,100,text="RUN FOR YOUR LIFE",fill="#08155c",font=fontregle,tags="prix2")
    canvas5.create_text(400,250,text="Vous jouez un petit personnage qui doit manger toutes les bulles.",fill="#08155c",font=fontregle,tags="regle")
    canvas5.create_text(400,300,text="Cependant, des fantômes vont vouloir vous attrapper alors il faut les éviter.",fill="#08155c",font=fontregle,tags="regle")
    canvas5.create_text(400,350,text="Pour vous déplacer, utilisez vos flèches directionnelles de votre clavier",fill="#08155c",font=fontregle,tags="prix2")



def horloge(tps):
    global fin,mort
    if fin==0 and mort==0:
        if tps>=259:
            tps=1
            sons_musiquerun.stop()
            sons_musiquerun.play()
        tps+=1
        print(tps)
        fenetre.after(1000,horloge,tps)

def commencerjeu():
    global x,y,bx,by,rx,ry,vx,vy,jx,jy,actif,bouche,fin,mort,level
    sons_musiquerun.play()
    canvas5.delete("menu")
    fin=0
    mort=0
    #règlage son
    horloge(1)
    #activation de l'animation de la bouche
    if actif==0 or actif==1 or actif==2 or actif==3 or actif==7 or actif==8:
        bouchefermée()
    else:
        bouche=3
    arbitre()
    #activation des mouvement des fantômes
    mouvementbleu()
    mouvementrouge()
    mouvementvert()
    mouvementjaune()
    mouvementpink()

    if level >=8:
        mouvementnoir()
        mouvementnoir2()
        mouvementnoir3()
        mouvementnoir4()

    #activation des touches flèches du clavier reliées aux mouvement du pacman
    canvas5.focus_set()
    canvas5.bind("<KeyRelease>", fleche)

def clic(event):
    global point,level,bonus,argent,debloque1,debloque2,debloque3,debloque4,debloque5,debloque6,debloque7,debloque8,actif
    x=event.x
    y=event.y
    if debloque1==0 and argent>=6 and bonus>=1 and 100<x<130 and 50<y<80:

        MsgBox = messagebox.askquestion ('Déguisement','Voulez vous vraiment acheter Vert ? ',icon = 'question')
        if MsgBox=="yes":
            messagebox.showinfo ('Déguisement','Vous avez acheté vert.',icon = 'info')
            argent=argent-6
            niveaux={
                  "level":    level,
                  "bonus":   bonus,
                  "argent":   argent,
                  "point":  point,
                }
            with open('donnees', 'wb') as fichier:
                mon_pickler = pickle.Pickler(fichier)
                mon_pickler.dump(niveaux)
            debloque1=1
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
            canvas5.delete("prix1")
            canvas5.create_text(120,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix1")
        else:
            messagebox.showinfo('Retour',"Vous n'avez pas acheté Vert.")

    elif argent>=6 and bonus>=2 and 185<x<215 and 50<y<80 and debloque2==0:
        MsgBox = messagebox.askquestion ('Déguisement','Voulez vous vraiment acheter Bleu ? ',icon = 'question')
        if MsgBox=="yes":
            messagebox.showinfo ('Déguisement','Vous avez acheté Bleu.',icon = 'info')
            argent=argent-6
            niveaux={
                  "level":    level,
                  "bonus":   bonus,
                  "argent":   argent,
                  "point":  point,
                }
            with open('donnees', 'wb') as fichier:
                mon_pickler = pickle.Pickler(fichier)
                mon_pickler.dump(niveaux)
            debloque2=1
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
            canvas5.delete("prix2")
            canvas5.create_text(204,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix2")
        else:
            messagebox.showinfo('Retour',"Vous n'avez pas acheté Bleu")

    elif argent>=6 and bonus>=3 and 270<x<300 and 50<y<80 and debloque3==0:
        MsgBox = messagebox.askquestion ('Déguisement','Voulez vous vraiment acheter Coccinelle  ? ',icon = 'question')
        if MsgBox=="yes":
            messagebox.showinfo ('Déguisement','Vous avez acheté Coccinelle.',icon = 'info')
            argent=argent-6
            niveaux={
                  "level":    level,
                  "bonus":   bonus,
                  "argent":   argent,
                  "point":  point,
                }
            with open('donnees', 'wb') as fichier:
                mon_pickler = pickle.Pickler(fichier)
                mon_pickler.dump(niveaux)
            debloque3=1
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
            canvas5.delete("prix3")
            canvas5.create_text(289,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix3")
        else:
            messagebox.showinfo('Retour',"Vous n'avez pas acheté Coccinelle.")

    elif argent>=6 and bonus>=4 and 355<x<385 and 50<y<80 and debloque4==0:
        MsgBox = messagebox.askquestion ('Déguisement','Voulez vous vraiment acheter PacMan-Fantôme ? ',icon = 'question')
        if MsgBox=="yes":
            messagebox.showinfo ('Déguisement','Vous avez acheté PacMan-Fantôme.',icon = 'info')
            argent=argent-6
            niveaux={
                  "level":    level,
                  "bonus":   bonus,
                  "argent":   argent,
                  "point":  point,
                }
            with open('donnees', 'wb') as fichier:
                mon_pickler = pickle.Pickler(fichier)
                mon_pickler.dump(niveaux)
            debloque4=1
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
            canvas5.delete("prix4")
            canvas5.create_text(374,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix4")
        else:
            messagebox.showinfo('Retour',"Vous n'avez pas acheté PacMan-Fantôme")

    elif argent>=6 and bonus>=5 and 440<x<470 and 50<y<80 and debloque5==0:
        MsgBox = messagebox.askquestion ('Déguisement','Voulez vous vraiment acheter Fantôme ? ',icon = 'question')
        if MsgBox=="yes":
            messagebox.showinfo ('Déguisement','Vous avez acheté Fantôme.',icon = 'info')
            argent=argent-6
            niveaux={
                  "level":    level,
                  "bonus":   bonus,
                  "argent":   argent,
                  "point":  point,
                }
            with open('donnees', 'wb') as fichier:
                mon_pickler = pickle.Pickler(fichier)
                mon_pickler.dump(niveaux)
            debloque5=1
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
            canvas5.delete("prix5")
            canvas5.create_text(459,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix5")
        else:
            messagebox.showinfo('Retour',"Vous n'avez pas acheté Fantôme")

    elif argent>=6 and bonus>=6 and 525<x<555 and 50<y<80 and debloque6==0:
        MsgBox = messagebox.askquestion ('Déguisement','Voulez vous vraiment acheter Fantôme-Ensanglanté ? ',icon = 'question')
        if MsgBox=="yes":
            messagebox.showinfo ('Déguisement','Vous avez acheté Fantôme-Ensanglanté.',icon = 'info')
            argent=argent-6
            niveaux={
                  "level":    level,
                  "bonus":   bonus,
                  "argent":   argent,
                  "point":  point,
                }
            with open('donnees', 'wb') as fichier:
                mon_pickler = pickle.Pickler(fichier)
                mon_pickler.dump(niveaux)
            debloque6=1
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
            canvas5.delete("prix6")
            canvas5.create_text(544,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix6")
        else:
            messagebox.showinfo('Retour',"Vous n'avez pas acheté Fantôme-Ensanglanté")

    elif argent>=6 and  bonus>=7 and 605<x<635 and 50<y<80 and debloque7==0:
        MsgBox = messagebox.askquestion ('Déguisement','Voulez vous vraiment acheter Camembert ? ',icon = 'question')
        if MsgBox=="yes":
            messagebox.showinfo ('Déguisement','Vous avez acheté Camembert.',icon = 'info')
            argent=argent-6
            niveaux={
                  "level":    level,
                  "bonus":   bonus,
                  "argent":   argent,
                  "point":  point,
                }
            with open('donnees', 'wb') as fichier:
                mon_pickler = pickle.Pickler(fichier)
                mon_pickler.dump(niveaux)
            debloque7=1
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
            canvas5.delete("prix7")
            canvas5.create_text(625,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix7")
        else:
            messagebox.showinfo('Retour',"Vous n'avez pas acheté Camembert")

    elif argent>=6 and bonus>=8 and 690<x<720 and 50<y<80 and debloque8==0:
        MsgBox = messagebox.askquestion ('Déguisement','Voulez vous vraiment acheter  Maître-PacMan ? ',icon = 'question')
        if MsgBox=="yes":
            messagebox.showinfo ('Déguisement','Vous avez acheté Maître-PacMan.',icon = 'info')
            argent=argent-6
            niveaux={
                  "level":    level,
                  "bonus":   bonus,
                  "argent":   argent,
                  "point":  point,
                }
            with open('donnees', 'wb') as fichier:
                mon_pickler = pickle.Pickler(fichier)
                mon_pickler.dump(niveaux)
            debloque8=1
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
            canvas5.delete("prix8")
            canvas5.create_text(709,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix8")
        else:
            messagebox.showinfo('Retour',"Vous n'avez pas acheté Maître-PacMan")

    if debloque1==1 and 100<x<130 and 50<y<80:
        Msg = messagebox.askquestion ('Déguisement','Voulez vous vraiment équiper Vert ? ',icon = 'question')
        if Msg== "yes":
            messagebox.showinfo("déguisement","Vous avez équipé Vert.")
            actif=1
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
        else:
            messagebox.showinfo("déguisement", "Vous n'avez pas équipé Vert.")

    elif debloque2==1 and 185<x<215 and 50<y<80:
        Msg = messagebox.askquestion ('Déguisement','Voulez vous vraiment équiper Bleu ? ',icon = 'question')
        if Msg== "yes":
            messagebox.showinfo("déguisement","Vous avez équipé Bleu.")
            actif=2
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
        else:
            messagebox.showinfo("déguisement", "Vous n'avez pas équipé Bleu.")

    elif debloque3==1 and 270<x<300 and 50<y<80:
        Msg = messagebox.askquestion ('Déguisement','Voulez vous vraiment équiper Coccinelle ? ',icon = 'question')
        if Msg== "yes":
            messagebox.showinfo("déguisement","Vous avez équipé Coccinelle.")
            actif=3
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
        else:
            messagebox.showinfo("déguisement", "Vous n'avez pas équipé Coccinelle.")

    elif debloque4==1 and 355<x<385 and 50<y<80:
        Msg = messagebox.askquestion ('Déguisement','Voulez vous vraiment équiper PacMan-Fantôme ? ',icon = 'question')
        if Msg== "yes":
            messagebox.showinfo("déguisement","Vous avez équipé PacMan-Fantôme.")
            actif=4
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
        else:
            messagebox.showinfo("déguisement", "Vous n'avez pas équipé PacMan-Fantôme.")

    elif debloque5==1 and 440<x<470 and 50<y<80:
        Msg = messagebox.askquestion ('Déguisement','Voulez vous vraiment équiper Fantôme ? ',icon = 'question')
        if Msg== "yes":
            messagebox.showinfo("déguisement","Vous avez équipé Fantôme.")
            actif=5
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
        else:
            messagebox.showinfo("déguisement", "Vous n'avez pas équipé Fantôme.")

    elif debloque6==1 and 525<x<555 and 50<y<80:
        Msg = messagebox.askquestion ('Déguisement','Voulez vous vraiment équiper Fantôme-Ensanglanté ? ',icon = 'question')
        if Msg== "yes":
            messagebox.showinfo("déguisement","Vous avez équipé Fantôme-Ensanglanté.")
            actif=6
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
        else:
            messagebox.showinfo("déguisement", "Vous n'avez pas équipé Fantôme-Ensanglanté.")

    elif debloque7==1 and 605<x<635 and 50<y<80:
        Msg = messagebox.askquestion ('Déguisement','Voulez vous vraiment équiper Camembert ? ',icon = 'question')
        if Msg== "yes":
            messagebox.showinfo("déguisement","Vous avez équipé Camembert.")
            actif=7
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
        else:
            messagebox.showinfo("déguisement", "Vous n'avez pas équipé Camembert.")

    elif debloque8==1 and 690<x<720 and 50<y<80:
        Msg = messagebox.askquestion ('Déguisement','Voulez vous vraiment équiper Maître-PacMan ? ',icon = 'question')
        if Msg== "yes":
            messagebox.showinfo("déguisement","Vous avez équipé Maître-PacMan.")
            actif=8
            debloquage={
              "debloque1":debloque1,
              "debloque2":debloque2,
              "debloque3":debloque3,
              "debloque4":debloque4,
              "debloque5":debloque5,
              "debloque6":debloque6,
              "debloque7":debloque7,
              "debloque8":debloque8,
              "actif":actif,
            }
            with open('récompenses', 'wb') as fichier2:
                mon_pickler_recompenses= pickle.Pickler(fichier2)
                mon_pickler_recompenses.dump(debloquage)
        else:
            messagebox.showinfo("déguisement", "Vous n'avez pas équipé Maître-PacMan.")



def skin():
    global a,bonus
    canvas5.delete("menu")
    canvas5.delete("fantomej")
    canvas5.delete("fantomer")
    canvas5.delete("fantomeb")
    canvas5.delete("fantomev")
    canvas5.delete("fantomep")
    canvas5.delete("fantomen")
    canvas5.delete("fantomen2")
    canvas5.delete("fantomen3")
    canvas5.delete("fantomen4")
    canvas5.delete("pacman")
    canvas5.delete("level")
    canvas5.delete("argent")

    for i in range(a):
        canvas5.delete("bubul"+str(i))
        canvas5.delete("block"+str(i))
      # on synchronise la fonction skin avvec le click
    canvas5.bind("<Button-1>",clic)
    #fond
    #première plaque
    canvas5.create_rectangle((40, 120, 745, 160), outline="#781a00", fill="#781a00", width=2 ,tag= "bonus")
    canvas5.create_polygon((40,120),(90,60),(795,60),(745,120), outline="brown", fill="brown", width=2,tag= "bonus")
    canvas5.create_polygon((745,160),(745,120),(795,60),(795,100), outline="#781a00", fill="#781a00", width=2,tag= "bonus")
    #deuxième plaque
    canvas5.create_rectangle((202.5, 360, 602.5, 400), outline="#781a00", fill="#781a00", width=2 ,tag= "bonus")
    canvas5.create_polygon((202.5,360),(277.5,300),(677.5,300),(602.5,360), outline="brown", fill="brown", width=2,tag= "bonus")
    canvas5.create_polygon((602.5,400),(602.5,360),(677.5,300),(677.5,340), outline="#781a00", fill="#781a00", width=2,tag= "bonus")

    if bonus>=1:
        canvas5.create_arc(100,50,100+30,50+30,extent=300,start=45,fill= "green",tag= "bonus")
        canvas5.create_oval((100+8),(50+1+1/3),(100+14+4.667),(50+8+2.667),fill="white", outline="green",tag= "bonus")
        canvas5.create_oval((100+10+3.333),(50+4+1.333),(100+14+4.667),(50+8+2.667),fill="black", outline="black",tag= "bonus")
        canvas5.create_text(115,90,text="LEVEL 2",fill="#08155c",font=fontregle,tags="bonus")
        if debloque1==0:
            #affichage des prix
            canvas5.create_oval((125),(100),(145),(120),fill="orange", outline="orange",tag= "prix1")
            canvas5.create_oval((130),(105),(140),(115),fill="brown", outline="orange",tag= "prix1")
            canvas5.create_text(102,110,text="Prix:6",fill="#08155c",font=fontregle,tags="prix1")
        else:
            canvas5.delete("prix1")
            canvas5.create_text(120,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix1")
    if bonus>=2:
        active=2
        canvas5.create_arc(185,50,185+30,50+30,extent=300,start=45,fill= "blue",tag= "bonus")
        canvas5.create_oval((185+8),(50+1+1/3),(185+14+4.667),(50+8+2.667),fill="white", outline="blue",tag= "bonus")
        canvas5.create_oval((185+10+3.333),(50+4+1.333),(185+14+4.667),(50+8+2.667),fill="black", outline="black",tag= "bonus")
        canvas5.create_text(200,90,text="LEVEL 3",fill="#08155c",font=fontregle,tags="bonus")
        if debloque2==0:
            #affichage des prix
            canvas5.create_oval((210),(100),(230),(120),fill="orange", outline="orange",tag= "prix2")
            canvas5.create_oval((215),(105),(225),(115),fill="brown", outline="orange",tag= "prix2")
            canvas5.create_text(187,110,text="Prix:6",fill="#08155c",font=fontregle,tags="prix2")
        else:
            canvas5.delete("prix2")
            canvas5.create_text(204,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix2")
    if bonus>=3:
        canvas5.create_arc(270,50,270+30,50+30,extent=300,start=45,fill= "red",tag= "bonus")
        canvas5.create_oval((270+8),(50+1+1/3),(270+14+4.667),(50+8+2.667),fill="white", outline="red",tag= "bonus")
        canvas5.create_oval((270+10+3.333),(50+4+1.333),(270+14+4.667),(50+8+2.667),fill="black", outline="black",tag= "bonus")
        canvas5.create_oval((260+10+3.333),(55+4+1.333),(260+14+4.667),(55+8+2.667),fill="black", outline="black",tag= "bonus")
        canvas5.create_oval((278+10+3.333),(65+4+1.333),(278+14+4.667),(65+8+2.667),fill="black", outline="black",tag= "bonus")
        canvas5.create_oval((268+10+3.333),(63+4+1.333),(268+14+4.667),(63+8+2.667),fill="black", outline="black",tag= "bonus")
        canvas5.create_text(285,90,text="LEVEL 4",fill="#08155c",font=fontregle,tags="bonus")
        if debloque3==0:
            #affichage des prix
            canvas5.create_oval((295),(100),(315),(120),fill="orange", outline="orange",tag= "prix3")
            canvas5.create_oval((300),(105),(310),(115),fill="brown", outline="orange",tag= "prix3")
            canvas5.create_text(272,110,text="Prix:6",fill="#08155c",font=fontregle,tags="prix3")
        else:
            canvas5.delete("prix3")
            canvas5.create_text(289,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix3")
    if bonus>=4:
        canvas5.create_polygon((355+5+1.667,50+14+4.667),(355,50+18+6),(355,50+5+1.667),(355+5+1.667,50),(355+14+4.667,50),(355+19+6.333,50+5+1.667),(355+19+6.333,50+18+6),(355+14+4.667,50+14+4.667),(355+9+3,50+18+6), fill="yellow", outline="yellow", width=3, tag="bonus")
        canvas5.create_oval((355+1+0.333),(50+2.5+0.833),(355+8.5+2.833),(50+12+4),fill="white", outline="yellow",tag= "bonus")
        canvas5.create_oval((355+9.5+3.167),(50+2.50+0.833),(355+17+5.667),(50+12+4),fill="white", outline="yellow",tag= "bonus")
        canvas5.create_oval((355+4.5+1.5),(50+7+2.333),(355+8.5+2.833),(50+12+4),fill="#588ffc", outline="#588ffc",tag= "bonus")
        canvas5.create_oval((355+13+4.333),(50+7+2.333),(355+17+5.667),(50+12+4),fill="#588ffc", outline="#588ffc",tag= "bonus")
        canvas5.create_text(370,90,text="LEVEL 5",fill="#08155c",font=fontregle,tags="bonus")
        if debloque4==0:
            #affichage des prix
            canvas5.create_oval((380),(100),(400),(120),fill="orange", outline="orange",tag= "prix4")
            canvas5.create_oval((385),(105),(395),(115),fill="brown", outline="orange",tag= "prix4")
            canvas5.create_text(357,110,text="Prix:6",fill="#08155c",font=fontregle,tags="prix4")
        else:
            canvas5.delete("prix4")
            canvas5.create_text(374,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix4")
    if bonus>=5:
        canvas5.create_polygon((440+5+1.667,50+14+4.667),(440,50+18+6),(440,50+5+1.667),(440+5+1.667,50),(440+14+4.667,50),(440+19+6.333,50+5+1.667),(440+19+6.333,50+18+6),(440+14+4.667,50+14+4.667),(440+9+3,50+18+6), fill="white", outline="white", width=3, tag="bonus")
        canvas5.create_oval((440+1+0.333),(50+2.5+0.833),(440+8.5+2.833),(50+12+4),fill="white", outline="white",tag= "bonus")
        canvas5.create_oval((440+9.5+3.167),(50+2.50+0.833),(440+17+5.667),(50+12+4),fill="white", outline="white",tag= "bonus")
        canvas5.create_oval((440+4.5+1.5),(50+7+2.333),(440+8.5+2.833),(50+12+4),fill="#588ffc", outline="#588ffc",tag= "bonus")
        canvas5.create_oval((440+13+4.333),(50+7+2.333),(440+17+5.667),(50+12+4),fill="#588ffc", outline="#588ffc",tag= "bonus")
        canvas5.create_text(455,90,text="LEVEL 6",fill="#08155c",font=fontregle,tags="bonus")
        if debloque5==0:
            #affichage des prix
            canvas5.create_oval((465),(100),(485),(120),fill="orange", outline="orange",tag= "prix5")
            canvas5.create_oval((470),(105),(480),(115),fill="brown", outline="orange",tag= "prix5")
            canvas5.create_text(443,110,text="Prix:6",fill="#08155c",font=fontregle,tags="prix5")
        else:
            canvas5.delete("prix5")
            canvas5.create_text(459,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix5")
    if bonus>=6:
        canvas5.create_polygon((525+5+1.667,50+14+4.667),(525,50+18+6),(525,50+5+1.667),(525+5+1.667,50),(525+14+4.667,50),(525+19+6.333,50+5+1.667),(525+19+6.333,50+18+6),(525+14+4.667,50+14+4.667),(525+9+3,50+18+6), fill="red", outline="white", width=3, tag="bonus")
        canvas5.create_oval((525+1+0.333),(50+2.5+0.833),(525+8.5+2.833),(50+12+4),fill="white", outline="white",tag= "bonus")
        canvas5.create_oval((525+9.5+3.167),(50+2.50+0.833),(525+17+5.667),(50+12+4),fill="white", outline="white",tag= "bonus")
        canvas5.create_oval((525+4.5+1.5),(50+7+2.333),(525+8.5+2.833),(50+12+4),fill="darkred", outline="darkred",tag= "bonus")
        canvas5.create_oval((525+13+4.333),(50+7+2.333),(525+17+5.667),(50+12+4),fill="darkred", outline="darkred",tag= "bonus")
        canvas5.create_text(540,90,text="LEVEL 7",fill="#08155c",font=fontregle,tags="bonus")
        if debloque6==0:
            #affichage des prix
            canvas5.create_oval((550),(100),(570),(120),fill="orange", outline="orange",tag= "prix6")
            canvas5.create_oval((555),(105),(565),(115),fill="brown", outline="orange",tag= "prix6")
            canvas5.create_text(527,110,text="Prix:6",fill="#08155c",font=fontregle,tags="prix6")
        else:
            canvas5.delete("prix8")
            canvas5.create_text(709,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix8")
    if bonus>=7:
        canvas5.create_arc(605,50,605+30,50+30,extent=300,start=45,fill= "yellow",tag= "bonus")
        canvas5.create_oval((605+10+3.333),(50+4+1.333),(605+14+4.667),(50+8+2.667),fill="orange", outline="orange",tag= "bonus")
        canvas5.create_oval((595+10+3.333),(55+4+1.333),(595+14+4.667),(55+8+2.667),fill="orange", outline="orange",tag= "bonus")
        canvas5.create_oval((613+10+3.333),(65+4+1.333),(613+14+4.667),(65+8+2.667),fill="orange", outline="orange",tag= "bonus")
        canvas5.create_oval((603+10+3.333),(63+4+1.333),(603+14+4.667),(63+8+2.667),fill="orange", outline="orange",tag= "bonus")
        canvas5.create_text(620,90,text="LEVEL 8",fill="#08155c",font=fontregle,tags="bonus")
        #affichage des fantomes démons en dessous
        canvas5.create_polygon((355+5+1.667,290+14+4.667),(355,290+18+6),(355,290+5+1.667),(355+5+1.667,290),(355+14+4.667,290),(355+19+6.333,290+5+1.667),(355+19+6.333,290+18+6),(355+14+4.667,290+14+4.667),(355+9+3,290+18+6), fill="black", outline="black", width=3, tag="bonus")
        canvas5.create_oval((355+1+0.333),(290+2.5+0.833),(355+8.5+2.833),(290+12+4),fill="white", outline="black",tag= "bonus")
        canvas5.create_oval((355+9.5+3.167),(290+2.50+0.833),(355+17+5.667),(290+12+4),fill="white", outline="black",tag= "bonus")
        canvas5.create_oval((355+4.5+1.5),(290+7+2.333),(355+8.5+2.833),(290+12+4),fill="#588ffc", outline="#588ffc",tag= "bonus")
        canvas5.create_oval((355+13+4.333),(290+7+2.333),(355+17+5.667),(290+12+4),fill="#588ffc", outline="#588ffc",tag= "bonus")
        #un autre
        canvas5.create_polygon((440+5+1.667,290+14+4.667),(440,290+18+6),(440,290+5+1.667),(440+5+1.667,290),(440+14+4.667,290),(440+19+6.333,290+5+1.667),(440+19+6.333,290+18+6),(440+14+4.667,290+14+4.667),(440+9+3,290+18+6), fill="black", outline="black", width=3, tag="bonus")
        canvas5.create_oval((440+1+0.333),(290+2.5+0.833),(440+8.5+2.833),(290+12+4),fill="white", outline="black",tag= "bonus")
        canvas5.create_oval((440+9.5+3.167),(290+2.50+0.833),(440+17+5.667),(290+12+4),fill="white", outline="black",tag= "bonus")
        canvas5.create_oval((440+4.5+1.5),(290+7+2.333),(440+8.5+2.833),(290+12+4),fill="#588ffc", outline="#588ffc",tag= "bonus")
        canvas5.create_oval((440+13+4.333),(290+7+2.333),(440+17+5.667),(290+12+4),fill="#588ffc", outline="#588ffc",tag= "bonus")
        #encore un autre
        canvas5.create_polygon((525+5+1.667,290+14+4.667),(525,290+18+6),(525,290+5+1.667),(525+5+1.667,290),(525+14+4.667,290),(525+19+6.333,290+5+1.667),(525+19+6.333,290+18+6),(525+14+4.667,290+14+4.667),(525+9+3,290+18+6), fill="black", outline="black", width=3, tag="bonus")
        canvas5.create_oval((525+1+0.333),(290+2.5+0.833),(525+8.5+2.833),(290+12+4),fill="white", outline="black",tag= "bonus")
        canvas5.create_oval((525+9.5+3.167),(290+2.50+0.833),(525+17+5.667),(290+12+4),fill="white", outline="black",tag= "bonus")
        canvas5.create_oval((525+4.5+1.5),(290+7+2.333),(525+8.5+2.833),(290+12+4),fill="#588ffc", outline="#588ffc",tag= "bonus")
        canvas5.create_oval((525+13+4.333),(290+7+2.333),(525+17+5.667),(290+12+4),fill="#588ffc", outline="#588ffc",tag= "bonus")
        #un petit dernier pour la route
        canvas5.create_polygon((605+5+1.667,290+14+4.667),(605,290+18+6),(605,290+5+1.667),(605+5+1.667,290),(605+14+4.667,290),(605+19+6.333,290+5+1.667),(605+19+6.333,290+18+6),(605+14+4.667,290+14+4.667),(605+9+3,290+18+6), fill="black", outline="black", width=3, tag="bonus")
        canvas5.create_oval((605+1+0.333),(290+2.5+0.833),(605+8.5+2.833),(290+12+4),fill="white", outline="black",tag= "bonus")
        canvas5.create_oval((605+9.5+3.167),(290+2.50+0.833),(605+17+5.667),(290+12+4),fill="white", outline="black",tag= "bonus")
        canvas5.create_oval((605+4.5+1.5),(290+7+2.333),(605+8.5+2.833),(290+12+4),fill="#588ffc", outline="#588ffc",tag= "bonus")
        canvas5.create_oval((605+13+4.333),(290+7+2.333),(605+17+5.667),(290+12+4),fill="#588ffc", outline="#588ffc",tag= "bonus")
        canvas5.create_text(310,310,text="LEVEL 8 :",fill="#08155c",font=fontregle,tags="bonus")
        canvas5.create_text(470,340,text="Ajout de quatre fantômes démoniaques",fill="#08155c",font=fontregle,tags="bonus")
        if debloque7==0:
            #affichage des prix
            canvas5.create_oval((630),(100),(650),(120),fill="orange", outline="orange",tag= "prix7")
            canvas5.create_oval((635),(105),(645),(115),fill="brown", outline="orange",tag= "prix7")
            canvas5.create_text(607,110,text="Prix:6",fill="#08155c",font=fontregle,tags="prix7")
        else:
            canvas5.delete("prix7")
            canvas5.create_text(625,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix7")
    if bonus>=8:
        canvas5.create_arc(690,50,690+30,50+30,extent=300,start=45,fill= "yellow",tag= "bonus")
        canvas5.create_oval((690+8),(50+1+1/3),(690+14+4.667),(50+8+2.667),fill="white", outline="white",tag= "bonus")
        canvas5.create_oval((690+10+3.333),(50+4+1.333),(690+14+4.667),(50+8+2.667),fill="black", outline="black",tag= "bonus")
        canvas5.create_text(705,90,text="LEVEL 9",fill="#08155c",font=fontregle,tags="bonus")
        if debloque8==0:
            #affichage des prix
            canvas5.create_oval((715),(100),(735),(120),fill="orange", outline="orange",tag= "prix8")
            canvas5.create_oval((720),(105),(730),(115),fill="brown", outline="orange",tag= "prix8")
            canvas5.create_text(693,110,text="Prix:6",fill="#08155c",font=fontregle,tags="prix8")
        else:
            canvas5.delete("prix8")
            canvas5.create_text(709,110,text="Débloqué",fill="#08155c",font=fontregle,tags="prix8")


    canvas5.create_window(420,650, window=btretour, tags = "bonus")


def propalskinBF():
    global x,y,actif,sens
    if sens==1:
        if actif==0:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=130,fill= "yellow",tag="pacman")
        elif actif==1:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=130,fill= "green",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+6),(x*20+9),(y*20+12),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+4),(y*20+6),(x*20+8),(y*20+10),fill="black", outline="black",tag= "pacman")
        elif actif==2:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=130,fill= "blue",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+6),(x*20+9),(y*20+12),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+4),(y*20+6),(x*20+8),(y*20+10),fill="black", outline="black",tag= "pacman")
        elif actif==3:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=130,fill= "red",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+6),(x*20+9),(y*20+12),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+4),(y*20+6),(x*20+8),(y*20+10),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+6),(y*20+14),(x*20+10),(y*20+18),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+13),(y*20+6),(x*20+17),(y*20+2),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+12),(y*20+9),(x*20+16),(y*20+13),fill="black", outline="black",tag= "pacman")

        elif actif==7:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=130,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+6),(x*20+9),(y*20+12),fill="white", outline="yellow",tag= "pacman")
            canvas5.create_oval((x*20+4),(y*20+6),(x*20+8),(y*20+10),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+6),(y*20+14),(x*20+10),(y*20+18),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+13),(y*20+6),(x*20+17),(y*20+2),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+12),(y*20+9),(x*20+16),(y*20+13),fill="orange", outline="orange",tag= "pacman")
        elif actif==8:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=130,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+6),(x*20+9),(y*20+12),fill="white", outline="white",tag= "pacman")
            canvas5.create_oval((x*20+4),(y*20+6),(x*20+8),(y*20+10),fill="black", outline="black",tag= "pacman")
    elif sens==2:
        if actif==0:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=-45,fill= "yellow",tag="pacman")
        elif actif==1:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=-45,fill= "green",tag= "pacman")
            canvas5.create_oval((x*20+11),(y*20+7),(x*20+18),(y*20+13),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+12),(y*20+9),(x*20+16),(y*20+13),fill="black", outline="black",tag= "pacman")
        elif actif==2:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=-45,fill= "blue",tag= "pacman")
            canvas5.create_oval((x*20+11),(y*20+7),(x*20+18),(y*20+13),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+12),(y*20+9),(x*20+16),(y*20+13),fill="black", outline="black",tag= "pacman")
        elif actif==3:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=-45,fill= "red",tag= "pacman")
            canvas5.create_oval((x*20+11),(y*20+7),(x*20+18),(y*20+13),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+12),(y*20+9),(x*20+16),(y*20+13),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+9),(y*20+2),(x*20+13),(y*20+6),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+3),(y*20+14),(x*20+7),(y*20+18),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+4),(y*20+7),(x*20+8),(y*20+11),fill="black", outline="black",tag= "pacman")
        elif actif==7:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=-45,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+11),(y*20+7),(x*20+18),(y*20+13),fill="white", outline="yellow",tag= "pacman")
            canvas5.create_oval((x*20+12),(y*20+9),(x*20+16),(y*20+13),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+9),(y*20+2),(x*20+13),(y*20+6),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+3),(y*20+14),(x*20+7),(y*20+18),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+4),(y*20+7),(x*20+8),(y*20+11),fill="orange", outline="orange",tag= "pacman")
        elif actif==8:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=-45,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+11),(y*20+7),(x*20+18),(y*20+13),fill="white", outline="white",tag= "pacman")
            canvas5.create_oval((x*20+12),(y*20+9),(x*20+16),(y*20+13),fill="black", outline="black",tag= "pacman")
    elif sens==3:
        if actif==0:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=190,fill= "yellow",tag="pacman")
        elif actif==1:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=190,fill= "green",tag= "pacman")
            canvas5.create_oval((x*20+6),(y*20+1),(x*20+12),(y*20+8),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+7),(y*20+4),(x*20+10),(y*20+8),fill="black", outline="black",tag= "pacman")
        elif actif==2:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=190,fill= "blue",tag= "pacman")
            canvas5.create_oval((x*20+6),(y*20+1),(x*20+12),(y*20+8),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+7),(y*20+4),(x*20+10),(y*20+8),fill="black", outline="black",tag= "pacman")
        elif actif==3:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=190,fill= "red",tag= "pacman")
            canvas5.create_oval((x*20+6),(y*20+1),(x*20+12),(y*20+8),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+7),(y*20+4),(x*20+10),(y*20+8),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+14),(y*20+6),(x*20+18),(y*20+11),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+13),(x*20+6),(y*20+17),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+9),(y*20+12),(x*20+13),(y*20+16),fill="black", outline="black",tag= "pacman")
        elif actif==7:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=190,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+6),(y*20+1),(x*20+12),(y*20+8),fill="white", outline="yellow",tag= "pacman")
            canvas5.create_oval((x*20+7),(y*20+4),(x*20+10),(y*20+8),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+14),(y*20+6),(x*20+18),(y*20+11),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+13),(x*20+6),(y*20+17),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+9),(y*20+12),(x*20+13),(y*20+16),fill="orange", outline="orange",tag= "pacman")
        elif actif==8:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=190,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+6),(y*20+1),(x*20+12),(y*20+8),fill="white", outline="white",tag= "pacman")
            canvas5.create_oval((x*20+7),(y*20+4),(x*20+10),(y*20+8),fill="black", outline="black",tag= "pacman")
    elif sens==4:
        if actif==0:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=45,fill= "yellow",tag="pacman")
        elif actif==1:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=45,fill= "green",tag= "pacman")
            canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="black", outline="black",tag= "pacman")
        elif actif==2:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=45,fill= "blue",tag= "pacman")
            canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="black", outline="black",tag= "pacman")
        elif actif ==3:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=45,fill= "red",tag= "pacman")
            canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+6),(x*20+6),(y*20+10),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+14),(y*20+13),(x*20+18),(y*20+17),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+7),(y*20+12),(x*20+11),(y*20+16),fill="black", outline="black",tag= "pacman")
        elif actif==7:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=45,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="yellow",tag= "pacman")
            canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+6),(x*20+6),(y*20+10),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+14),(y*20+13),(x*20+18),(y*20+17),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+7),(y*20+12),(x*20+11),(y*20+16),fill="orange", outline="orange",tag= "pacman")
        elif actif==8:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=359,start=45,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="white",tag= "pacman")
            canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="black", outline="black",tag= "pacman")
def propalskinBO():
    global x,y,actif,sens
    if sens==1:
        if actif==0:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=130,fill= "yellow", tag= "pacman")
        elif actif==1:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=130,fill= "green",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+6),(x*20+9),(y*20+12),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+4),(y*20+6),(x*20+8),(y*20+10),fill="black", outline="black",tag= "pacman")
        elif actif==2:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=130  ,fill= "blue",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+6),(x*20+9),(y*20+12),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+4),(y*20+6),(x*20+8),(y*20+10),fill="black", outline="black",tag= "pacman")
        elif actif==3:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=130,fill= "red",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+6),(x*20+9),(y*20+12),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+4),(y*20+6),(x*20+8),(y*20+10),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+6),(y*20+14),(x*20+10),(y*20+18),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+13),(y*20+6),(x*20+17),(y*20+2),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+12),(y*20+9),(x*20+16),(y*20+13),fill="black", outline="black",tag= "pacman")
        elif actif==7:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=130,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+6),(x*20+9),(y*20+12),fill="white", outline="yellow",tag= "pacman")
            canvas5.create_oval((x*20+4),(y*20+6),(x*20+8),(y*20+10),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+6),(y*20+14),(x*20+10),(y*20+18),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+13),(y*20+6),(x*20+17),(y*20+2),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+12),(y*20+9),(x*20+16),(y*20+13),fill="orange", outline="orange",tag= "pacman")
        elif actif==8:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=130,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+6),(x*20+9),(y*20+12),fill="white", outline="white",tag= "pacman")
            canvas5.create_oval((x*20+4),(y*20+6),(x*20+8),(y*20+10),fill="black", outline="black",tag= "pacman")
    elif sens==2:
        if actif==0:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=-45,fill= "yellow", tag= "pacman")
        elif actif==1:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=-45,fill= "green",tag= "pacman")
            canvas5.create_oval((x*20+11),(y*20+7),(x*20+18),(y*20+13),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+12),(y*20+9),(x*20+16),(y*20+13),fill="black", outline="black",tag= "pacman")
        elif actif==2:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=-45,fill= "blue",tag= "pacman")
            canvas5.create_oval((x*20+11),(y*20+7),(x*20+18),(y*20+13),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+12),(y*20+9),(x*20+16),(y*20+13),fill="black", outline="black",tag= "pacman")
        elif actif==3:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=-45,fill= "red",tag= "pacman")
            canvas5.create_oval((x*20+11),(y*20+7),(x*20+18),(y*20+13),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+12),(y*20+9),(x*20+16),(y*20+13),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+9),(y*20+2),(x*20+13),(y*20+6),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+3),(y*20+14),(x*20+7),(y*20+18),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+4),(y*20+7),(x*20+8),(y*20+11),fill="black", outline="black",tag= "pacman")
        elif actif==7:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=-45,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+11),(y*20+7),(x*20+18),(y*20+13),fill="white", outline="yellow",tag= "pacman")
            canvas5.create_oval((x*20+12),(y*20+9),(x*20+16),(y*20+13),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+9),(y*20+2),(x*20+13),(y*20+6),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+3),(y*20+14),(x*20+7),(y*20+18),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+4),(y*20+7),(x*20+8),(y*20+11),fill="orange", outline="orange",tag= "pacman")
        elif actif==8:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=-45,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+11),(y*20+7),(x*20+18),(y*20+13),fill="white", outline="white",tag= "pacman")
            canvas5.create_oval((x*20+12),(y*20+9),(x*20+16),(y*20+13),fill="black", outline="black",tag= "pacman")
    elif sens==3:
        if actif==0:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=190,fill= "yellow", tag= "pacman")
        elif actif==1:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=190,fill= "green",tag= "pacman")
            canvas5.create_oval((x*20+6),(y*20+1),(x*20+12),(y*20+8),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+7),(y*20+4),(x*20+10),(y*20+8),fill="black", outline="black",tag= "pacman")
        elif actif==2:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=190,fill= "blue",tag= "pacman")
            canvas5.create_oval((x*20+6),(y*20+1),(x*20+12),(y*20+8),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+7),(y*20+4),(x*20+10),(y*20+8),fill="black", outline="black",tag= "pacman")
        elif actif==3:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=190,fill= "red",tag= "pacman")
            canvas5.create_oval((x*20+6),(y*20+1),(x*20+12),(y*20+8),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+7),(y*20+4),(x*20+10),(y*20+8),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+14),(y*20+6),(x*20+18),(y*20+11),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+13),(x*20+6),(y*20+17),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+9),(y*20+12),(x*20+13),(y*20+16),fill="black", outline="black",tag= "pacman")
        elif actif==7:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=190,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+6),(y*20+1),(x*20+12),(y*20+8),fill="white", outline="yellow",tag= "pacman")
            canvas5.create_oval((x*20+7),(y*20+4),(x*20+10),(y*20+8),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+14),(y*20+6),(x*20+18),(y*20+11),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+13),(x*20+6),(y*20+17),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+9),(y*20+12),(x*20+13),(y*20+16),fill="orange", outline="orange",tag= "pacman")
        elif actif==8:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=190,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+6),(y*20+1),(x*20+12),(y*20+8),fill="white", outline="white",tag= "pacman")
            canvas5.create_oval((x*20+7),(y*20+4),(x*20+10),(y*20+8),fill="black", outline="black",tag= "pacman")
    elif sens==4:
        if actif==0:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=45,fill= "yellow", tag= "pacman")
        elif actif==1:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=45,fill= "green",tag= "pacman")
            canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="black", outline="black",tag= "pacman")
        elif actif==2:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=45,fill= "blue",tag= "pacman")
            canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="black", outline="black",tag= "pacman")
        elif actif==3:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=45,fill= "red",tag= "pacman")
            canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="red",tag= "pacman")
            canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+6),(x*20+6),(y*20+10),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+14),(y*20+13),(x*20+18),(y*20+17),fill="black", outline="black",tag= "pacman")
            canvas5.create_oval((x*20+7),(y*20+12),(x*20+11),(y*20+16),fill="black", outline="black",tag= "pacman")
        elif actif==7:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=45,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="yellow",tag= "pacman")
            canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+2),(y*20+6),(x*20+6),(y*20+10),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+14),(y*20+13),(x*20+18),(y*20+17),fill="orange", outline="orange",tag= "pacman")
            canvas5.create_oval((x*20+7),(y*20+12),(x*20+11),(y*20+16),fill="orange", outline="orange",tag= "pacman")
        elif actif==8:
            canvas5.create_arc(x*20,y*20,x*20+20,y*20+20,extent=300,start=45,fill= "yellow",tag= "pacman")
            canvas5.create_oval((x*20+8),(y*20+1),(x*20+14),(y*20+8),fill="white", outline="white",tag= "pacman")
            canvas5.create_oval((x*20+10),(y*20+4),(x*20+14),(y*20+8),fill="black", outline="black",tag= "pacman")
#boutons
btretour = Button(fenetre, text="Retour",command=commencer)
btcommencer = Button(fenetre, text="Commencer",command=commencerjeu)
btskin = Button(fenetre, text="Déguisement",command=skin)
btregle = Button(fenetre, text="Règles",command=regledujeu)
#configuration des boutons
btretour.config(width= 19, height = 3,bg="yellow", fg="black", font="-size 14")
btcommencer.config(width= 14, height = 3,bg="yellow", fg="black", font="-size 14")
btskin.config(width= 14, height = 3,bg="yellow", fg="black", font="-size 14")
btregle.config(width= 14, height = 3,bg="yellow", fg="black", font="-size 14")
commencer()
canvas5.pack()
fenetre.mainloop()
sons_musiquerun.stop()
