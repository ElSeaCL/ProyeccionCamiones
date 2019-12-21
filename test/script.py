'''
Borrador de programa que permite realizar el ajuste de camiones de lodo deshidratado.

Este programa viene a reemplazar el desarrollado anteriormente en VBA. Inicialmente se espera
replicar su estructura. Una vez se consiga una estructura básica funcional se realizaran los
cambios necesarios a favor de la eficiencia del programa.

Tomando esto en cuenta, el programara funcionará en conjunto con e archivo ya existente 
'Proyección LD nuevo 2019' del cual se van a extraer los datos iniciales, y donde se escribirán los 
resultados finales.

Uno de los objetivos es depender en la menor medida posible de las herramientas de excel, solo utilizando
los calculos de valores iniciales y la funcion de gráfico

TODO:

 - Revisar si es posible manejar los datos arrays de celdas a listas. Puede que el manejo se mas rapido así
 - Extender el uso del programa para los distintos estanques de lodo digerido.

'''

import numpy as np
from openpyxl import load_workbook
wb = load_workbook(filename = 'Proyección LD nuevo 2019.xlsx', data_only=True)

# Funciones

def array2list(array):
    '''
        Devuelve una lista a partir de un array de openpyxl 
    '''

    return [x[0].value for x in array]

def xl2npMatrix(hoja, minrow, maxrow, mincol, maxcol):
    '''
        Toma una hoja de excel y tras definir los limites de extracción de datos,
        (fila minima, fila máxima, columna minima, columna máxima) devuelve una
        matriz de numpy.

        :param hoja: Nombre de la hoja de excel de la que extraen los datos
        :param minrow: Numero de la fila donde se empieza a rescatar los valores.
        :param maxrow: Numero de la fila donde termina de rescatar los valores.
        :param mincol: Numero de la columna donde se empieza a rescatar los valores.
        :param maxcol: Numero de la columna donde termina de rescatar los valores.
        :returns: Matriz de Numpy con los valores.

        >>> xl2npMatrix('hoja1', 1, 3, 2, 4)
        array([[1, 0, 1],
               [1, 0, 1]])
    '''

    listo = list()

    for row in hoja.iter_rows(min_row = minrow, max_row = maxrow, 
    min_col = mincol, max_col = maxcol):
        for cell in row:
            listo.append(cell.value)
    
    listo = np.array(listo)
    listo = listo.reshape(maxrow - minrow + 1, maxcol - mincol + 1)

    return listo

def nivelEstanque(nivelAnterior, caudalDig, caudalCent):
    '''
    Calcula el nivel de la cámaara de acumulación de lodo digerido a 
    partir del nivel previo, el funcionamiento de las centrífugas y la 
    alimentación de lodo a los digestores.

    :param nivelAnterior: an integer >= 0 and <= 1
    :param caudalDig: an integer >= 0 / 
    :param caudalCent: an integer >= 0
    :returns: nivelActual

    >>> acumulacionLD(0.84, 150, 230)
    0.82 
    '''

    return (nivelAnterior * eld1 + caudalDig - caudalCent) / eld1

def nivelSilo(nivelAnterior, caudalCent):
    '''
    Calcula el nivel del silo de lodo deshidratado a partir del caudal de las
    centrífugas en operación y el nivel anterior del silo.

    :param nivelAnterior: an integer >= 0
    :param caudalCent: an integer >= 0
    :returns: nivelSilo

    >>> nivelSilo(2, 100)
    2.44663
    '''

    return nivelAnterior + caudalCent * factor840 / (cargaCamion * 1000) * alturaSiloCamion

def dictSilosCentrifugas(hora):
    '''
    Crea un Diccionario donde las keys corresponden a los distintos silos, cada silo esta 
    asociado a una lista con un caracter representando a la centrífuga con la que está
    alineado.
    
    :param hora: Numero entero que representa la hora de la que se extrae la alineación.
    :returns: Diccionario con las centrífugas por silo.

    >>> dictSilosCentrifugas()
    {'A': [0, 2], 'B': [], 'C': [3, 4], 'D': [1, 5]}
    '''

    siloCent = {'A':[], 'B':[], 'C':[], 'D':[]}
    for i in range(6):
        siloCent[alinCent2Silos[hora][i]].append(i)
    
    for i in ['A', 'B', 'C', 'D']:
        lis = []
        for j in range(6):
            if j in siloCent[i]:
                lis.append(1)
            else:
                lis.append(0)
        siloCent[i] = lis

    return siloCent

