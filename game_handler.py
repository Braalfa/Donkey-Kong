from escenario import *
from game import Partida
import tkinter as tk
from tkinter import simpledialog
import time

# ===== Game_handler ===== #
#La clase game handler maneja un juego con todos sus niveles
class Game_handler():
    #E: Un frame
    #R: Se espera que sea frame, pero solo lo asumee
    def __init__(self,frame):
        #Se crean los tres escenarios
        escenario1= self.crear_escenario(4)
        escenario2= self.crear_escenario(6)
        escenario3= self.crear_escenario(8)
        self.escenarios=[escenario1, escenario2, escenario3]
        #Se crea la partida
        self.parti= Partida(self.escenarios, frame)
        
    #Iniciar maneja todo el juego
    #E: Ninguna(solo self)
    #S: Ninguna, realiza acciones
    #R: Ninguna
    def iniciar(self):
        self.parti.iniciar()
        
        #Se manejan los eventos del usuario, para hacer a mario moverse y brincar
        while self.parti.vidas>0 and self.parti.nivel<3:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                        self.parti.stop=True
                        while self.parti.hilo_animacion.is_alive():
                            pass
                        pygame.quit()
                        quit()
                if event.type== pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.parti.animacion.animationFlag_abaj=True
                    elif event.key == pygame.K_UP:
                        self.parti.animacion.animationFlag_arr=True         
                    elif event.key == pygame.K_RIGHT:
                        self.parti.animacion.animationFlag_der=True
                    elif event.key == pygame.K_LEFT:
                        self.parti.animacion.animationFlag_izq=True
                    elif event.key == pygame.K_SPACE:
                        self.parti.animacion.mario.animationFlag_brinco=True
                        self.parti.animacion.mario.velocidad_brinco=-13
        
                        while self.parti.animacion.mario.animationFlag_brinco:
                            events=pygame.event.get(pygame.KEYDOWN)
                            for event in events:
                                if event.key != pygame.K_SPACE:
                                    pygame.event.post(event)
                                    
                            events=pygame.event.get(pygame.KEYUP)
                            for event in events:
                                pygame.event.post(event)
                                
                            pass

                if event.type== pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.parti.animacion.animationFlag_abaj=False
                    if event.key == pygame.K_UP:
                        self.parti.animacion.animationFlag_arr=False
                    if event.key == pygame.K_RIGHT:
                        self.parti.animacion.animationFlag_der=False
                        if isinstance(self.parti.animacion.mario.objeto_posicion, Plataforma):
                            self.parti.animacion.mario.marioestatico_der()
                    if event.key == pygame.K_LEFT:
                        self.parti.animacion.animationFlag_izq=False
                        if isinstance(self.parti.animacion.mario.objeto_posicion, Plataforma):
                            self.parti.animacion.mario.marioestatico_izq()
             
    
        pygame.mixer.music.stop()
        root=tk.Tk()
        root.iconify()
        root.geometry("30x30+100+100")
        #Se le pregunta el nombre al usuario
        nombre= simpledialog.askstring("Nombre", "Cual es su nombre?", parent=root)
        print(nombre)
        root.destroy()
        if isinstance(nombre, str):
            #Se actualiza el salon de la fama
            self.actualizar_salonfama(nombre, self.parti.puntos)

    
    #Se actualiza el salon de la fama
    #E: Un String y un entero
    #S: Ninguna, realiza acciones
    #R: No se hacen restricciones, se asume que la entrada es correcta
    def actualizar_salonfama(self,nombre, puntaje):
        #Se lee el salon de la fama actual
        salon= open("salonDeLaFama.txt","r")
        lineas=salon.readlines()
        #Se crea una lista con el nuevo salon de la fama
        puntajes= self.nuevo_puntaje(nombre,puntaje, lineas,0)
        salon.close()
        #Se guardan los tres primeros lugares en la lista
        salon= open("salonDeLaFama.txt","w")
        salon.writelines(puntajes[:6])
        salon.close()

    #Se agrega un puntaje y nombre a la lista de salon de la fama
        
    #E: Un String, un entero, una lista de strings y un entero(indice)
    #S: Se retorna una lista con los puntajes y jugadores ordenados
    #R: No se hacen restricciones, se asume que la entrada es correcta
    def nuevo_puntaje(self,nombre, puntaje, lineas, i):
        if i==len(lineas):
            return lineas
        elif i%2==0 and puntaje>int(lineas[i]):
            lineas = lineas[:i] +[str(puntaje)+"\n"]+ [nombre+"\n"] + lineas[i:]
            return lineas
        else:
            return self.nuevo_puntaje(nombre, puntaje, lineas, i+1)

    #Se crea un escenario de acuerdo con la cantidad de plataformas requeridas
    #E: Un entero, la cantidad de plataformas
    #S: Se retorna un escenario
    #R: No se hacen restricciones, se asume que la entrada es correcta
    def crear_escenario(self,cantidad_plataformas):
        plataformas=[]
        escaleras=[]
        #Se crean las plataformas y se agregan a la lista de plataformas
        for i in range(0,cantidad_plataformas+1):
            if i==0:
                plat= Plataforma(25, 50*(cantidad_plataformas+1),"inicial")
            elif i==cantidad_plataformas-1:
                plat= Plataforma(25, 50*2,"final")
            elif i==cantidad_plataformas:
                plat= Plataforma(100, 50,"princesa")
            elif i%2==1:
                plat= Plataforma(25, 50*(cantidad_plataformas+1-i),"decreciente")
            elif i%2==0:
                plat= Plataforma(50, 50*(cantidad_plataformas+1-i),"creciente")
            plat.crear()
            plataformas.append(plat)
        #Se crean las escaleras y se agregan a la lista de escaleras
        for i in range(0,cantidad_plataformas):
            if i==0:
                esc1=[Escalera(plataformas[i].ancho_escalon*10+plataformas[i].x, plataformas[i],plataformas[i+1])]
                esc1[0].crear()
                esc2=[]
            elif i==cantidad_plataformas-1:
                esc1=[Escalera(plataformas[i+1].ancho+plataformas[i+1].x-plataformas[i+1].ancho_escalon//2, plataformas[i],plataformas[i+1])]
                esc1[0].crear()
                esc2=[]
            elif i%2==0:
                esc1=[Escalera(plataformas[i].ancho_escalon*9+plataformas[i].x, plataformas[i],plataformas[i+1])]
                esc2=[Escalera(plataformas[i].ancho_escalon*6+plataformas[i].x, plataformas[i],plataformas[i+1])]

                esc1[0].crear()
                esc2[0].crear()
            elif i%2==1:
                esc1=[Escalera(plataformas[i].ancho_escalon*2+plataformas[i].x, plataformas[i],plataformas[i+1])]
                esc2=[Escalera(plataformas[i].ancho_escalon*4+plataformas[i].x, plataformas[i],plataformas[i+1])]
                esc1[0].crear()
                esc2[0].crear()
            escaleras=escaleras+esc1+esc2
        #Se establecen las escaleras dentro de las plataformas
        for plat in plataformas:
            plat.establecer_escaleras(escaleras)
        escenario=Escenario(plataformas, escaleras)
        return escenario
