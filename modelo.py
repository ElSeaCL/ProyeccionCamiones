import numpy as np
'''
TODO: 
- funcion que defina la diferencia de caudal de entrada y salida de un ELD.
- Ajuste de centrifugas en operación para para que la diferencia de caudales en el ELD
    sea positiva (permita acumular lodo)
- Permitir fijar una cantidad de camiones a asignar distinto para una hora especifica. A utilizar
en caso de domingos y fechas especificas.
'''

class Centrifuga:
    prioridades = [1, 2, 3, 4, 5, 6]
    silos = ['siloA', 'siloB', 'siloC', 'siloD']
    estanques = ['eld1', 'eld2', 'eld3']

    def __init__(self, id, estanque, silo, caudal, prioridad, dias):
        self.id = id
        self.setterPrioridad(prioridad)
        self.silo = silo
        self.estanque = estanque
        self.caudalReferencia = caudal
        self.caudalHorario = np.full((24 * dias, 1), caudal)
        
    def setterPrioridad(self, prioridad):
        try:
            Centrifuga.prioridades.remove(prioridad)
            self.prioridad = prioridad
        except:
            print("Prioridad no existente o ya fue asignada")
            return False

    def setterSilo(self, silo):
        try:
            silo in Centrifuga.silos
            self.silo = silo
        except:
            print("valor de silo ingresado no valido")
            return False

    def setterEstanque(self, estanque):
        try:
            estanque in Centrifuga.estanques
            self.estanque = estanque
        except:
            print("Valor de estanque no valido")
        
    def detenerCentrifuga(self, hora):
        self.caudalHorario[hora] = 0

    def operarCentrifuga(self):
        self.caudal = self.caudalReferencia

    def toString(self):
        return print("Centrìfuga " + str(self.id) + " alimentada por el estanque " + 
        str(self.estanque) + " y alineada al silo " + str(self.silo))

class TallerDeshidratacion:
    centrifugas = []

    def __init__(self):
        return 

    def addCentrifuga(self, centrifuga):
        if isinstance(centrifuga, Centrifuga):
            TallerDeshidratacion.centrifugas.append(centrifuga)
        else:
            print("Valor no valido.")
    
    def caudalEstanque(self, estanque, hora):
        caudal = 0

        for cent in TallerDeshidratacion.centrifugas:
            if cent.estanque == estanque:
                caudal += cent.caudalHorario[hora]
            
        return float(caudal)

    def caudalSilo(self, silo, hora):
        caudal = 0

        for cent in TallerDeshidratacion.centrifugas:
            if cent.silo == silo:
                caudal += cent.caudalHorario[hora]
        
        return float(caudal)
    
    def detenerCentSilo(self, silo, hora):
        for cent in TallerDeshidratacion.centrifugas:
            if cent.silo == silo:
                cent.detenerCentrifuga(hora)
    
    def detenerCentPrioridad(self, estanque, hora):
        '''
            Detiene la centrìfuga con mayor valor de prioridad.
        '''

        zipCent = zip(range(len(TallerDeshidratacion.centrifugas)),
        [x.prioridad for x in TallerDeshidratacion.centrifugas])

        listCent = sorted(zipCent, key=lambda x: x[1], reverse=True)
        for tupleIndex in listCent:
            a, _ = tupleIndex
            if TallerDeshidratacion.centrifugas[a].estanque == estanque:
                TallerDeshidratacion.centrifugas[a].detenerCentrifuga(hora)
            
class EstanqueLodoDigerido:

    def __init__(self, volumen, caudalDig, nivelActual = 0, dias = 1):
        self.volumen = volumen
        self.nivelHorario = np.zeros((24 * dias, 1))
        self.nivelHorario[0] = nivelActual
        self.caudalHorario = np.full((24 * dias, 1), caudalDig/24)
        
    def calcularNivel(self, caudalCentrifugas, hora):
        self.nivelHorario[hora] = (self.nivelHorario[hora - 1] /100 * self.volumen + self.caudalHorario[hora - 1] - caudalCentrifugas) * 100 / (self.volumen)

        return self.nivelHorario[hora]

    def getNivel(self, hora):
        return self.nivelHorario[hora]

    def getCaudalHorario(self):
        return self.caudalHorario

class Silo:
    id = ['siloA', 'siloB', 'siloC', 'siloD']

    def __init__(self, id, nivelActual, dias, factor, pesoCamion, alturaCamion):
        self.id = id
        self.dias = dias
        self.nivel = np.zeros((24 * dias, 1))
        self.nivel[0] = nivelActual  
        self.factor = factor 
        self.pesoCamion = pesoCamion
        self.alturaCamion = alturaCamion
        self.camionesAsignados = np.zeros((24 * dias, 1))  

    def getNivel(self):
        return self.nivel  

    def calcularNivel(self, caudalCentrifugas, hora):
        self.nivel[hora] = self.nivel[hora - 1] + caudalCentrifugas * self.factor / self.pesoCamion * self.alturaCamion - self.getCamionesAsignados()[hora - 1]
        
        return self.nivel[hora]

    def asignarCamion(self, hora):
        self.camionesAsignados[hora] += 1

    def getCamionesAsignados(self):
        return self.camionesAsignados

class TallerSilos:

    silos = []
    
    def __init__(self, horasCarguio, numCamiones, dias):
        self.horasCarguio = horasCarguio
        camiones = np.zeros((24, 1))
        for i in range(24):
            if i in horasCarguio:
                camiones[i] = numCamiones
        self.camionesDisponibles = camiones
        for i in range(dias):
            self.camionesDisponibles = \
            np.concatenate((self.camionesDisponibles, self.camionesDisponibles), axis = 0)

    def addSilo(self, silo):
        if isinstance(silo, Silo):
            TallerSilos.silos.append(silo)
        else:
            print("Valor no válido.")

    def getNivelSilos(self):
        listaSilos = [x.nivel for x in TallerSilos.silos]
        return np.concatenate(listaSilos, axis=1)

    def getCamionesDisponibles(self):
        return self.camionesDisponibles

    def getCamionesProyectados(self):
        return np.concatenate([x.getCamionesAsignados() for x in TallerSilos.silos], axis=1)

    def getIndSiloMayor(self, hora):
        ind = list(self.getNivelSilos()[hora]).index(max(self.getNivelSilos()[hora]))
        return ind

    def getSiloMayor(self, hora):
        ind = self.getIndSiloMayor(hora)
        return TallerSilos.silos[ind]

    def asignarCamion(self, silo, hora):
        silo.asignarCamion(hora)
        self.camionesDisponibles[hora] -= 1

    def esHoraDeCarguio(self, hora):
        if self.camionesDisponibles[hora] > 0:
            return True
        else:
            return False
    
    
