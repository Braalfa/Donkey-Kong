from game_handler import*
from game import*
import pygame

pygame.init()
pygame.font.init()

# ===== Menu ===== #
class Menu():
    #E: Un background
    def __init__(self, bcg):
        #Se crean los botones del menu y se define el fondo
        self.boton_jugar= Boton("Jugar",130,50,100,25,(255,255,255))
        self.boton_mejores= Boton("Salon de la Fama",80,120,200,25,(255,255,255))
        self.boton_conf= Boton("Configuracion",80,190,200,25,(255,255,255))
        self.bcg=bcg
        
    #Se dibuja el fondo y luego los botones
    #E: Un frame, y si mismo
    #S: Ninguna, realiza acciones
    #R: Se espera que la entrada Surface, pero no se analiza 
    def dibujar(self , frame):
        frame.blit(self.bcg,(0,0))
        self.boton_jugar.dibujar(frame)
        self.boton_mejores.dibujar(frame)
        self.boton_conf.dibujar(frame)

        
    #Se espera a que el usuario haga clic en algun boton y se reacciona de acuerdo
    #E: Un frame, y si mismo
    #S: Ninguna, realiza acciones
    #R: Se espera que la entrada sea tipo Surface, pero no se analiza
    def esperar(self, frame):
        pygame.event.clear()
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type== pygame.MOUSEBUTTONDOWN:
                    if self.boton_jugar.cliqueado():
                        game_handler=Game_handler(frame)
                        game_handler.iniciar()
                        self.dibujar(frame)
                        pygame.display.flip()
                        pygame.event.clear()
                    elif self.boton_mejores.cliqueado():
                        mejores=Mejores_menu()
                        mejores.esperar(frame)
                        pygame.event.clear()
                        self.dibujar(frame)
                        pygame.display.flip()
                    elif self.boton_conf.cliqueado():
                        conf=Config_menu()
                        conf.esperar(frame)
                        pygame.event.clear()
                        self.dibujar(frame)
                        pygame.display.flip()
                    