def fijarCaudalCent(hora):
    '''
    Fija las centrifugas operando a partir del array de los caudales y el de
    disponibilidad de las centrífugas.

    :param hora: Número entero que representa la hora de la que se fijan las centrífugas.
    :returns: Array de Numpy con los caudales establecidos de operación a la hora indicada.

    >>> fijarCaudalCent(0)
    array([45., 45., 30.,  0., 55., 45.])
    '''

    return dispCentrifugas[hora] * caudalCent

def ajusteCentEstanque(hora):
    '''
    Ajusta el array de centrifugas disponibles (dispCentrifugas) para que la suma
    de los caudales de centrifugas disponible sea menor al caudal de digestores
    al estanque 840 (caudalesDig840).

    :param hora: Numero entero que representa la hora en la que se realiza el ajuste.
    :returns: None

    >>> ajusteCentEstanque(0)

    '''

    dif = sum(caudalesCent840[hora]) - float(caudalesDig840[hora])
    caudalDetenido = 0
    prioridadCent = estadoCent[:]

    while caudalDetenido < dif:
        centMenorPrioridad = prioridadCent.index(max(prioridadCent))          # indice de la centrífuga con menor prioridad
        dispCentrifugas[hora][centMenorPrioridad] = 0                         # Determina la centrifuga con minima prioridad y la asgina como detenida
        prioridadCent[centMenorPrioridad] = 0                                 # La lista de prioridad se deja en 0

        caudalesCent840[hora] = fijarCaudalCent(hora)                         # Llama a la funcion para fijar el caudal por centrifuga operativa
        dif = sum(caudalesCent840[hora]) - float(caudalesDig840[hora])        # Calcula la diferencia entre lo alimentado a digestores con lo cargado a centrifugas
        print("una vuelta")
    return dispCentrifugas[hora]

def ajusteCentSilo(hora, numsilo):
    '''
    Ajusta el array de centrifugas disponibles (dispCentrifugas) para que en caso
    de que uno de los silos de lodo deshidratado haya alcanzado su nivel máximo
    las centrífugas asociadas a este se detengan.

    :param hora: Numero entero que representa la hora en la que se realiza el ajuste. 
    :returns: None

    >>> ajusteCentSilo(0)

    '''

    dispCentrifugas[hora] = dispCentrifugas[hora] * (np.array([1, 1, 1, 1, 1, 1]) - dictSiloCent[silo[numsilo]])

    #dispCentrifugas[hora] =  dictSiloCent[silos[i]]
    #dispCentrifugas[hora][centSilo] = 0
    
    return dispCentrifugas[hora]

def asignarCamiones(hora, maxCamiones):
    '''
    Llena la matriz de camiones a la hora especificada segun la posibilidad de carga
    de cada uno de los silos, representado por la matriz de silos.

    :param hora: Numero entero que representa la hora en la que se realiza el ajuste. 
    :param maxCamiones: Numero entero que representa el numero máximo de camiones a asignar.
    :returns: None.

    >>> asginarCamiones(5, 7)

    '''

    cont = 0
    modsilos = list(silos[hora])

    while cont < maxCamiones:
        indSiloMax = modsilos.index(max(modsilos))
        if modsilos[indSiloMax] >= minSilo * alturaSiloCamion:
            camionesCargados[hora][indSiloMax] += 1
            modsilos[indSiloMax] -= alturaSiloCamion
        
        else:
            break 
        cont += 1
    silos[hora] = np.array(modsilos)

    return

# constantes a rescatar
sheet_val = wb['VAL']

eld1 = sheet_val['C6'].value                # Volumen del ELD1
eld3 = sheet_val['C8'].value                # Volumen del ELD3
factor840 = sheet_val['D14'].value          # Factor para calcular el lodo equivalente a silo
alturaSiloCamion = sheet_val['E16'].value   # Metros de silo equivalente a 1 camión
cargaCamion = sheet_val['E17'].value        # toneladas de lodo cargados por camión

#  Parámetros base proyección
sheet_proy = wb['PROYECCIÓN']

## Niveles de operación 840
min840 = sheet_proy['C5'].value
max840 = sheet_proy['D5'].value

## Niveles de operación silos
minSilo = sheet_proy['Q5'].value
maxSilo = sheet_proy['Q6'].value

