'''
TODO:
    - Crear objetos de manera dinamica tras solicitar informacion al usuario.
    http://jelly.codes/articles/python-dynamically-creating-classes/
    - Permitir la visualizacion de datos cargados anteriormente, almacenados
    en csv para creaar rapidamente los objetos usados en el modelo.
    -    
'''

import sys
from modelo import (
    Centrifuga, 
    Silo, 
    EstanqueLodoDigerido, 
    TallerSilos, 
    TallerDeshidratacion, 
    AreaELD
)

class Menu:

    HORAS = [1, 5, 10]
    NUMCAMIONES = 7
    MINELD = 35
    MINSILO = 2.3
    MAXSILO = 10
    VOLELD = {'eld1': 4240, 'eld2': 4240, 'eld3': 2300}
    ALTURASILOCAMION = 2.3
    PESOCAMION = 2_887

    def __init__(self):
        self.opciones = {
            "1":self.diasProyeccion,
            "2":self.nivelEstanquesSilos,
            "3":self.parametrosSilos,
            "4":self.main
        }
        pass

    def bienvenida(self):
        print('''
        Bienvenido al programa de proyección de camiones :>

        Este programa tiene como objetivo calcular la cantidad de camiones necesarios para cumplir con los requerimientos de nivel tanto en los estanques como en silo. 
        El programa automaticamente ajusta la cantidad necesaria de centrifugas en funcionamiento para lograr esto.

        Creado por Sebastián González (elSea).
        Se aceptan donaciones

        ''')
        input("Aprete <ENTER> para continuar")
        pass
    
    def displayMenu(self):
        print('''
        1. Ingresar días de proyección.
        2. Ingresar niveles estanques/silos.
        3. Ingresar parámetros de silos.
        4. Ingresar parámetros de operación centrífugas.
        5. Calcular!
        ''')
        pass

    def diasProyeccion(self):
        self.dias = input("ingresa los dìas de proyecciòn")
        pass

    def nivelEstanquesSilos(self):
        numEstanques = input("Ingresa estanques en operaciòn")

        for i in range(numEstanques):
            id = input("Ingresa id del estanque")
            vol = input("Ingresa volumen del estanque")
            minlvl = input("Ingresa nivel minimo de operaciòn")
            new_eld = EstanqueLodoDigerido(id, vol, 4000, minlvl)
            globals()[id] = new_eld



        for i in list(VOLELD.keys()):
            bol = input("El " + i + " se encuentra disponible? (S/N)")
            if bol == "S":
                input("Ingresa el nivel del estanque: ")
        pass

    def parametrosSilos(self):
        pass

    def main(self):
        pass
    

        

    # # Ingresar numero de dias de la proyección
    # flag = True
    # while flag:
    #     dias = input('Ingrese el número de días de proyección: \n')

    #     try:
    #         dias = int(dias)
    #         if dias > 0:
    #             flag = False
    #         else:
    #             print('valor no valido')
    #     except:
    #         print("valor no valido")

    # # Ingresar nivel del ELD1
    # flag = True    
    # while flag:
    #     eld840 = input('Ingrese el nivel (porcentual) del ELD1: \n')

    #     try:
    #         eld840 = float(eld840)
    #         if eld840 > 0 and eld840 <= 100:
    #             flag = False
    #         else:
    #             print('Valor invalido')
    #     except:
    #         print('valor no valido, puto')

    # # Ingresar nivel del ELD3
    # flag = True    
    # while flag:
    #     eld1840 = input('Ingrese el nivel (porcentual) del ELD3: \n')

    #     try:
    #         eld1840 = float(eld1840)
    #         if eld1840 > 0 and eld1840 <= 100:
    #             flag = False
    #         else:
    #             print('Valor invalido')
    #     except:
    #         print('valor no valido, puto')

    # # Ingresar nivel de los silos de silos de lodo deshidratado
    # print('Ingrese niveles de los silos de lodo')
    # nivelSilos = list()
    # for i in range(4):
    #     flag = True 
    #     while flag:
    #         silo = input('silo ' + str(i + 1) + ': ')

    #         try:
    #             silo = float(silo)
    #             if silo > 0 and silo < 12:
    #                 nivelSilos.append(silo)
    #                 flag = False
    #             else:
    #                 print('valor no valido, puto')
    #         except:
    #             print('valor no valido, puto')