# ===== Mejores_menu ===== #
class Mejores_menu():
    #E:Ninguna (solo self)
    def __init__(self):
        #Se crea el boton de salida
        self.boton_salir= Boton("Salir",130,350,100,100,(255,255,255))
        #Se cargan los mejores y se crean botones para contener esta informacion
        salon= open("salonDeLaFama.txt","r")
        self.cuadros=[]
        lineas= salon.readlines()
        for i in range(0,len(lineas)//2):
            self.cuadros.append(Boton(str(i+1)+"-" +lineas[2*i+1][:len(lineas[2*i+1])-1]+ " "+str(lineas[2*i][:len(lineas[2*i])-1]) +" pts",130,100+50*i,100,100,(0,255,0)))
      
    #Se dibujan todos los botones(Algunos solo son cuadros)
    #E: Un frame, y si mismo
    #S: Ninguna, realiza acciones
    #R: Se espera que la entrada Surface, pero no se analiza 
    def dibujar(self , frame):
        self.boton_salir.dibujar(frame)
        for cuadro in self.cuadros:
            cuadro.dibujar(frame)
        
    #Se espera a que el usuario de cliq en salir y se termina la ejecucion
    #E: Un frame, y si mismo
    #S: Ninguna, realiza acciones
    #R: Se espera que la entrada sea tipo Surface, pero no se analiza
    def esperar(self, frame):
        stay=True
        frame.fill((0,0,0))
        self.dibujar(frame)
        pygame.display.flip()
        while stay:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type== pygame.MOUSEBUTTONDOWN:
                    if self.boton_salir.cliqueado():
                        stay=False
            
            
            
            
            
            

    
# ===== Config_menu ===== #
class Config_menu():
    #E:Ninguna (solo self)
    def __init__(self):
        #Se crean variables para acomodar bien los botones de acuerdo a su grupo
        #Coordenada y de los botones de vida
        vy=50
        #Coordenada y de los botones de obstaculos
        oy=150
        #Coordenada y de los botones de puntos
        py=250
        #Se abren las configuraciones y se establece el menu de acuerdo a estas
        conf= open("config.txt","r")
        lineas=conf.readlines()

        if lineas[0]== "vds3\n":
            self.vds5_color=(255,255,255)
            self.vds3_color=(250,0,0)
        else:
            self.vds5_color=(250,0,0)
            self.vds3_color=(255,255,255)
        if lineas[1]== "facil\n":
            self.dificil_color=(255,255,255)
            self.facil_color=(250,0,0)
        else:
            self.dificil_color=(250,0,0)
            self.facil_color=(255,255,255)
        if lineas[2]== "si-plat\n":
            self.plat_color=(250,0,0)
        else:
            self.plat_color=(255,255,255)

        if lineas[3]== "si-brinco\n":
            self.brinco_color=(250,0,0)
        else:
            self.brinco_color=(255,255,255)
            
        if lineas[4]== "si-nivel\n":
            self.nivel_color=(250,0,0)
        else:
            self.nivel_color=(255,255,255)
            
        conf.close()

        #Se crean los botones y cuadros
        self.boton_salir = Boton("Salir",140,400,100,25,(255,255,255))
        self.boton_vds3 = Boton("3",125,vy,100,25,self.vds3_color)
        self.boton_vds5 = Boton("5",225,vy,100,25,self.vds5_color)
        self.cuadro_vidas = Boton("Vidas:",25,vy,100,25,(255,255,255))
        self.cuadro_obs = Boton("Dificultad:",25,oy,100,25,(255,255,255))
        self.boton_facil = Boton("Facil",125,oy,100,25,self.facil_color)
        self.boton_dificil = Boton("Dificil",225,oy,100,25,self.dificil_color)
        self.cuadro_pts = Boton("Puntos por:",25,py,100,25,(255,255,255))
        self.boton_ptsbrincar = Boton("Brincar",200,py,100,25,self.brinco_color)
        self.boton_ptsplat = Boton("Subir Plataformas",200,py+50,100,25,self.plat_color)
        self.boton_ptsnivel = Boton("Pasar Nivel",200,py+100,100,25,self.nivel_color)
        
        
    #Se dibujan los botones y cuadros
    #E: Un frame, y si mismo
    #S: Ninguna, realiza acciones
    #R: Se espera que la entrada Surface, pero no se analiza 
    def dibujar(self , frame):
        self.boton_salir.dibujar(frame)
        self.boton_vds3.dibujar(frame)
        self.boton_vds5.dibujar(frame)
        self.cuadro_vidas.dibujar(frame)
        self.cuadro_obs.dibujar(frame)
        self.boton_facil.dibujar(frame)
        self.boton_dificil.dibujar(frame)
        self.cuadro_pts.dibujar(frame)
        self.boton_ptsbrincar.dibujar(frame)
        self.boton_ptsplat.dibujar(frame)
        self.boton_ptsnivel.dibujar(frame)
        
    """Se espera a que el usuario interactue con el menu
    Si hace cliq en un boton de cambiar alguna configuracion, se cambian los colores
    de acuerdo a la nueva configuracion
    Se cambian los colores en el menu de acuerdo a los cambios en configuracion
    Las opciones de vida y dificultad (obstaculos por segundo) son exclusivas
    unas de otras
    En las opciones de puntos estara seleccionada al menos una"""

    #E: Un frame, y si mismo
    #S: Ninguna, realiza acciones
    #R: Se espera que la entrada sea tipo Surface, pero no se analiza
    def esperar(self, frame):
        stay=True
        frame.fill((0,0,0))
        self.dibujar(frame)
        pygame.display.flip()
        conf= open("config.txt","r")
        lineas=conf.readlines()
        conf.close()
        while stay:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type== pygame.MOUSEBUTTONDOWN:
                    if self.boton_salir.cliqueado():
                        stay=False
                    if self.boton_vds5.cliqueado():
                        self.vds5_color=(250,0,0)
                        self.vds3_color=(255,255,255)
                        lineas[0]= "vds5\n"
                    if self.boton_vds3.cliqueado():
                        self.vds5_color=(255,255,255)
                        self.vds3_color=(250,0,0)
                        lineas[0]= "vds3\n"
                    if self.boton_facil.cliqueado():
                        self.dificil_color=(255,255,255)
                        self.facil_color=(250,0,0)
                        lineas[1]= "facil\n"
                    if self.boton_dificil.cliqueado():
                        self.facil_color=(255,255,255)
                        self.dificil_color=(250,0,0)
                        lineas[1]= "dificil\n"
                    if self.boton_ptsbrincar.cliqueado():
                        if lineas[3]== "no-brinco\n":
                            self.brinco_color=(250,0,0)
                            lineas[3]= "si-brinco\n"
                        elif lineas[2]== "si-plat\n" or lineas[4]== "si-nivel\n":
                            self.brinco_color=(255,255,255)
                            lineas[3]= "no-brinco\n"
                    if self.boton_ptsplat.cliqueado():
                        if lineas[2]== "no-plat\n":
                            self.plat_color=(250,0,0)
                            lineas[2]= "si-plat\n"
                        elif lineas[3]== "si-brinco\n" or lineas[4]== "si-nivel\n":
                            self.plat_color=(255,255,255)
                            lineas[2]= "no-plat\n"
                    if self.boton_ptsnivel.cliqueado():
                        if lineas[4]== "no-nivel\n":
                            self.nivel_color=(250,0,0)
                            lineas[4]= "si-nivel\n"
                        elif lineas[3]== "si-brinco\n" or lineas[2]== "si-plat\n":
                            self.nivel_color=(255,255,255)
                            lineas[4]= "no-nivel\n"
                    
                    self.actualizar_colores()
                    frame.fill((0,0,0))
                    self.dibujar(frame)
                    pygame.display.flip()

        conf= open("config.txt","w")
        conf.writelines(lineas)
        conf.close()

        
    #Se actualizan los colores de los botones
    #E: Ninguna(solo self)
    #S: Ninguna, realiza acciones
    #R: Ninguna

    def actualizar_colores(self):
        self.boton_vds3.cgh_color(self.vds3_color)
        self.boton_vds5.cgh_color(self.vds5_color)
        self.boton_facil.cgh_color(self.facil_color)
        self.boton_dificil.cgh_color(self.dificil_color)
        self.boton_ptsbrincar.cgh_color(self.brinco_color)
        self.boton_ptsplat.cgh_color(self.plat_color)
        self.boton_ptsnivel.cgh_color(self.nivel_color)
        

