import pygame
from pygame import Surface
import os

# Inicializa PyGame
pygame.init()

# ===== Platforma ===== #
#La clase plataforma es donde camina mario
class Plataforma:
    #E:Dos enteros(coordinadas), y un string(el tipo de plataforma)
    #R:-
    def __init__(self, x, y, tipo):
        #Se definen las variables 
        self.ancho_escalon=25
        self.num_escalones=12
        self.caida=1
        self.x=x
        self.y = y
        self.ancho=300
        self.tipo = tipo
        #Se define la lista de escalones de la plataforma
        self.escalones=[]
        #Se definene las listas de escaleras en plataforma
        self.escaleras_iniciales = []
        self.escaleras_finales =  []
        if self.tipo=="princesa":
            self.num_escalones=5
            self.ancho=125
        if self.tipo== "inicial":
            self.ancho=325
    
    #Crear se encarga de agregar los escalones a self.escalon, dependiendo de si
    #la pataforma es creciente, decreciente, etc
    #E:Ninguna (solo self)
    #S:-
    #R:-
    def crear(self):
        if self.tipo == "creciente":
            self.escalones= self.crear_aux(self.num_escalones, [], self.ancho_escalon,-self.caida, 0, 0)        
        elif self.tipo== "decreciente":
            self.escalones= self.crear_aux( self.num_escalones, [], self.ancho_escalon,self.caida, 0, 0)
        elif self.tipo== "inicial":
            escalones = self.crear_aux( (self.num_escalones+1)//2, [], self.ancho_escalon, 0, 0, 0)
            self.escalones= self.crear_aux( self.num_escalones+1, escalones, self.ancho_escalon,-self.caida, (self.num_escalones+1)//2, (self.num_escalones+1)//2)
        elif self.tipo== "final":
            escalones = self.crear_aux( (self.num_escalones+1)//2, [], self.ancho_escalon, 0, 0, 0)
            self.escalones= self.crear_aux( self.num_escalones, escalones, self.ancho_escalon,self.caida, (self.num_escalones+1)//2, (self.num_escalones+1)//2)
        elif self.tipo=="princesa":
            self.escalones= self.crear_aux( self.num_escalones, [], self.ancho_escalon,0, 0, 0)  
    
    def crear_aux(self, total, escalones, camx,camy, escalones_izquierda, i):
        if i == total:
            return escalones
        else:
            escalon = Escalon(camx*i+self.x, camy*(i-escalones_izquierda)+self.y)
            escalones.append(escalon)
            return self.crear_aux(total, escalones, camx,camy, escalones_izquierda, i+1)

    #dibujar dibuja la escalera escalon por escalon en el frame
    #E:Un frame (y self)
    #S:-
    #R:-
    def dibujar(self, frame):
        for escalon in self.escalones:
            escalon.dibujar(frame)

    #altura devuelve la cordenada y de la escalera para cierto valor de x
    #E:Un numero entero (Coordenada x)
    #S:La posicion en y de la escalera en la coordenada x
    #R:-
    def altura(self, posicionx):
            if self.tipo =="creciente":
                return -self.caida*((posicionx-(self.x))//self.ancho_escalon)+(self.y)
            elif self.tipo=="decreciente":
                 return self.caida*((posicionx-(self.x))//self.ancho_escalon)+(self.y)
            elif self.tipo=="inicial":
                if (posicionx-self.x+self.ancho_escalon//2)//self.ancho_escalon<(self.num_escalones+1)//2+1:
                    return self.y
                else:
                    return -self.caida*((posicionx-self.x+self.ancho_escalon//2)//self.ancho_escalon-(self.num_escalones+1)//2)+(self.y)
            elif self.tipo=="final":
                if (posicionx-self.x)//self.ancho_escalon<(self.num_escalones+1)//2+1:
                    return self.y
                else:
                    return self.caida*(((posicionx-(self.x))//self.ancho_escalon)-(self.num_escalones+1)//2)+(self.y)
            elif self.tipo=="princesa":
                return self.y

    #establecer_escaleras define cuales son las escaleras que inician y terminan
    # en la plataforma
    #E: Una lista de escaleras
    #S:-
    #R:-
    def establecer_escaleras(self,escaleras):
        for escalera in escaleras:
            if escalera.plataforma1 is self:
                self.escaleras_iniciales.append(escalera)
            if escalera.plataforma2 is self:
                self.escaleras_finales.append(escalera)

    #Busca si hay escaleras en la plataforma en cierto rango de x
    #E: Dos enteros ( dos coordenadas en x)
    #S: Una escalera, si existe una en el rango de entrada. Sino retorna -1
    #R:-
    def buscar_escalera(self, iniciox, finalx ,tipo):
        if tipo== "inicial":
            return self.buscar_escalera_aux(iniciox, finalx, self.escaleras_iniciales)
        elif tipo== "final":
            return self.buscar_escalera_aux(iniciox, finalx, self.escaleras_finales)


    def buscar_escalera_aux(self,iniciox, finalx, escaleras):
        if escaleras ==[]:
            return -1
        elif (3*iniciox+finalx)//4<escaleras[0].x+5<=(iniciox+3*finalx)//4:
            return escaleras[0]
        else:
             return self.buscar_escalera_aux(iniciox, finalx, escaleras[1:])        
# ===== Escalon =====#
#La clase escalon son los escalones de la plataforma
class Escalon:
    #E:Dos enteros(coordinadas)
    #R:-
    def __init__(self, x,y):
        self.x = x
        self.y= y
        self.imagen =pygame.image.load(os.path.join('imagenes', 'plataforma.gif'))
        self.rect= self.imagen.get_rect(topleft=(self.x, self.y))
        
    #dibuja el escalon en el frame
    #E: Un frame
    #S: -
    #R: -
    def dibujar(self, frame):
        frame.blit(self.imagen, (self.x, self.y))

# ===== Escalera =====#
class Escalera:
    #E:Un entero (coordenada x), dos plataformas(inferior y superior)
    #R:-
    def __init__(self, x , plataforma1, plataforma2):

        self.x = x
        self.ancho_escalon=13
        self.altura_escalon=6
        self.inicioy = plataforma1.altura(x+self.ancho_escalon//2)
        self.finaly = plataforma2.altura(x+self.ancho_escalon//2)
        #Plataforma arriba
        self.plataforma1 = plataforma1
        #Plataforma abajo
        self.plataforma2 = plataforma2
        self.peldanos=[]
        self.rect1= pygame.Rect((self.x,self.finaly-20),(self.ancho_escalon,-self.finaly+20+self.inicioy))

    #crear crea los peldanos de la escalera
    #E: Niguna (solo self)
    #S: -
    #R: -
    def crear(self):
        continuar =True
        altura= self.inicioy-self.altura_escalon
        while continuar:
            peldano= Peldano(self.x, altura)
            self.peldanos.append(peldano)
            altura-=6
            continuar= altura-6>self.finaly+self.altura_escalon//2

    #dibujar dibuja la escalera en el frame, peldano por peldano
    #E: Un frame
    #S: -
    #R: -
    def dibujar(self, frame):
        for pel in self.peldanos:
            pel.dibujar(frame)
        

# ===== Peldano =====#
#La clase peldano son los peldanos de la plataforma
class Peldano:
    #E:Dos enteros (Coordenadas x, y) 
    #R:-
    def __init__(self, x,y):
        self.x = x
        self.y= y
        self.imagen = pygame.image.load(os.path.join('imagenes', 'escalera.gif'))
        self.rect= self.imagen.get_rect(topleft=(self.x, self.y))
    #dibujar dibuja el peldano en el frame
    #E: Un frame
    #S: -
    #R: -
    def dibujar(self, frame):
        frame.blit(self.imagen, (self.x, self.y))

# ===== Princesa =====#
class Princesa():
    #E:Una plataforma
    #R:-
    def __init__(self, plataforma_princesa):
        #Se definen los sprites de la princesa
        imagen1 = pygame.image.load(os.path.join('imagenes', 'princesa1.png')).convert()
        imagen1.set_colorkey((0,0,0))
        imagen2 = pygame.image.load(os.path.join('imagenes', 'princesa2.png')).convert()
        imagen2.set_colorkey((0,0,0))
        imagen3= pygame.image.load(os.path.join('imagenes', 'princesa3.png')).convert()
        imagen3.set_colorkey((0,0,0))
        #Se pasan todas las imagenes a una lista
        self.imagenes=[imagen1, imagen3,imagen2]
        self.imagen=imagen1

        #Se define el indice de la imagen actual en la lista de imagenes
        self.indice_img=0
        
        self.y=plataforma_princesa.y-self.imagen.get_rect().size[1]
        self.x=plataforma_princesa.x
        self.ancho= self.imagen.get_rect().size[0]
        #Se define la plataforma en la que estara la princesa
        self.plataforma_princesa=plataforma_princesa

    #La siguiente funcion cambia la imagen a la siguiente
    #E: Nada (solo self)
    #S: -
    #R: -
    def siguiente_img(self):
        self.imagen=self.imagenes[self.indice_img]
        self.y=self.plataforma_princesa.y-self.imagen.get_rect().size[1]
        self.indice_img=(self.indice_img+1)%3

    # Se dibuja la princesa    
    #E: Un frame
    #S: -
    #R: -
    def dibujar(self, frame):
        frame.blit(self.imagen, (self.x, self.y))


# ===== Mono =====#
#La clase mono es el mono en la plataforma tipo final del escenario
class Mono():
    #E:Una plataforma
    #R:-
    def __init__(self, plataforma_final):
        #Se define el color transparente de las imagenes
        transColor=(0,0,0)
        #Se definen los sprites del mono
        imagen1 = pygame.image.load(os.path.join('imagenes', 'monoa.png')).convert()
        imagen1.set_colorkey(transColor)
        imagen2 = pygame.image.load(os.path.join('imagenes', 'monob.png')).convert()
        imagen2.set_colorkey(transColor)
        imagen3= pygame.image.load(os.path.join('imagenes', 'monoc.png')).convert()
        imagen3.set_colorkey(transColor)
        imagen4= pygame.image.load(os.path.join('imagenes', 'monod.png')).convert()
        imagen4.set_colorkey(transColor)
        imagen5= pygame.image.load(os.path.join('imagenes', 'monoe.png')).convert()
        imagen5.set_colorkey(transColor)
        imagen6= pygame.image.load(os.path.join('imagenes', 'monof.png')).convert()
        imagen6.set_colorkey(transColor)
        imagen7= pygame.image.load(os.path.join('imagenes', 'monog.png')).convert()
        imagen7.set_colorkey(transColor)
        #Se pasan todas las imagenes a una lista
        self.imagenes=[imagen1, imagen2, imagen3, imagen4,imagen5, imagen6, imagen7]
        #Se define la imagen inicial
        self.imagen=imagen1
        #Se define el indice de la imagen actual en la lista de imagenes
        self.indice_img=0
        self.cantidad_img=len(self.imagenes)
        
        self.y=plataforma_final.y-self.imagen.get_rect().size[1]
        self.x=plataforma_final.x+33
        self.alto= self.imagen.get_rect().size[1]
        
    #Se cambia a la siguiente imagen en la lista de imagenes
    #E: Nada (solo self)
    #S: -
    #R: -
    def siguiente_img(self):
        self.imagen=self.imagenes[self.indice_img]
        self.indice_img=(self.indice_img+1)%len(self.imagenes)

    #Se dibuja el mono en el frame
    #E: Un frame
    #S: -
    #R: -
    def dibujar(self, frame):
        frame.blit(self.imagen, (self.x, self.y))
        
        
        
# ===== Escenario =====#
#Escenario es una clase que contiene a todas las plataformas y escaleras de un nivel
class Escenario():
    #E:Una lista de plataformas, una lista de escaleras
    #R:-
    def __init__(self, plataformas, escaleras):
        self.plataformas=plataformas
        self.escaleras=escaleras
        self.bkg=""
        self.barriles= pygame.image.load(os.path.join('imagenes', 'barriles.png')).convert()
        self.barriles.set_colorkey((255,255,255))
        
    #Dibuja el escenario en el frame, elemento por elemento
    #E: Un frame
    #S: -
    #R: -
    def dibujar(self, frame):
        frame.fill((0,0,0))
        for escal in self.escaleras:
            escal.dibujar(frame)
        for plat in self.plataformas:
            plat.dibujar(frame)
            if plat.tipo=="final":
                frame.blit(self.barriles, (plat.x, plat.y-self.barriles.get_rect().size[1]))
            
       
        self.bkg= frame.copy()
# ===== Boton =====#
#La clase boton es un rect con un texto, se puede usar tambien como un cuadro
#con texto
class Boton():
    #E:Un string (mensjae), cuatro enteros(coordenadas x, y , ancho y altura ), un color y un entero de tamaño de fuente
    #R:-
    def __init__(self,msg,x,y,ancho,alto,color, size=20):
        self.font = pygame.font.SysFont("comicsansms",size)
        self.msg=msg
        self.color=color
        self.x=x
        self.y=y
        self.ancho=ancho
        self.altura=alto

    #Cambia el color del texto en el boton
    #E: Un color
    #S: -
    #R: -
    def cgh_color(self,color):
        self.color=color

    #Dibuja el boton en el frame
    #E: Un frame
    #S: -
    #R: -
    def dibujar(self,frame):
        imagen= self.font.render(self.msg, True, self.color)
        rect=imagen.get_rect()
        rect.center = ( (self.x+(self.ancho/2)), (self.y+(self.altura/2)) )
        frame.blit(imagen, rect)

    #Retorna True si el boton fue cliqueado
    #E: Nada (solo self)
    #S: Un booleano que indica si se hizo cliq en el boton
    #R: -
    def cliqueado(self):
        mouse = pygame.mouse.get_pos()
        if self.x+self.ancho > mouse[0] > self.x and self.y+self.altura > mouse[1] > self.y:
            return True
        return False
