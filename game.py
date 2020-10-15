import pygame
from pygame import Surface
import os
import random
import threading
from escenario import *

# Se inicializa pygame
pygame.init()
pygame.font.init()
        

# ===== Mario ===== #
#La clase mario es la clase del jugador
class Mario:
    #E: Un objeto, plataforma o escalera
    #R: -
    def __init__(self, objeto_posicion):

        #Se establecen booleanos sobre el movimiento de mario
        self.animationFlag_izq=False
        self.animationFlag_arr=False
        self.animationFlag_abaj=False
        self.animationFlag_der=False
        self.animationFlag_brinco=False
        
        #Se establece la longitud  de los movimientos y la direccion
        self.paso=4
        self.direccion=0

        #Se establece el objeto en el que se encuentra mario
        self.objeto_posicion=objeto_posicion 

        #Se establece la velocidad del brinco
        self.velocidad_brinco=0

        #Se cargan los sprites de mario
        self.spriteSheet = pygame.image.load(os.path.join('imagenes', 'mario.png'))

        #Se definen las imagenes sin movimiento
        self.spriteSheet.set_clip(10, 1, 12, 16)
        self.parado_izq = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert_alpha()
        self.parado_izq.set_colorkey((255,255,255))
        self.spriteSheet.set_clip(92,18, 12, 16)
        self.parado_der = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert_alpha()
        

        #Se definen las imagenes de caminar y brincar a la izquierda
        self.spriteSheet.set_clip(29, 1, 15, 16)
        caminar_izq1 = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert_alpha()
        self.spriteSheet.set_clip(48, 2, 15, 15)
        caminar2_izq2 = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert_alpha()
        self.spriteSheet.set_clip(92, 2, 12, 15)
        self.brincar_izq = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert_alpha()
        self.img_izq=[caminar_izq1,caminar2_izq2]
        
        #Se definen las imagenes de caminar y brincar a la derecha
        self.spriteSheet.set_clip(71, 19, 15, 16)
        caminar_der1 = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert_alpha()
        self.spriteSheet.set_clip(51, 19,15, 15)
        caminar2_der2 = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert_alpha()
        self.spriteSheet.set_clip(9, 19, 12, 16)
        self.brincar_der = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert_alpha()
        self.img_der=[caminar_der1,caminar2_der2]

        #Se definen las imagenes de subir
        self.spriteSheet.set_clip(29, 18, 12, 16)
        subir_der = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert_alpha()
        self.spriteSheet.set_clip(72, 1, 13, 16)
        subir_izq = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert_alpha()

        #Se define la imagen de muerto
        self.spriteSheet.set_clip(111, 2, 16, 16)
        self.muerto = self.spriteSheet.subsurface(self.spriteSheet.get_clip()).convert_alpha()

        #Se agregan a una lista las imagenes de subir
        self.img_subir=[subir_izq,subir_der]
        
        #Se define el indice de la imagen actual en la lista
        self.img_indice = 0
        
        #Se define un booleano para saber si se debe de cambiar de imagen
        self.cambiar_img_escalera=True
        
        #Se define una variable que almacena el numero de plataforma actual 
        self.ind_plat=0
        #Se define una variable que almacena el numero mas alto de plataformas en las que ha estado mario
        self.ind_plat_max=0

        #Se define la imagen inicial
        self.imagen = self.parado_der

        #Se definen las propiedades geometricas
        self.altura = self.imagen.get_rect().size[1]
        self.ancho = self.imagen.get_rect().size[0]
        self.y = objeto_posicion.y -self.altura
        self.x = objeto_posicion.x

        #Se define el rect
        self.rect= self.imagen.get_rect(topleft=(self.x, self.y))

    #Se mueve mario en la direccion indicada
    #E: Un string ( la direccion a la que va)
    #S:
    #R:
    def mover(self, direccion):
        if isinstance(self.objeto_posicion, Plataforma):
            #Se ejecuta si mario esta en una plataforma
            if direccion=="derecha" and self.objeto_posicion.ancho + self.objeto_posicion.x>=self.x+self.ancho+self.paso:
                #Se ejecuta si mario no se va a salir de la plataforma
                self.mover_der()
            elif direccion=="izquierda" and self.objeto_posicion.x<=self.x-self.paso:
                #Se ejecuta si mario no se va a salir de la plataforma
                self.mover_izq()
            elif direccion == "arriba" and not(self.animationFlag_brinco):
                #Se ejecuta si mario no esta brincando
                escalera= self.hay_escaleras_iniciales()
                if isinstance(escalera,Escalera):
                    #Se ejecuta si mario esta sobre una escalera
                    self.mover_arr_inicio(escalera)
            elif direccion == "abajo" and not(self.animationFlag_brinco):
                #Se ejecuta si mario no esta brincando
                escalera= self.hay_escaleras_finales()
                if isinstance(escalera,Escalera):
                    #Se ejecuta si mario esta sobre una escalera
                    self.mover_abaj_inicio(escalera)
            if self.animationFlag_brinco:
                #Se ejecuta si mario esta brincando y no se esta moviendo
                self.brincar(direccion)
        
                
        elif isinstance(self.objeto_posicion, Escalera):
            #Se ejecuta si mario esta en una escalera
            if direccion == "arriba":
                self.mover_arr()
            elif direccion == "abajo":
                self.mover_abaj()
            if self.animationFlag_brinco:
                #Si esta en una escalera no se puede brincar
                self.animationFlag_brinco=False
                self.velocidad_brinco=0
        #Se actualiza el rect
        self.actualizar_rect()

    #Se mueve a la derecha
    #E: Ninguna (solo self)
    #S:-
    #R:-
    def mover_der(self):
        self.x += self.paso
        #Si esta brincando la posicion y se cambia en otra funcion
        if not(self.animationFlag_brinco):
            self.y = self.objeto_posicion.altura(self.x)-self.altura
            self.imagen=self.img_der[self.img_indice]
            self.img_indice=(self.img_indice+1)%2
        else:
            self.imagen=self.brincar_der

    #Se mueve a la izquierda
    #E: Ninguna (solo self)
    #S:-
    #R:-
    def mover_izq(self):
        self.x -= self.paso
        #Si esta brincando la posicion y se cambia en otra funcion
        if not(self.animationFlag_brinco):
            self.y = self.objeto_posicion.altura(self.x)-self.altura
            self.imagen=self.img_izq[self.img_indice]
            self.img_indice=(self.img_indice+1)%2
        else:
            self.imagen=self.brincar_izq


    #Se ejecuta esta funcion para empezar a subir la escalera
    #E: Una escalera
    #S:-
    #R:-
    def mover_arr_inicio(self,escalera):
            #Se cambia el objeto actual a la escalera
            self.objeto_posicion= escalera
            self.y-= self.paso
            #Se cambia a la imagen de subir escalera
            self.imagen=self.img_subir[self.img_indice]
            self.img_indice=(self.img_indice+1)%2

    #Se ejecuta esta funcion para empezar a bajar la escalera
    #E: Una escalera
    #S:-
    #R:-
    def mover_abaj_inicio(self,escalera):
            #Se cambia el objeto actual a la escalera
            self.objeto_posicion= escalera
            self.y+= self.paso
            #Se cambia a la imagen de subir escalera
            self.imagen=self.img_subir[self.img_indice]
            self.img_indice=(self.img_indice+1)%2

    #Se mueva hacia abajo cuando se esta en una escalera
    #E: Ninguna (solo self)
    #S:-
    #R:-
    def mover_abaj(self):
        #Si se va a salir de la imagen de la escalera se cambia el objeto posicion a plataforma
        if self.objeto_posicion.inicioy-self.altura<self.y+self.paso: 
            self.y=self.objeto_posicion.inicioy-self.altura
            self.objeto_posicion= self.objeto_posicion.plataforma1
            self.img_indice=0
            self.ind_plat-=1
        else:
            self.y+= self.paso
            if self.cambiar_img_escalera:
                self.imagen=self.img_subir[self.img_indice]
                self.img_indice=(self.img_indice+1)%2

    #Se mueva hacia arriba cuando se esta en una escalera
    #E: Ninguna (solo self)
    #S:-
    #R:-
    def mover_arr(self):
        #Si se va a salir de la imagen de la escalera se cambia el objeto posicion a plataforma
        if self.objeto_posicion.finaly-self.altura>self.y-self.paso: 
            self.y=self.objeto_posicion.finaly-self.altura
            self.objeto_posicion= self.objeto_posicion.plataforma2
            self.img_indice=0
            self.ind_plat+=1
            if self.ind_plat>self.ind_plat_max:
                self.ind_plat_max = self.ind_plat
        else:
            self.y-= self.paso
            if self.cambiar_img_escalera:
                self.imagen=self.img_subir[self.img_indice]
                self.img_indice=(self.img_indice+1)%2

    #Se cambia la posicion y de acuerdo a la velocidad del brinco
    #E: Un String (la direccion del brinco)
    #S:-
    #R:-
    def brincar(self, direccion):
        altura_obj=self.objeto_posicion.altura(self.x)
        #Si ya va a caer se cambia el objeto a tipo plataforma
        if self.y+self.velocidad_brinco>altura_obj-self.altura:
            self.y=altura_obj-self.altura
            self.animationFlag_brinco=False
            self.velocidad_brinco=0
            if(self.imagen is self.brincar_der):        
                self.imagen=self.parado_der
            else:
                self.imagen=self.parado_izq
        #Si no se cumple lo anterior, se aumenta la velocidad de caida y se cambia la imagen apropiadamente
        else:
            self.y+=self.velocidad_brinco
            self.velocidad_brinco+=3
            if( direccion=="" and not(self.imagen is self.brincar_der or self.imagen is self.brincar_izq)):
                if(self.imagen is self.parado_der or self.imagen is self.img_der[0] or self.imagen is self.img_der[1] ):
                    self.imagen=self.brincar_der
                else:
                    self.imagen=self.brincar_izq

    #Se actualiza el rect de mario
    #E: Ninguna (solo self)
    #S:-
    #R:-
    def actualizar_rect(self):
        self.rect.topleft= (self.x,self.y)

        
    #Se analiza si hay escaleras de tipo inicial en la posicion actual de mario y se retorna la escalera si existe
    #E: Ninguna (solo self)
    #S: Retorna una escalera si Mario esta en frente de la parte inicial de una escalera, sino retorna un string de error 
    #R:-
    def hay_escaleras_iniciales(self):
        for escalera in self.objeto_posicion.escaleras_iniciales:
            if escalera.rect1.collidepoint(self.x+self.ancho//2, self.y):
                return escalera
        return "error"
        
    #Se analiza si hay escaleras de tipo final en la posicion actual de mario y se retorna la escalera si existe    
    #E: Ninguna (solo self)
    #S: Retorna una escalera si Mario esta en frente de la parte final de una escalera, sino retorna un string de error 
    #R:-
    def hay_escaleras_finales(self):
        for escalera in self.objeto_posicion.escaleras_finales:
            if escalera.rect1.collidepoint(self.x+self.ancho//2, self.y):
                return escalera
        return "error"

    #Se cambia la imagen de mario a estatico
    #E: Ninguna (solo self)
    #S:-
    #R:-
    def marioestatico_izq(self):
        self.imagen=self.parado_izq
        self.img_indice=0
        
    #Se cambia la imagen de mario a estatico
    #E: Ninguna (solo self)
    #S:-
    #R:-
    def marioestatico_der(self):
        self.imagen=self.parado_der
        self.img_indice=0

    #Se dibuja mario en el frame
    #E: Un frame
    #S:-
    #R:-
    def dibujar(self, frame):
        frame.blit(self.imagen, (self.x, self.y))


# ===== Obstaculo ===== #
#La clase obstaculo es la clase de los barriles
class Obstaculo():
    #E: Una lista de plataformas
    #R: -
    def __init__(self,plataformas):
        #Se establece un booleano que indica si el barril cae
        self.cae=False
        #Se establece la cantidad de desplazamiento
        self.paso=5
        #Se establece la direccion inicial
        self.direccion=1
        
        #Se deinen las imagenes de obstaculo y se agregan a una lista
        img1 = pygame.image.load(os.path.join('imagenes', 'barril1.gif'))
        img2 = pygame.image.load(os.path.join('imagenes', 'barril2.gif'))
        img3 = pygame.image.load(os.path.join('imagenes', 'barril3.gif'))
        img4 = pygame.image.load(os.path.join('imagenes', 'barril4.gif'))
        self.imagenes=[img1,img2,img3,img4]
        #Se establece la imagen inicial
        self.imagen = img1

         #Se establecen las plataformas del juego
        self.plataformas=plataformas
        #Se establece el indice de plataforma actual
        self.i = len(plataformas)-2

        #Se establecen las propiedades geometricas
        self.altura = self.imagen.get_rect().size[1]
        self.ancho = self.imagen.get_rect().size[0]
        self.x = plataformas[self.i].x+35+60
        self.y = plataformas[self.i].y- self.altura

       
        #Se establece el rect
        self.rect= self.imagen.get_rect(topleft=(self.x, self.y))


    #Aqui se mueve el obstaculo
    #E:Un entero, el cual indica la direccion del movimiento
    #S:-
    #R:-
    def mover(self, direccion):
        plat= self.plataformas[self.i]
        escalera = plat.buscar_escalera(self.x+self.ancho//2-self.paso//2, self.x+self.ancho//2+self.paso//2, "final")
        #Si en la plataforma actual hay una escalera y no esta en esa escalera, empieza a caer
        if isinstance(escalera, Escalera) and not(self.cae):
            rand=random.randint(0,1)
            if rand==0:
                self.x+= direccion*self.paso
                self.y = plat.altura(self.x)- self.altura

            else:
                self.y+=self.paso
                self.i= self.i-1
                self.cae=True
        #Si esta cayendo sigue cayendo hasta llegar a la plataforma de abajo
        elif self.cae:
            altura =plat.altura(self.x)
            if self.y+self.paso>= altura -self.altura:
                self.y= altura- self.altura
                self.cae=False
            else:
                self.y+= self.paso
        #Dependiendo del tipo de plataforma en la que esta, asi se mueve
        elif (plat.tipo=="decreciente" or plat.tipo=="final") and plat.x+plat.ancho+1<self.x:
            self.cae=True
            self.y+=self.paso
            self.i= self.i-1
        elif plat.tipo=="creciente" and plat.x+1>self.x+self.ancho:
            self.cae=True
            self.y+=self.paso
            self.i= self.i-1
        elif plat.tipo=="inicial" and plat.x>self.x+self.paso:
            self.cae=True
            self.i=-1
        else:
            self.x+= direccion*self.paso
            self.y = plat.altura(self.x)- self.altura
        if(self.cae):
            self.direccion=0
        else:
            self.direccion=direccion
        self.rect.topleft= (self.x,self.y)

    #Aqui se dibuja el obstaculo en el frame
    #E:Un frame (Surface)
    #S:-
    #R:-
    def dibujar(self, frame):
        frame.blit(self.imagen, (self.x, self.y))

# ===== Animacion ===== #
#La clase animacion es la que maneja las animaciones
class Animacion():
    #E: Un Surface(background), un Surface(frame), Mario,Princesa,Mono, una lista de plataformas, un entero(frames per second), Partida
    #R:-
    def __init__(self, background, frame,mario, princesa, mono, plataformas,FPS, partida):
        self.clock = pygame.time.Clock()
        #Se establecen los personajes
        self.mario= mario
        self.princesa=princesa
        self.mono=mono
        #Se establece el fondo, las plataformas y el frame
        self.plat= plataformas
        self.bkg = background
        self.frame=frame

        #Se establecen los booleanos de mover a mario en cierta direccion
        self.animationFlag_izq = False
        self.animationFlag_arr = False
        self.animationFlag_abaj = False
        self.animationFlag_der = False

        #Se establece la lista de obstaculos existentes
        self.obstaculos = []

        #Se establecen booleanos que indican si mario gano o choco
        self.gano=False
        self.choque=False

        #Se establecen los fps
        self.FPS=FPS
        self.part=partida

        #Se leen las configuraciones para establecer la dificultad
        conf= open("config.txt","r")
        lineas=conf.readlines()
        conf.close()
        self.dificultad=1
        if lineas[1]=="dificil\n":
            self.dificultad=2
        #Se establece la imagen del corazon
        self.heart = pygame.image.load(os.path.join('imagenes', 'heart.png')).convert()
        self.heart.set_colorkey((255,255,255))

    #Cambia el atributo de ganar a True si mario esta en la plataforma de la princesa y esta viendo hacia ella
    #E: Ninguna (solo self)
    #S:-
    #R:-
    def mario_gana(self):
        if self.mario.objeto_posicion is self.plat[len(self.plat)-1] and self.mario.imagen is self.mario.img_izq[0]:
            self.gano=True

    #Devuelve True si mario choca con algun obstaculo
    #E: Ninguna (solo self)
    #S: Un booleano, True si Mario colisiona con algun barril, False si no
    #R:-
    def hay_choque(self):
        for obs in self.obstaculos:       
            if self.colision( obs) :
                return True
        return False

    #Devuelve True si mario colisiona con un objeto
    #E: Un obstaculo
    #S: Un booleano, True si Mario colisiona con un barril, False si no
    #R:-
    def colision(self,obs):        
        if obs.rect.colliderect(self.mario.rect):
            #Se ejecuta esta linea si los rect de mario y el objeto colisionan
            pixelarray=pygame.PixelArray(obs.imagen)
            n=pixelarray.shape[0]
            m=pixelarray.shape[1]
            return self.colision_aux(obs, n,m,0,0, pixelarray)
        else:
            return False
        
    #Se analiza si mario choca con la imagen circular del obstaculo, no solo con el rect    
    def colision_aux(self,obs,n,m,i,j, pxarray):
        if i==n:
            return False
        elif j==m:
            return self.colision_aux(obs, n,m,i+1,0, pxarray)
        else:
            if self.mario.rect.collidepoint(obs.x+j, obs.y+i) and pxarray[i,j] !=0 and pxarray[i,j] !=16 :
                return True  
            else:
                return self.colision_aux(obs, n,m,i,j+1, pxarray)

    #Se calcula el numero de brincos exitosos
    #E: Ninguna (solo self)
    #S: Un entero, la cantidad de obstaculos brincados
    #R:-
    def brincos_exitosos(self):
        suma=0
        for obs in self.obstaculos:
            if isinstance(self.mario.objeto_posicion, Plataforma) and (self.mario.y+self.mario.altura)<(obs.y) and (self.mario.objeto_posicion is obs.plataformas[obs.i]) :
                #Se llega aqui si mario esta en una plataforma y si mario y el objeto cumplen las condiciones en y para un brinco exitoso
                if obs.direccion > self.mario.direccion:
                    suma+= self.brincos_exitosos_aux(obs, self.mario)
                elif obs.direccion < self.mario.direccion:
                    suma+= self.brincos_exitosos_aux(self.mario, obs)
        return suma

    #Devuelve 1 si en el eje x cumplen las condiciones de brinco
    #Positivo es el objeto que va para la derecha y negativo el que va para la izquierda
    def brincos_exitosos_aux(self, positivo,negativo):
        if(positivo.x+positivo.ancho//2)<(negativo.x+negativo.ancho//2) and (positivo.x+positivo.ancho//2+positivo.paso*positivo.direccion)>=(negativo.x+negativo.ancho//2+negativo.paso*negativo.direccion):
            return 1
        else:
            return 0

    #Actualiza el frame de acuero a las nuevas  posiciones
    #E: Ninguna(solo self)
    #S: -
    #R: -
    def actualizar(self):
        #Se dibujan los indicadores de vida, nivel, puntos
        self.frame.blit(self.bkg, (0,0))
        font = pygame.font.SysFont("comicsansms",15)
        nivel_img=font.render("Nivel: "+str((self.part.nivel+1)), True, (255,255,255))
        self.frame.blit(nivel_img, (275,10))
        pts_img=font.render("Puntos: "+str((self.part.puntos)), True, (255,255,255))
        self.frame.blit(pts_img, (275,30))
        vds_img=font.render("Vidas: "+str((self.part.vidas)), True, (255,255,255))
        self.frame.blit(vds_img, (275,50))

        #Se dibujan la princesa, el mono y los obstaculos
        self.princesa.dibujar(self.frame)
        self.mono.dibujar(self.frame)
        for obs in self.obstaculos:
            obs.dibujar(self.frame)
        self.mario.dibujar(self.frame)
        #Si mario gana, se dibuja el corazon
        if self.gano:
            self.frame.blit(self.heart,(self.princesa.x+self.princesa.ancho+40,self.princesa.y+15))
            pygame.display.flip()
            pygame.mixer.music.load(os.path.join('musica', 'win.ogg'))
            pygame.mixer.music.play()
            self.clock.tick(0.3)
        pygame.display.flip()

    #Esta funcion crea un nuevo obstaculo y la agrega a la lista de obstaculos
    #E: Ninguna(solo self)
    #S: -
    #R: -
    def crear_obstaculo(self):
        obs= Obstaculo(self.plat)
        self.obstaculos.append(obs)


    #Esta funcion elimina un obstaculo de la lista de obstaculos
    #E: Un obstaculo
    #S: -
    #R: -
    def eliminar_obstaculo(self, obs):
        i=0
        for obstaculo in self.obstaculos:
            if obstaculo is obs:
                self.obstaculos= self.obstaculos[:i]+ self.obstaculos[i+1:]
                return
            i=i+1


    #Esta funcion se encarga de animar
    #E: Un numero, la cantidad de iteraciones animadas
    #S: -
    #R: -
    def animar(self, iteraciones):
        #Se camian las imagenes dependiendo del numero de iteracion
        if iteraciones%(70//self.dificultad)==30//self.dificultad:
            self.crear_obstaculo()
        if iteraciones%26==0:
            self.mario.cambiar_img_escaleras=True
            self.moverMario()
            self.mario.cambiar_img_escaleras=False
        else:
            self.moverMario()
        if iteraciones%(10//self.dificultad)==0:
            self.mono.siguiente_img()
        if iteraciones%3==0:
            self.princesa.siguiente_img()
        #Se mueven los obstaculos
        for obs in self.obstaculos:
            obs.imagen=obs.imagenes[iteraciones%4]
            obs.mover((-1)**(obs.i+1) )
            if obs.i==-1:
                self.eliminar_obstaculo(obs)
        #Si calcula si hay choque y se cambian los atributos de clase apropiadamente
        if self.hay_choque():
            self.choque=True
            self.mario.imagen= self.mario.muerto
            pygame.mixer.music.load(os.path.join('musica', 'lose.ogg'))
            pygame.mixer.music.play()
        self.mario_gana()

        #Se actualiza la pantalla
        self.actualizar()

        #Si hay choque se espera un momento
        if self.choque:
            self.clock.tick(0.25)
        self.clock.tick(self.FPS)
        
    #Esta funcion mueve a mario dependiendo de loss valores de los atributos booleanos   
    #E: Ninguna (self)
    #S: -
    #R: -
    def moverMario(self):
        if self.animationFlag_izq:
            self.mario.mover("izquierda")
            self.mario.direccion=-1
        elif self.animationFlag_der:
            self.mario.mover("derecha")
            self.mario.direccion=1
        elif self.animationFlag_abaj:
            self.mario.mover("abajo")
        elif self.animationFlag_arr:
            self.mario.mover("arriba")
        elif self.mario.animationFlag_brinco:
            self.mario.direccion=0
            self.mario.mover("")
            
# ===== Partida ===== #
#La clase partida maneja una partida
class Partida():
    #E: Una lista de escenarios, un Surface(frame)
    #R: -
    def __init__(self, escenarios, frame):
        #Se establecen la cantidad de vidas de acuerdo a las configuraciones
        conf= open("config.txt","r")
        lineas=conf.readlines()
        conf.close()
        if lineas[0]=="vds5\n":
            self.vidas=5
        elif lineas[0]=="vds3\n":
            self.vidas=3
        
        #Se establece la manera de lograr puntos segun las configuraciones
        
        if lineas[2]=="no-plat\n":
            self.plat_cuenta=False
        else:
            self.plat_cuenta=True
            
        if lineas[3]=="no-brinco\n":
            self.brinco_cuenta=False
        else:
            self.brinco_cuenta=True

        if lineas[4]=="no-nivel\n":
            self.nivel_cuenta=False
        else:
            self.nivel_cuenta=True


        #Se inicia en nivel 0 y 0 puntos
        self.nivel=0
        self.puntos=0
        #Se establecen los escenarios, el frame y el cuadro de gameover
        self.escenarios=escenarios
        self.frame=frame
        self.gameover_rect= Boton("Game Over",80,190,200,25,(255,255,255))
        #Se establece la animacion
        self.FPS=15
        self.animacion=""
        self.hilo_animacion=""
        #Se establece la variable de salir del juego
        self.stop=False

    #Se inicia la animacion
    #E: Ninguna (self)
    #S: -
    #R: -
    def iniciar(self):

        pygame.mixer.music.load(os.path.join('musica', 'bacmusic.wav'))
        pygame.mixer.music.play(-1)
        
        clock = pygame.time.Clock()
        #Se escoje el escenario dependiendo del nivel
        escenario = self.escenarios[self.nivel]
        plataformas = escenario.plataformas
        #Se dibuja el escenario
        escenario.dibujar(self.frame)
        #Se crea mario, la princesa y el mono
        mario = Mario(plataformas[0])
        princesa= Princesa(plataformas[len(plataformas)-1])
        mono=Mono(plataformas[len(plataformas)-2])
        #Se crea la animacion
        self.animacion = Animacion(escenario.bkg, self.frame, mario, princesa, mono, plataformas,self.FPS, self)

        #Se inicia el hilo de animar
        self.hilo_animacion= threading.Thread(target=self.animar, args=())
        self.hilo_animacion.start()

    #Se anima
    #E: Ninguna (self)
    #S: -
    #R: -
    def animar(self):
        iteraciones=0
        plat_max=0

        #Se ejecuta mientras mario no choque ni gane
        while not(self.animacion.choque or self.animacion.gano or self.stop) :
            brincos=self.animacion.brincos_exitosos()
            self.animacion.animar(iteraciones)
            iteraciones+=1
            #Se actualiza la puntuacion de acuerdo a las configuraciones
            if self.brinco_cuenta: 
                self.puntos+=brincos
            if self.plat_cuenta:
                self.puntos+=(self.animacion.mario.ind_plat_max-plat_max)
                plat_max=self.animacion.mario.ind_plat_max
        #Si el juego se debe de parar se termina la ejecucion
        if not self.stop:
            #Se cambian las vidas y nivel dependiendo de como termino el juego
            if self.animacion.gano:
                if self.nivel_cuenta:
                    self.puntos+=1
                self.nivel+=1
            else:
                self.vidas-=1
            if self.vidas>0 and self.nivel<3:
                #Si sigue vivo y no ha ganado se ejecuta de nuevo
                self.animacion.mario.ind_plat_max=0
                self.iniciar()
            else:
                #Si perdio o gano se acaba la partida
                self.frame.fill((0,0,0))
                self.gameover_rect.dibujar(self.frame)
                pygame.mixer.music.load(os.path.join('musica', 'gameover.ogg'))
                pygame.mixer.music.play()
                pygame.display.flip()
        
