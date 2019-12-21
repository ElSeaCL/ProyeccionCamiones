import sys
from main import *


# Ingresar numero de dias de la proyección
flag = True
while flag:
    dias = input('Ingrese el número de días de proyección: \n')

    try:
        dias = int(dias)
        if dias > 0:
            flag = False
        else:
            print('valor no valido')
    except:
        print("valor no valido")

# Ingresar nivel del ELD1
flag = True    
while flag:
    eld840 = input('Ingrese el nivel (porcentual) del ELD1: \n')

    try:
        eld840 = float(eld840)
        if eld840 > 0 and eld840 <= 100:
            flag = False
        else:
            print('Valor invalido')
    except:
        print('valor no valido, puto')

# Ingresar nivel del ELD3
flag = True    
while flag:
    eld1840 = input('Ingrese el nivel (porcentual) del ELD3: \n')

    try:
        eld1840 = float(eld1840)
        if eld1840 > 0 and eld1840 <= 100:
            flag = False
        else:
            print('Valor invalido')
    except:
        print('valor no valido, puto')

# Ingresar nivel de los silos de silos de lodo deshidratado
print('Ingrese niveles de los silos de lodo')
nivelSilos = list()
for i in range(4):
    flag = True 
    while flag:
        silo = input('silo ' + str(i + 1) + ': ')

        try:
            silo = float(silo)
            if silo > 0 and silo < 12:
                nivelSilos.append(silo)
                flag = False
            else:
                print('valor no valido, puto')
        except:
            print('valor no valido, puto')

