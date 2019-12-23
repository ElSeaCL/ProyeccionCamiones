from modelo import Centrifuga, Silo, EstanqueLodoDigerido, TallerSilos, TallerDeshidratacion

# Ingreso de variables

silos = ['siloA', 'siloB', 'siloC', 'siloD']

dias = 7
factor = 114.19
alturaSiloCamion = 2.3
pesoCamion = 24_213
horas = [1, 5, 10]
minELD = 35
minSilo = 4.6
maxSilo = 10
numCamiones = 7

# Creación de objetos

eld1 = EstanqueLodoDigerido('eld1', 4240, 2887, 37.8, dias)

siloA = Silo('siloA', 6.5, dias, factor, pesoCamion, alturaSiloCamion)
siloB = Silo('siloB', 5.2, dias, factor, pesoCamion, alturaSiloCamion)
siloC = Silo('siloC', 9.2, dias, factor, pesoCamion, alturaSiloCamion)
siloD = Silo('siloD', 9.3, dias, factor, pesoCamion, alturaSiloCamion)

taller_silos = Silo.taller_silos
taller_silos.setCamionesDisponibles(horas, numCamiones, dias)

taller_silos.setCamionesHora(0, 10, 2)
taller_silos.setCamionesHora(0, 1, 3)
taller_silos.setCamionesHora(0, 5, 3)

centA = Centrifuga('A', 'eld1', 'siloA', 45, 5, dias)
centB = Centrifuga('B', 'eld1', 'siloD', 45, 4, dias)
centC = Centrifuga('C', 'eld1', 'siloA', 30, 3, dias)
centD = Centrifuga('D', 'eld1', 'siloC', 30, 6, dias)
centE = Centrifuga('E', 'eld1', 'siloC', 55, 2, dias)
centF = Centrifuga('F', 'eld1', 'siloD', 45, 1, dias)

taller_deshidratacion = Centrifuga.taller_deshidratacion

# Loop ajuste de centrífugas con asignación de camiones

for hora in range(24* dias):

    print(taller_deshidratacion.getCaudalporCentrifuga()[hora: hora + 10])
    modList = list(taller_silos.getNivelSilos()[hora])

    # Asignación de camiones
    if taller_silos.esHoraDeCarguio(hora):
        while max(modList) >= minSilo and taller_silos.getCamionesDisponibles()[hora][0] > 0:
            ind = modList.index(max(modList))
            silo = taller_silos[ind]
            taller_silos.asignarCamion(silo, hora)
            modList[ind] -= alturaSiloCamion 

    # Detención de centrífugas si el silo está lleno
    for nivel in modList:
        if nivel > maxSilo:
            i = modList.index(nivel)
            silo = silos[i]
            taller_deshidratacion.detenerCentSilo(silo, hora)

    if not hora == (24 * dias - 1):
        
        # Calculo nivel de ELD tras detencion de centrifugas por silo
        caudal_estanque = taller_deshidratacion.caudalEstanque('eld1', hora)
        eld1.calcularNivel(caudal_estanque, hora + 1)

        # Detención de centrífugas si el nivel del silo está bajo el mínimo
        if eld1.getNivel(hora + 1)[0] < minELD:
            #
            zipCent = zip(range(len(taller_deshidratacion)), [x.prioridad for x in taller_deshidratacion])
            listCent = sorted(zipCent, key=lambda x: x[1], reverse=True)
            #
            while eld1.getCaudalHorario()[hora][0] - taller_deshidratacion.caudalEstanque('eld1', hora) < 0:
                #
                a, _ = listCent.pop(0)
                taller_deshidratacion[a].detenerCentrifuga(hora)
                # taller_deshidratacion.detenerCentPrioridad('eld1', hora)
                #
                caudal_estanque = taller_deshidratacion.caudalEstanque('eld1', hora)
                niveleld1 = eld1.calcularNivel(caudal_estanque, hora + 1)

        eld1.calcularNivel(caudal_estanque, hora + 1)

        # Calcular nivel de silos para proxima hora
        for silo in taller_silos:
            id = silo.id
            silo.calcularNivel(taller_deshidratacion.caudalSilo(id, hora), hora + 1)
    
