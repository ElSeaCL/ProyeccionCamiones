from modelo import Centrifuga, Silo, EstanqueLodoDigerido, TallerSilos, TallerDeshidratacion

# Ingreso de variables

silos = ['siloA', 'siloB', 'siloC', 'siloD']

dias = 7
factor = 109
alturaSiloCamion = 2.3
pesoCamion = 42000
horas = [1, 6, 9]
minELD = 35
minSilo = 4.6
maxSilo = 10
numCamiones = 7

# Creación de objetos

eld1 = EstanqueLodoDigerido(4240, 4020, 50, dias)

siloA = Silo('siloA', 6.9, dias, factor, pesoCamion, alturaSiloCamion)
siloB = Silo('siloB', 3.9, dias, factor, pesoCamion, alturaSiloCamion)
siloC = Silo('siloC', 5.7, dias, factor, pesoCamion, alturaSiloCamion)
siloD = Silo('siloD', 9.7, dias, factor, pesoCamion, alturaSiloCamion)

taller_silos = TallerSilos(horas, numCamiones, dias)

taller_silos.addSilo(siloA)
taller_silos.addSilo(siloB)
taller_silos.addSilo(siloC)
taller_silos.addSilo(siloD)

centA = Centrifuga('A', 'eld1', 'siloA', 45, 5, dias)
centB = Centrifuga('B', 'eld1', 'siloD', 45, 4, dias)
centC = Centrifuga('C', 'eld1', 'siloA', 30, 3, dias)
centD = Centrifuga('D', 'eld1', 'siloC', 30, 6, dias)
centE = Centrifuga('E', 'eld1', 'siloC', 55, 2, dias)
centF = Centrifuga('F', 'eld1', 'siloD', 45, 1, dias)

taller_deshidratacion = TallerDeshidratacion()

taller_deshidratacion.addCentrifuga(centA)
taller_deshidratacion.addCentrifuga(centB)
taller_deshidratacion.addCentrifuga(centC)
taller_deshidratacion.addCentrifuga(centD)
taller_deshidratacion.addCentrifuga(centE)
taller_deshidratacion.addCentrifuga(centF)

# Loop ajuste de centrífugas con asignación de camiones

for hora in range(24* dias):

    modList = list(taller_silos.getNivelSilos()[hora])

    # Asignación de camiones
    if taller_silos.esHoraDeCarguio(hora):
        while max(modList) >= minSilo and taller_silos.getCamionesDisponibles()[hora][0] > 0:
            ind = modList.index(max(modList))
            silo = taller_silos.silos[ind]
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
            while eld1.getCaudalHorario()[hora][0] - taller_deshidratacion.caudalEstanque('eld1', hora) < 0:
                taller_deshidratacion.detenerCentPrioridad('eld1', hora)
                caudal_estanque = taller_deshidratacion.caudalEstanque('eld1', hora)
                print("el caudal de centrifugas es de" + str(caudal_estanque))
                niveleld1 = eld1.calcularNivel(caudal_estanque, hora + 1)
                print("El nivel proyectado es de" + str(niveleld1))

        eld1.calcularNivel(caudal_estanque, hora + 1)

        # Calcular nivel de silos para proxima hora
        for silo in taller_silos.silos:
            id = silo.id
            silo.calcularNivel(taller_deshidratacion.caudalSilo(id, hora), hora + 1)

