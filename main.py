import pygame
from menus import*
from escenario import *
import threading
import os

# Se inicializan variables utiles  
displayWidth = 375
displayHeight = 500
clock = pygame.time.Clock()

# Se inicializa pygame
pygame.init()
frame = pygame.display.set_mode((displayWidth, displayHeight))

    
# ===== Main ===== #
#El metodo main inicia el programa y la animacion inicial y luego pasa al menu
#E: Ninguna
#S: Ninguna, realiza acciones
def main():
    #Se establece el frame
    frame = pygame.display.set_mode((displayWidth, displayHeight))
    pygame.display.set_caption('Game')
    #Se realizala animacion inicial
    animar()
    bcg5=frame.copy()
    #Se crea el menu y se pasa a este
    men=Menu(bcg5)
    men.dibujar(frame)
    men.esperar(frame)
    
#Se lleva a cabo la animacion inicial
#E: Ninguna
#S: Ninguna, realiza acciones
#R: Ninguna
def animar():
    #Se definen las imagenes del corazon
    heart1 = pygame.image.load(os.path.join('imagenes', 'heart.png')).convert()
    heart1.set_colorkey((255,255,255))
    heart2 = pygame.image.load(os.path.join('imagenes', 'heart2.png')).convert_alpha()

    #Se crea una plataforma y se posiciona
    plat= Plataforma(25, 50*6,"final")
    plat.x+=12

    #Se crea una princesa y se dibuja
    princesa=Princesa(plat)
    princesa.dibujar(frame)
    #Se crea el mono y se posiciona
    mono=Mono(plat)
    mono.x=plat.x+plat.ancho//5
    mono.y=0
    #Se crean los peldanos de la plataforma y se dibuja esta
    plat.crear()
    plat.dibujar(frame)
    #Se crea el primer fondo
    bcg1=frame.copy()
    #Se crea mario y se posiciona
    mario =Mario(plat)
    mario.x=plat.x+plat.ancho-25

    #Se incia la musica
    pygame.mixer.music.load(os.path.join('musica', 'intro1.ogg'))
    pygame.mixer.music.play()        

    #Mario se mueve
    for i in range(0,25):
        mario.mover("izquierda")
        frame.blit(bcg1, (0,0))
        mario.dibujar(frame)
        pygame.display.flip()
        clock.tick(15)
    #Se cambia la imagen de mario a parado
    frame.blit(bcg1, (0,0))
    mario.imagen=mario.parado_izq
    mario.dibujar(frame)
    #Se crea el fondo 2
    bcg2=frame.copy()
    #Se dibija el corazon 1
    frame.blit(heart1,(princesa.x+princesa.ancho+50,princesa.y+15))
    #Se crea el fondo 3
    bcg3=frame.copy()
    #Se anima la caida del mono
    animationFlag=True
    #Se define la velocidad del mono v
    v=0
    while animationFlag:
        v+=1
        mono.y+=v
        #Se para la animacion si el mono llega a la plataforma
        if mono.y+mono.alto>plat.y:
            mono.y=plat.y-mono.alto
            animationFlag=False
        #Se dibuja el mono y el fondo
        frame.blit(bcg3, (0,0))
        mono.dibujar(frame)
        pygame.display.flip()
        clock.tick(15)

    #Se animan los movimientos del mono
    frame.blit(bcg2, (0,0))
    bcg4=frame.copy()
    mono.dibujar(frame)
    pygame.display.flip()
    mono.imagenes=[mono.imagenes[0]]+mono.imagenes[4:]
    for i in range(0,8):
        mono.siguiente_img()
        frame.blit(bcg4, (0,0))
        mono.dibujar(frame)
        pygame.display.flip()
        clock.tick(5)
    #Se dibuja el corazon 2
    frame.blit(heart2,(princesa.x+princesa.ancho+50,princesa.y-30))
    pygame.display.flip()
    
# Ejecutar
main()