## maximo de camiones diario
maxCamiones = sheet_proy['I5:I11']
maxCamiones = array2list(maxCamiones)

## Estado y prioridad de las centrifugas
estadoCent = sheet_proy['L5:L10']
estadoCent = array2list(estadoCent)
for i in range(6):
    if isinstance(estadoCent[i], str):
        estadoCent[i] = 0

## Caudales de centrífugas
caudalCent = sheet_proy['M5:M10']
caudalCent = array2list(caudalCent)

## inicio y fin de proyección
inicio = sheet_proy['D22'].value
fin = sheet_proy['D23'].value
dias = fin - inicio + 1

## DataFrames de referencia
sheet_cam = wb['CAMIONES']

# Cauadal de entrada a digestores por día de la semana
cargaSemana = sheet_cam['S9:S15']
cargaSemana = array2list(cargaSemana)

# Caudal de alimentación a digestores primer día de semana
caudalDia840 = cargaSemana[0]
caudalDia1840 = sheet_cam['T9'].value

## Matrices disponibilidad ELD
dispELD = xl2npMatrix(sheet_cam, 26, 49, 5, 7)

## Matriz disponibildiad Silos
dispSilos = xl2npMatrix(sheet_cam, 26, 49, 8, 11)

## Matriz alineación centrífuga
alinCent2Silos = xl2npMatrix(sheet_cam, 26, 49, 12, 17)
# Diccionario con los datos de la primera hora
dictSiloCent = dictSilosCentrifugas(0)

## Matriz ingreso niveles
nivelEstanqueIngresado = xl2npMatrix(sheet_cam, 21, 23, 26, 49)

## Matriz caudales
caudalesDig840 = np.full((24,1), caudalDia840/24)
caudalesquitDig1840 = np.full((24,1), caudalDia1840/24)
#print(caudalHora840)

# Matriz a completar
caudales = np.zeros((24, 6))            # Caudales de centrífugas
nivel840 = np.zeros((24, 1))            # Niveles del estanque 840
nivel1840 = np.zeros((24,1))            # Niveles del estanque 1840
silos = np.zeros((24, 4))               # Nivel de los silos de lodo deshidratado
camionesCargados = np.zeros((24, 4))    # numero de camiones a cargar por silos
dispCentrifugas = np.zeros((24, 6))     # Matriz binaria que indica por hora si la centrífuga se encuentra disponible o no



#############################################################
#### MAIN
#############################################################

periodoProyeccion = dias * 24

# Fijar la matriz de disponibilidad segun las centrífugas operativas
for i in range(6):
    if estadoCent[i] == 0:
        dispCentrifugas[0][i] = 0
    else:
        dispCentrifugas[0][i] = 1

for i in range(dispCentrifugas.shape[0] - 1):
    dispCentrifugas[i + 1] = dispCentrifugas[0]

# Fijar caudales de centrífugas
caudalesCent840 = dispCentrifugas * caudalCent
print(caudalesCent840)

# codigo perteneciente al test del programa
nivel840inicial = 0.20
nivelesSilinicial = [9.5, 4.8, 6.0, 5.5]

nivel840[0] = nivel840inicial
silos[0] = nivelesSilinicial

silo = ['A', 'B', 'C', 'D']

for i in range(24):

    # Asignacion de camiones a las horas seleccionadas:
    if i in [0, 4, 7]:
        asignarCamiones(i, 7)

    # Detención de centrifugas si silo está por sobre el minimo
    for j in range(4):
        if silos[i][j] >= maxSilo:
            dispCentrifugas[i] = ajusteCentSilo(i, j)
            caudalesCent840[i] = fijarCaudalCent(i)

    # Ajuste disponibilidad si nivel de 840 está por debajo del minimo 
    if nivel840[i] <= min840:
        dispCentrifugas[i] = ajusteCentEstanque(i)
        caudalesCent840[i] = fijarCaudalCent(i)

    if i != 23:
        # Calculo del nivel de silo para la hora siguiente
        nivel840[i + 1] = nivelEstanque(nivel840[i], caudalesDig840[i], sum(caudalesCent840[i]))

        # Calculo del nivel de los silos para la hora siguiente
        for j in range(4):
            silos[i + 1][j] = nivelSilo(silos[i][j], sum(dictSiloCent[silo[j]] * np.array(caudalesCent840[i])))

    print(" se completa el ciclo " + str(i+1))





